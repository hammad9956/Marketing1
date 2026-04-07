# Deploy on Railway (Helix Prime marketing site)

This repo has **two** deployables: **Django API** (`backend/`) and **Next.js** (`frontend/`). Create **two Railway services** from the same GitHub repo and set each service’s **Root Directory** accordingly.

## 1. Create services

1. **Postgres** (Railway template): add a **PostgreSQL** database. Railway injects `DATABASE_URL` into linked services.
2. **Backend** (Django): New service → same repo → **Root Directory** = `backend`. Link the Postgres plugin so `DATABASE_URL` is available.
3. **Frontend** (Next.js): New service → same repo → **Root Directory** = `frontend`.

Deploy **backend** first so you have its public URL for the frontend build.

## 2. Backend environment variables

Set these in the **backend** service (Railway → Variables).

| Variable | Required | Example / notes |
|----------|----------|-----------------|
| `DATABASE_URL` | Yes (production) | Injected when Postgres is **linked** to this service. Do **not** add an empty `DATABASE_URL` variable (it overrides the reference and breaks migrate with “supply the NAME”). Use **Variables → Reference** → `${{Postgres.DATABASE_URL}}` (name may vary). The image **build** runs `collectstatic` with `DJANGO_COLLECTSTATIC_BUILD=1` so a partial URL during build does not need a database name. If the URL has **no database path**, Django falls back to **`PGDATABASE`** (set by Railway) or **`railway`** (Railway’s default DB name). Override with **`DJANGO_POSTGRES_DEFAULT_DB`** if your DB has another name. |
| `DATABASE_PUBLIC_URL` | Optional | Shown on the **Postgres** service (public TCP). Use only if you set **`DJANGO_USE_PUBLIC_DATABASE=1`** on the backend (see troubleshooting below). |
| `DJANGO_USE_PUBLIC_DATABASE` | Optional | Set to `1` to connect via **`DATABASE_PUBLIC_URL`** instead of private `DATABASE_URL` when private networking returns **connection refused**. |
| `DJANGO_DATABASE_URL` | Optional | If set, **overrides** both URLs (paste a full `postgresql://…` for debugging). |
| `DJANGO_SECRET_KEY` | Yes | Long random string (50+ chars). |
| `DJANGO_DEBUG` | Yes | `false` in production. |
| `DJANGO_ALLOWED_HOSTS` | Yes | Your backend hostname(s), comma-separated, **no** `https://`. Example: `your-api.up.railway.app` |
| `CORS_ALLOWED_ORIGINS` | Yes | Your **frontend** public URL(s), comma-separated, **with** `https://`. Example: `https://your-app.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | Yes | Same as CORS for Django admin over HTTPS: `https://your-api.up.railway.app` (and frontend URL if you ever POST from browser to Django with cookies). |
| `EMAIL_HOST` | For contact form | e.g. `smtp.gmail.com` |
| `EMAIL_PORT` | Optional | `587` (TLS) or `465` (SSL) |
| `EMAIL_USE_TLS` | Optional | `true` with port 587 |
| `EMAIL_USE_SSL` | Optional | `true` with port 465 (then set `EMAIL_USE_TLS=false`) |
| `EMAIL_HOST_USER` | For contact form | Gmail address or SMTP user |
| `EMAIL_HOST_PASSWORD` | For contact form | App password / SMTP password |
| `DEFAULT_FROM_EMAIL` | Recommended | Usually same as `EMAIL_HOST_USER` |
| `CONTACT_RECIPIENT_EMAIL` | Optional | Inbox that receives inquiries |
| `DJANGO_SUPERUSER_EMAIL` | Optional | With `DJANGO_SUPERUSER_PASSWORD`, creates the **first** Django admin on deploy (`python manage.py ensure_superuser`). Ignored if any superuser already exists. |
| `DJANGO_SUPERUSER_PASSWORD` | Optional | Strong password for that admin (store only in Railway Variables). |
| `DJANGO_SUPERUSER_USERNAME` | Optional | Defaults to the email if omitted. |

**Railway-specific (optional):**

- `RAILWAY_ENVIRONMENT` — set automatically by Railway; enables `.up.railway.app` in `ALLOWED_HOSTS` when appropriate.
- `DJANGO_MEDIA_ROOT` — if you attach a **volume**, set this to the mount path (e.g. `/data/media`) so CMS uploads persist across deploys.
- `DJANGO_SECURE_SSL_REDIRECT` — default is on when `DEBUG` is false; set to `false` only if you debug redirect issues behind a proxy.

After the first deploy, run migrations if needed (the **Procfile** / `railway.toml` start command runs `migrate` automatically).

**Admin user:** Set `DJANGO_SUPERUSER_EMAIL` and `DJANGO_SUPERUSER_PASSWORD` in Variables; each deploy runs `ensure_superuser` and creates an admin **only if no superuser exists yet**. Or run manually in **Shell**: `python manage.py createsuperuser`.

### Public URL not showing (backend)

1. Latest deploy must be **successful** (migrate + gunicorn running). Check **Deployments → Logs** for errors.
2. **Settings → Networking → Public networking** → generate a domain. **Target port** must match the port the app listens on. This project binds to **`${PORT:-8080}`** — Railway usually sets **`PORT`** (often `8080`). Use that value.
3. If the service **starts then stops**, check **Settings → Health check** (if present): path **`/`** or **`/api/health/`**, same port as the app (**8080** by default). This project returns **`{"ok": true}`** for both **`/`** and **`/api/health/`**.
4. **Gunicorn `[INFO]` lines labeled `[error]` in Railway** are normal — Gunicorn logs to stderr.

## 3. Frontend environment variables

Set these in the **frontend** service. **`NEXT_PUBLIC_*` must be present before `npm run build`** — set variables, then **Redeploy** so the build picks them up.

| Variable | Required | Example / notes |
|----------|----------|-----------------|
| `NEXT_PUBLIC_API_URL` | Yes | Public **backend** base URL, **no** trailing slash: `https://your-api.up.railway.app` |
| `NEXT_PUBLIC_SITE_URL` | Yes | Public **frontend** URL: `https://your-app.up.railway.app` |
| `NEXT_PUBLIC_CONTACT_EMAIL` | Recommended | Shown in footer / contact UI |
| `NEXT_PUBLIC_INFO_EMAIL` | Optional | Second line if different from contact |
| `CMS_API_URL` | Optional | Defaults to `NEXT_PUBLIC_API_URL`. Use if server-side fetches need a different base (rare on Railway). |
| `NODE_ENV` | Automatic | Railway sets `production` for deploys. |

Optional: social links, Tawk, etc. — see `frontend/.env.example`.

**Frontend build fails with `EBUSY` / `rmdir ... node_modules/.cache`:** Railway mounts a cache at that path; `npm ci` can conflict with it. This repo’s `frontend/railway.toml` uses `npm install` instead. If it still fails, add a service variable **`NIXPACKS_NO_CACHE=1`** (disables Nixpacks build caches; slower but reliable).

**Frontend logs: `npm error signal SIGTERM` / `command sh -c next start`:** Usually **normal** — Railway sends **SIGTERM** when **replacing** the container (new deploy) or stopping the service. It is not necessarily an app crash. If the site **never** loads, check **Networking** target port matches **`PORT`** (often **8080**) and that the latest deploy **succeeded**. This repo starts with `exec next start -H 0.0.0.0 -p $PORT` so the server binds correctly without going through `npm start` on Railway.

**Next.js “Ready” then “Stopping Container” a few seconds later:** The home page **`/`** server-renders and **fetches Django**. If the health probe hits **`/`** while the API is slow or down, the check can fail. `frontend/railway.toml` sets **`healthcheckPath = "/health"`** (a static JSON route that does **not** call CMS). In the Railway UI, if you override the health check, point it to **`/health`** (or clear overrides so config-as-code applies).

### Postgres “connection refused” to `*.railway.internal`

That host is Railway’s **private** network. Refused usually means:

1. **Postgres isn’t running** — open the Postgres service in Railway; ensure it’s deployed and healthy (not crashed or sleeping on a free tier).
2. **Backend and Postgres are in the same project** and the backend **references** that Postgres `DATABASE_URL` (not an old/copied URL from another project).
3. **Race on first boot** — redeploy backend after Postgres is healthy.

**Workaround:** On the **backend** service add variable **`DJANGO_USE_PUBLIC_DATABASE=1`** and a **reference** to the Postgres service’s **`DATABASE_PUBLIC_URL`** (in addition to or instead of private `DATABASE_URL`, depending how you name variables — the code prefers `DATABASE_PUBLIC_URL` when the flag is set). Public URL uses TLS; Django/psycopg2 will use `sslmode` from the URL if present.

## 4. Postgres and uploads

- **Database:** Link Postgres to the backend service so `DATABASE_URL` is set; do not rely on SQLite on Railway for production.
- **Media / CMS images:** Ephemeral disk resets on redeploy unless you add a **volume** and set `DJANGO_MEDIA_ROOT` to that path (or use external object storage later).

## 5. Email (contact form) not sending

The form **always saves** the row in Django (`Inquiry`). Mail is separate.

1. **Backend must have** `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` set (Gmail: use an [App Password](https://support.google.com/accounts/answer/185833), not your normal login password).
2. **`CONTACT_RECIPIENT_EMAIL`** is the team inbox that receives each inquiry. The submitter also gets a **confirmation email** at the address they typed, unless it is the same address as the team inbox (to avoid duplicate mail to `info@…`).
3. The team email includes **Reply-To** set to the visitor’s address so you can reply from your mail client in one step.
4. From the backend shell (local or Railway **Shell**), run:

   ```bash
   python manage.py test_contact_email
   ```

   If this fails, fix SMTP variables before testing the website again. If it succeeds but you see nothing, check **spam** and the recipient address.
5. **Browser shows “Network error or timeout”** — the browser never reached Django (wrong `NEXT_PUBLIC_API_URL`, CORS, or backend down). That is not an SMTP problem.
6. **Browser shows “We could not send your message…”** — Django ran but `send_mail` failed (bad password, blocked port, etc.). With `DJANGO_DEBUG=true`, the JSON response may include `smtp_error` in development.

## 6. Custom domains

Point DNS at Railway, then add the custom host to `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, and update `NEXT_PUBLIC_SITE_URL` and `NEXT_PUBLIC_API_URL` as needed. Redeploy **frontend** after changing `NEXT_PUBLIC_*`.
