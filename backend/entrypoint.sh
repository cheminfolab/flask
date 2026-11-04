#!/bin/sh
# Stop at the first failing step: never start the server on a half-migrated database.
set -e

# Migrations are generated, not committed (see README "Database migrations").
python /app/manage.py makemigrations --noinput
python /app/manage.py migrate --noinput
python /app/manage.py ensure_superuser
python /app/manage.py loaddata units.json
python /app/manage.py collectstatic --noinput

# exec: gunicorn becomes PID 1 and receives the container's stop signal
exec gunicorn api.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
