import logging
import os
from pathlib import Path

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

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]
# Railway default hostname pattern (*.up.railway.app) when deploying there.
if os.environ.get("RAILWAY_ENVIRONMENT") and ".up.railway.app" not in " ".join(ALLOWED_HOSTS):
    ALLOWED_HOSTS.append(".up.railway.app")

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

# Railway / Postgres: non-empty DATABASE_URL from linked PostgreSQL. Empty or broken URLs
# (e.g. manual override to blank) yield Postgres config without NAME and crash migrate.
_database_url = os.environ.get("DATABASE_URL", "").strip()
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
        raise ImproperlyConfigured(
            "DATABASE_URL is set but PostgreSQL has no database name (and no OPTIONS['service']). "
            "Use the full connection string from Railway’s Postgres plugin (includes /railway or "
            "similar path), or fix a malformed DATABASE_URL. "
            "(Build-time collectstatic uses DJANGO_COLLECTSTATIC_BUILD=1 — see backend/railway.toml.)"
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

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "media/"
_media_root_env = os.environ.get("DJANGO_MEDIA_ROOT", "").strip()
MEDIA_ROOT = Path(_media_root_env) if _media_root_env else (BASE_DIR / "media")

# Behind Railway / reverse proxies (HTTPS).
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "true").lower() in (
        "1",
        "true",
        "yes",
    )

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
