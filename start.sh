#!/bin/bash

# Make script exit on first error
set -e

# Create media directories if they don't exist
mkdir -p media/blog
mkdir -p media/portfolio
mkdir -p media/summernote

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --log-level info 
