import logging
import os
from pathlib import Path
from urllib.parse import urlparse

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Always load backend/.env regardless of the shell's current working directory.
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "dev-only-change-in-production-not-for-production-use"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() in ("1", "true", "yes")


def _normalize_allowed_host(raw: str) -> str:
    """
    Accept host values in common env formats:
    - api.example.com
    - https://api.example.com/
    - api.example.com:443
    """
    v = (raw or "").strip().rstrip("/")
    if not v:
        return ""
    if v.startswith(("http://", "https://")):
        try:
            p = urlparse(v)
            v = p.netloc or p.path or ""
        except Exception:
            return ""
    # Drop any path accidentally included without scheme.
    v = v.split("/")[0].strip()
    # If host:port, keep only host for ALLOWED_HOSTS matching.
    if ":" in v and not v.startswith("["):
        v = v.split(":", 1)[0].strip()
    return v


_allowed_hosts_raw = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,.railway.app,healthcheck.railway.app,api.helixprimesolutions.com",
)
ALLOWED_HOSTS = []
for _raw in _allowed_hosts_raw.split(","):
    _h = _normalize_allowed_host(_raw)
    if _h and _h not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_h)
# Railway hostnames vary: *.up.railway.app, *.railway.app, and internal *.railway.internal.
if os.environ.get("RAILWAY_ENVIRONMENT"):
    _hosts_blob = " ".join(ALLOWED_HOSTS)
    for _suffix in (".up.railway.app", ".railway.app", ".railway.internal"):
        if _suffix not in _hosts_blob:
            ALLOWED_HOSTS.append(_suffix)
            _hosts_blob = " ".join(ALLOWED_HOSTS)
    for _key in ("RAILWAY_PUBLIC_DOMAIN", "RAILWAY_PRIVATE_DOMAIN"):
        _h = _normalize_allowed_host(os.environ.get(_key, ""))
        if _h and _h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(_h)
    # Platform health probes use this Host header; not the same as your public URL.
    _railway_health = "healthcheck.railway.app"
    if _railway_health not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_railway_health)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "inquiries",
    "cms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "helix_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "helix_backend.wsgi.application"

# Docker/Railway build runs collectstatic before deploy; DATABASE_URL may be missing a DB
# name at build time. This flag is set only in backend/railway.toml for that step.
_collectstatic_build = os.environ.get("DJANGO_COLLECTSTATIC_BUILD", "").lower() in (
    "1",
    "true",
    "yes",
)

# Railway / Postgres: prefer linked DATABASE_URL (private *.railway.internal). If you see
# "connection refused" to .railway.internal, Postgres may be down or private DNS not ready;
# set DJANGO_USE_PUBLIC_DATABASE=1 and reference Postgres DATABASE_PUBLIC_URL instead.
def _database_url_from_env() -> str:
    override = os.environ.get("DJANGO_DATABASE_URL", "").strip()
    if override:
        return override
    use_public = os.environ.get("DJANGO_USE_PUBLIC_DATABASE", "").lower() in (
        "1",
        "true",
        "yes",
    )
    if use_public:
        pub = os.environ.get("DATABASE_PUBLIC_URL", "").strip()
        if pub:
            return pub
    return os.environ.get("DATABASE_URL", "").strip()


_database_url = _database_url_from_env()
_on_railway = bool(os.environ.get("RAILWAY_ENVIRONMENT"))

if _collectstatic_build:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        },
    }
elif not _database_url:
    if _on_railway:
        raise ImproperlyConfigured(
            "DATABASE_URL is missing or empty. On Railway: create a PostgreSQL service, "
            "link it to this backend service (Variables → add reference to Postgres "
            "DATABASE_URL), and remove any blank DATABASE_URL override."
        )
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
else:
    _db = dj_database_url.parse(_database_url, conn_max_age=600)
    _engine = str(_db.get("ENGINE", ""))
    _opts = _db.get("OPTIONS") or {}
    _pg_name = (_db.get("NAME") or "").strip() or _opts.get("service")
    if "postgresql" in _engine and not _pg_name:
        # Railway sometimes exposes URLs without a path segment; linked Postgres also sets
        # PGDATABASE. The platform default database name is usually "railway".
        _db["NAME"] = (
            os.environ.get("PGDATABASE", "").strip()
            or os.environ.get("DJANGO_POSTGRES_DEFAULT_DB", "").strip()
            or "railway"
        )
    DATABASES = {"default": _db}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


def _cloudinary_credentials_ok() -> bool:
    if os.environ.get("CLOUDINARY_URL", "").strip():
        return True
    return all(
        os.environ.get(k, "").strip()
        for k in ("CLOUDINARY_CLOUD_NAME", "CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET")
    )


def _use_cloudinary_media() -> bool:
    """
    CMS uploads use Cloudinary when credentials are set, or when DJANGO_USE_CLOUDINARY=1
    (which requires credentials — avoids local /media/ disk on Railway).
    """
    want = os.environ.get("DJANGO_USE_CLOUDINARY", "").lower() in ("1", "true", "yes")
    ok = _cloudinary_credentials_ok()
    if want and not ok:
        raise ImproperlyConfigured(
            "DJANGO_USE_CLOUDINARY is enabled but Cloudinary credentials are missing. "
            "Set CLOUDINARY_URL, or CLOUDINARY_CLOUD_NAME + CLOUDINARY_API_KEY + "
            "CLOUDINARY_API_SECRET. Dashboard: https://console.cloudinary.com/"
        )
    # Forced Cloudinary mode, or auto when credentials are present (no local /media/ uploads).
    return True if want else ok


USE_CLOUDINARY_MEDIA = _use_cloudinary_media()

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if USE_CLOUDINARY_MEDIA
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
_media_root_env = os.environ.get("DJANGO_MEDIA_ROOT", "").strip()
MEDIA_ROOT = Path(_media_root_env) if _media_root_env else (BASE_DIR / "media")

# django-cloudinary-storage reads this when the MediaCloudinaryStorage backend loads.
# Credentials come from CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME / _API_KEY / _API_SECRET.
if USE_CLOUDINARY_MEDIA:
    CLOUDINARY_STORAGE = {
        "SECURE": True,
    }

# Public origin of this API (no path, no trailing slash), e.g. https://your-api.up.railway.app
# Used for absolute /media/... URLs in JSON when Next.js calls the API via a private host
# (Railway *.railway.internal) — request.build_absolute_uri() would otherwise point the
# browser at an unreachable URL.
def _django_public_base_url() -> str:
    explicit = os.environ.get("DJANGO_PUBLIC_BASE_URL", "").strip().rstrip("/")
    if explicit:
        return explicit
    # Railway sets this to the service's public hostname (no scheme), e.g. xxx.up.railway.app
    rd = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").strip()
    if not rd:
        return ""
    if rd.startswith(("http://", "https://")):
        return rd.split("?")[0].rstrip("/")
    host = rd.split("/")[0].replace("https://", "").replace("http://", "")
    return f"https://{host}"


DJANGO_PUBLIC_BASE_URL = _django_public_base_url()

# Behind Railway / reverse proxies (HTTPS).
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "true").lower() in (
        "1",
        "true",
        "yes",
    )
    # Platform health probes often call the container over HTTP without X-Forwarded-Proto;
    # a 301 to https makes the probe fail and the service restarts in a loop.
    if SECURE_SSL_REDIRECT:
        SECURE_REDIRECT_EXEMPT = [r"^/$", r"^/api/health/?$"]

_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [
        o.strip() for o in _csrf_origins.split(",") if o.strip()
    ]

# CORS — Next.js dev server and production
_cors = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
)
CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors.split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True

# Gmail SMTP (use App Password: https://support.google.com/accounts/answer/185833)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com").strip()
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "true").lower() in ("1", "true", "yes")
# Implicit TLS (e.g. port 465). If true, leave EMAIL_USE_TLS false in .env for typical Gmail 465 setups.
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "false").lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "").strip()
# Google App Passwords are 16 characters; the UI shows four groups with spaces—remove spaces.
EMAIL_HOST_PASSWORD = (
    os.environ.get("EMAIL_HOST_PASSWORD", "").strip().replace(" ", "")
)
# Avoid hanging on blocked SMTP (seconds; set 0 to use library default).
_email_timeout = os.environ.get("EMAIL_TIMEOUT", "30").strip()
EMAIL_TIMEOUT = int(_email_timeout) if _email_timeout.isdigit() else 30
DEFAULT_FROM_EMAIL = (
    os.environ.get("DEFAULT_FROM_EMAIL", "").strip()
    or EMAIL_HOST_USER
    or "noreply@helixprimesolutions.com"
)

CONTACT_RECIPIENT_EMAIL = (
    os.environ.get("CONTACT_RECIPIENT_EMAIL", "").strip()
    or EMAIL_HOST_USER
    or "info@helixprimesolutions.com"
)

# Quiet runserver: hide routine "GET … 200" lines. Set DJANGO_VERBOSE_HTTP=1 to see every request.
_DJANGO_VERBOSE_HTTP = os.environ.get("DJANGO_VERBOSE_HTTP", "").lower() in (
    "1",
    "true",
    "yes",
)
_DJANGO_SERVER_LOG_LEVEL = logging.INFO if _DJANGO_VERBOSE_HTTP else logging.WARNING


def _skip_client_disconnect_noise(record):
    """
    Next.js (parallel SSR fetches, Fast Refresh) and browsers often close sockets
    before the dev server finishes writing — harmless; Django logs it as 'Broken pipe'.
    """
    try:
        msg = record.getMessage()
    except Exception:
        return True
    if "Broken pipe" in msg:
        return False
    if "Connection reset by peer" in msg:
        return False
    return True


# Same structure as django.utils.log.DEFAULT_LOGGING, plus filter on django.server only.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "skip_client_disconnect": {
            "()": "django.utils.log.CallbackFilter",
            "callback": _skip_client_disconnect_noise,
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": _DJANGO_SERVER_LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "django.server",
            "filters": ["skip_client_disconnect"],
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": _DJANGO_SERVER_LOG_LEVEL,
            "propagate": False,
        },
        "inquiries": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
