# FLASK — electronic lab notebook and chemical inventory

FLASK records laboratory work (projects, experiments, procedures, observations,
results, attachments) next to a chemical inventory (substances, compounds,
containers, storage locations, GHS hazard data). Materials used in an
experiment are booked out of inventory containers through a ledger.

- [Architecture](#architecture)
- [Quick start with Docker](#quick-start-with-docker)
- [Configuration (`.env`)](#configuration-env)
- [Native development](#native-development)
- [Accounts](#accounts)
- [Notebook records: access and integrity](#notebook-records-access-and-integrity)
- [API documentation and the frontend contract](#api-documentation-and-the-frontend-contract)
- [Database migrations](#database-migrations)
- [Operations: health, logs, backups](#operations-health-logs-backups)
- [Testing](#testing)
- [Not yet covered](#not-yet-covered)

## Architecture

```
browser ── nginx :80 ─┬─ /             React SPA (built into the nginx image)
                      ├─ /api, /admin  Django + DRF (gunicorn, backend container)
                      ├─ /static, /media                    (public files)
                      └─ /protected-attachments  internal only, via X-Accel-Redirect
Django ── PostgreSQL 15 (database container)
backup container: daily pg_dump + file archive into the `backups` volume
```

| Path | Contents |
|---|---|
| `backend/api/` | settings, URLs, shared base classes (`BaseModelViewSet`, `TrackedModel`, permissions) |
| `backend/accounts/` | `Member` (email login), working groups, roles, registration |
| `backend/projects/` | notebook: projects, experiments, entries, shares, material ledger, attachments |
| `backend/chemicals/`, `ghs/`, `locations/` | inventory and reference data |
| `frontend/src/lib/api.ts` | the single API client (auth, token refresh, error messages) |
| `frontend/src/types/api.gen.ts` | TypeScript types generated from the OpenAPI schema |
| `openapi/schema.yml` | the API contract (generated, committed) |

Authentication uses JWT (`/api/token/`, 5-minute access tokens, rotating 1-day refresh tokens).
Every API endpoint requires login except token obtain/refresh and registration.

## Quick start with Docker

Prerequisite: Docker with Compose.

1. Create `.env` in the repository root (see below). At minimum set `SECRET_KEY`,
   `POSTGRES_PASSWORD`, `DJANGO_SUPERUSER_EMAIL` and `DJANGO_SUPERUSER_PASSWORD`.
2. Start everything (`--wait` returns once all health checks pass):

   ```bash
   docker compose up -d --build --wait
   ```

3. Open http://localhost/ and log in with the superuser. The Django admin is at http://localhost/admin/.

Upgrading from a checkout before November 2026: the stack no longer uses the `<project>_build`
volume or fixed container names (`eln_db`, `eln_backend`, `nginx`). Run
`docker compose up -d --build --remove-orphans` once; `docker volume rm flask_build` removes the
unused volume. The database volume is unchanged.

Stop with `docker compose down` (add `-v` only if you want to delete the database and files).

## Configuration (`.env`)

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SECRET_KEY` | yes | — | Django secret key (long and random) |
| `POSTGRES_PASSWORD` | yes | — | database password |
| `POSTGRES_DB`, `POSTGRES_USER` | | `flask_database`, `admin` | database name and user |
| `POSTGRES_HOST`, `POSTGRES_PORT` | | `127.0.0.1`, `5432` | set by Compose for the backend container |
| `DEBUG` | | `False` | never `True` on a shared server: error pages expose internals |
| `ALLOWED_HOSTS` | | `127.0.0.1` | comma-separated host names the site is served under |
| `TIME_ZONE` | | `UTC` | e.g. `Europe/Berlin` |
| `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` | first start | — | first superuser, created only if none exists |
| `CORS_ALLOWED_ORIGINS` | | empty | full origins incl. scheme, e.g. `https://eln.example.org` (only needed if the SPA is served from another origin) |
| `CORS_ALLOW_ALL_ORIGINS` | | `False` | development only |
| `HTTPS` | | `False` | set `True` once nginx terminates TLS (SSL redirect, secure cookies) |
| `SECURE_HSTS_SECONDS` | | `0` | HSTS max-age when `HTTPS=True`, e.g. `31536000` |
| `ATTACHMENT_MAX_SIZE_MB` | | `100` | upload limit; keep nginx `client_max_body_size` at least as large |
| `PRIVATE_MEDIA_ROOT` | | `backend/private_media` | where attachment files are stored |
| `THROTTLE_LOGIN`, `THROTTLE_TOKEN_REFRESH`, `THROTTLE_REGISTER` | | `10/minute`, `60/minute`, `5/hour` | request limits per client address |
| `NUM_PROXIES` | | `1` | proxies in front of Django (nginx); used to find the real client address |
| `GUNICORN_WORKERS`, `GUNICORN_TIMEOUT` | | `3`, `120` | application server processes and request timeout (s) |
| `LOG_LEVEL` | | `INFO` | application log level |
| `BACKUP_TIME`, `BACKUP_KEEP_DAYS`, `BACKUP_ON_START` | | `02:30`, `14`, `true` | daily backup time (in `TIME_ZONE`), retention, backup at container start |
| `HTTP_PORT`, `DB_PORT`, `BACKEND_PORT` | | `80`, `5432`, `8000` | host ports (database and backend on `127.0.0.1` only) |
| `ENV_FILE` | | `.env` | env file used by Compose (set in the shell, e.g. for a second test stack) |

The database (5432) and backend (8000) ports are published on `127.0.0.1` only; external traffic goes through nginx.

## Native development

Prerequisites: conda (or Python 3.12 + Node 22), a PostgreSQL 15+ server.

```bash
conda env create -f environment.yml     # Python deps from backend/requirements.txt, Node 22, PostgreSQL 15
conda activate flask

cd backend
python manage.py makemigrations          # see "Database migrations"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver               # http://127.0.0.1:8000

cd ../frontend
npm ci
npm run dev                              # http://localhost:3000, proxies /api to :8000
```

See [backend/README.md](backend/README.md) for setting up a local PostgreSQL server and backups,
and [frontend/README.md](frontend/README.md) for frontend scripts.

## Accounts

- There is **no default admin account**. The first superuser comes from `DJANGO_SUPERUSER_*`
  (Docker) or `manage.py createsuperuser`.
- Self-registration (`/signup`) creates **inactive** accounts. An admin activates them in the Django
  admin (*Members* → *Is active*). Working group and roles are assigned by admins only.
- Admins can read all notebook records but cannot edit or delete them, also not in the Django admin.

## Notebook records: access and integrity

**Structure:** Project → Experiment → Entries (procedure, observation, result, note, correction),
plus materials booked from inventory containers and attached files.

**Who can see and change an experiment**

| | read | edit |
|---|---|---|
| author | ✓ | ✓ |
| members of the author's working group | ✓ | |
| project owner | ✓ | |
| members the experiment or its project is shared with (read / edit) | ✓ | edit shares only |
| admins | ✓ | |

Only the author completes an experiment and manages its shares; only the project owner manages
project shares. An edit share on a project also allows creating experiments in it.

**Integrity rules**

- Authorship (`created_by`, `updated_by`) and timestamps are set by the server.
- Every change, including deletions, is kept in history tables (visible in the Django admin).
- Experiments are never deleted through the API.
- **Completing** an experiment locks it: fields, entries, materials and attachments become read-only.
  Later changes are added as **correction** entries that reference the corrected entry and state a reason.
- Booking material decrements the container's remaining amount (in the container's unit; no
  conversion). Deleting a booking in a draft restores it.
- Attachments are stored outside the public media directory with a SHA-256 checksum and served only
  after the same read check, always as a download.

## API documentation and the frontend contract

- Interactive docs: http://localhost/api/docs/ (admins; log in at `/admin/` first). Schema: `/api/schema/`.
- `openapi/schema.yml` is generated from the backend and committed. The frontend types are generated from it:

  ```bash
  cd backend && python manage.py spectacular --file ../openapi/schema.yml --validate --fail-on-warn
  cd ../frontend && npm run gen:api
  ```

  CI fails if either file is out of date, so a backend change that alters the API must come with
  both regenerated files.

## Database migrations

Migration files are **not committed** (`backend/*/migrations/0*.py` is git-ignored): they are generated
from the models, also by the container on start (`makemigrations` then `migrate`). This is a deliberate
choice while no database holds data that must be kept. Before the first production database, start
committing migrations and remove `makemigrations` from `backend/entrypoint.sh`.

## Operations: health, logs, backups

**Health.** `GET /api/health/` returns `{"status": "ok"}` (200) when Django reaches the database,
503 otherwise; it needs no login and reveals nothing else. Every container has a health check
(`docker compose ps`); nginx's check covers the whole chain nginx → Django → PostgreSQL.
The backup container turns unhealthy when the last successful backup is older than 26 hours.

**Logs.** `docker compose logs -f backend` shows one JSON object per line. Every response carries an
`X-Request-ID` header; nginx logs the same id (`rid=`), so a request can be followed through both.
Failed logins are logged as `login_failed` with the client address, never with the email or password.
Logs stay on the server; no external monitoring service is used.

**Rate limits.** Login, token refresh and registration are throttled per client address
(see `THROTTLE_*`); excess requests get 429.

**Pagination.** All list endpoints return `{"count", "next", "previous", "results"}`;
use `?page=` and `?page_size=` (at most 500).

**Backups.** The `backup` service writes a backup at `BACKUP_TIME` every day (and at start) to the
`backups` volume and keeps `BACKUP_KEEP_DAYS` days. Each backup is a folder with `database.dump`
(pg_dump), `files.tar.gz` (images and attachments) and `SHA256SUMS`. A backup on the same disk does not
protect against losing that disk: copy the folders off the server regularly, e.g.

```bash
docker compose cp backup:/backups ./offsite-copy     # then move ./offsite-copy elsewhere
```

Run a backup right now with `docker compose exec backup sh /scripts/backup.sh`.

**Restore.**

```bash
scripts/restore.sh --list                      # available backups and the last success
scripts/restore.sh 2026-11-04T023000Z --yes    # replaces ALL data with that backup
```

The script stops the application, verifies the checksums, restores database and files, starts the
application again and runs `manage.py verify_attachments`, which checks every attachment against the
checksum recorded at upload. To restore an off-site copy, copy its folder into the volume first
(`docker compose cp ./2026-11-04T023000Z backup:/backups/`).

`scripts/e2e.sh` runs a complete backup → change → restore cycle against a throwaway stack (CI does
this on every push).

## Testing

Backend (needs a PostgreSQL 15+ server; the runner creates and drops its own `test_*` database):

```bash
cd backend
POSTGRES_HOST=localhost POSTGRES_PORT=5432 POSTGRES_USER=<user> POSTGRES_PASSWORD=<password> \
  python manage.py test --parallel auto
```

Frontend:

```bash
cd frontend
npm test          # unit tests (Vitest)
npm run lint
npm run build     # type-check and production build
```

End to end (builds the images and runs a separate, throwaway stack; needs Docker):

```bash
ENV_FILE=<test env file> COMPOSE_PROJECT_NAME=flask-e2e HTTP_PORT=8088 sh scripts/e2e.sh
```

The env file needs at least `SECRET_KEY`, `POSTGRES_PASSWORD` and `DJANGO_SUPERUSER_EMAIL`/`_PASSWORD`.

CI (`.github/workflows/ci.yml`) runs all of this, plus the schema and type drift checks, on every push and pull request.

## Not yet covered

- TLS in the nginx configuration (settings are ready: `HTTPS=True`); deliberately left to an upstream proxy for now.
- Automatic off-site copies of backups (copy them off the server yourself, see above).
- Frontend pages for experiments, entries and attachments (the API is complete; the Projects page lists and creates projects).
