#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=config.settings

echo "Initializing Django application..."

# Create directories
mkdir -p media/portfolio media/summernote staticfiles static apps/*/migrations

python manage.py makemigrations --noinput
python manage.py migrate --noinput --force-color
python manage.py collectstatic --noinput
python manage.py check --database default

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --threads 2 \
    --timeout 120
    