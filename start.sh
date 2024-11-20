#!/bin/bash

# Exit on error
set -e

# Debug information
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -m django --version)"
echo "Environment: $DJANGO_SETTINGS_MODULE"

# Create media directories
mkdir -p media/portfolio
mkdir -p media/summernote

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying migrations..."
python manage.py makemigrations --force-color
python manage.py migrate --force-color

# Add debug info for migrations
python manage.py showmigrations

# Check if superuser exists, if not, create one
echo "Checking for superuser..."
if [ -z "$(python manage.py shell -c 'from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())')" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
else
    echo "Superuser already exists."
fi

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug