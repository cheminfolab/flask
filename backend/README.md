# Backend (Django)

Overview, configuration and the notebook rules are in the [main README](../README.md).
This file covers the local database, administration tasks and backups.

## Local PostgreSQL server (native development)

The simplest database for development is the Compose service: `docker compose up -d database`
(listens on `127.0.0.1:5432`, user, password and database from `.env`).

Without Docker, use any PostgreSQL 15+ installation, for example from conda-forge
(`conda install -c conda-forge postgresql=15` in your environment). Then, in `backend/`:

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
| `python manage.py verify_attachments` | check every attachment file against its recorded SHA-256 |

## Backups

In Docker, the `backup` service backs up the database and all files daily, and `scripts/restore.sh`
restores them. See "Operations: health, logs, backups" in the [main README](../README.md).

After any restore, check the attachments against their recorded checksums:

```bash
python manage.py verify_attachments
```

For a native setup without Docker, back up both parts together:

```bash
pg_dump -Fc -U <user> <db> > flask.dump        # database
tar czf flask_files.tar.gz media private_media  # images and attachments
```

`manage.py dumpdata` is not a backup: it is not a consistent snapshot of a running system and
does not include files.
