#!/bin/sh

python /app/manage.py makemigrations --noinput
python /app/manage.py migrate --noinput
python /app/manage.py loaddata accounts.json
python /app/manage.py loaddata units.json
python /app/manage.py collectstatic --noinput

#python /app/manage.py runserver 0.0.0.0:8000
gunicorn api.wsgi:application --bind 0.0.0.0:8000
