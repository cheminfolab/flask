# Backend (Django)

Overview, configuration and the notebook rules are in the [main README](../README.md).
This file covers the local database, administration tasks and backups.

## Local PostgreSQL server (native development)

With the conda environment active, in `backend/`:

```bash
initdb -D database                       # once; `database/` is git-ignored
pg_ctl -D database -l logfile start      # start the server
createuser --encrypted --pwprompt admin  # database user (asks for a password)
createdb --owner=admin flask_database
```

Put the same user, password and database name into `.env`. Stop the server with
`pg_ctl -D database stop`.

## Schema and first user

```bash
python manage.py makemigrations   # migrations are generated, not committed (see main README)
python manage.py migrate
python manage.py createsuperuser
```

In Docker the container runs `ensure_superuser` on start: it creates a superuser from
`DJANGO_SUPERUSER_EMAIL` / `DJANGO_SUPERUSER_PASSWORD` only if no superuser exists, and never
changes existing accounts. There is no default admin account.

Self-registered accounts are inactive until an admin activates them (`/admin/` → *Members* → *Is active*).

## Useful commands

| Command | Purpose |
|---|---|
| `python manage.py test --parallel auto` | run the test suite (needs PostgreSQL) |
| `python manage.py check --deploy` | production settings check |
| `python manage.py spectacular --file ../openapi/schema.yml --validate --fail-on-warn` | regenerate the API schema after API changes (commit it) |
| `python manage.py ensure_superuser` | create the first superuser from the environment |

## Backups

A complete backup has two parts: the **database** and the **files** (substance images in `media/`,
experiment attachments in `private_media/`). Attachments are referenced by the database and verified
by their SHA-256 checksum, so back up both together.

Database (consistent snapshot while the application is running):

```bash
docker compose exec database pg_dump -U "$POSTGRES_USER" -Fc "$POSTGRES_DB" > flask_$(date +%F).dump
```

Files (Docker volumes):

```bash
docker run --rm -v flask_media:/media -v flask_private_media:/private_media -v "$PWD":/backup alpine \
  tar czf /backup/flask_files_$(date +%F).tar.gz /media /private_media
```

(Volume names are prefixed with the Compose project name, by default the directory name; check
with `docker volume ls`.)

Restore into an empty database with `pg_restore -U <user> -d <db> --clean --if-exists <file>.dump`
and unpack the file archive into the volumes. Test a restore before relying on a backup.

`manage.py dumpdata` is not a backup: it is not a consistent snapshot of a running system and
does not include files.
