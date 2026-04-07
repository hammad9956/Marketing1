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
| `DATABASE_URL` | Yes (production) | Injected automatically when Postgres is **linked** to this service. |
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

**Railway-specific (optional):**

- `RAILWAY_ENVIRONMENT` — set automatically by Railway; enables `.up.railway.app` in `ALLOWED_HOSTS` when appropriate.
- `DJANGO_MEDIA_ROOT` — if you attach a **volume**, set this to the mount path (e.g. `/data/media`) so CMS uploads persist across deploys.
- `DJANGO_SECURE_SSL_REDIRECT` — default is on when `DEBUG` is false; set to `false` only if you debug redirect issues behind a proxy.

After the first deploy, run migrations if needed (the **Procfile** / `railway.toml` start command runs `migrate` automatically).

**Create superuser** (one-off): Railway → backend service → **Shell**:

```bash
python manage.py createsuperuser
```

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
