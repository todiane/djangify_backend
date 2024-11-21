#!/bin/bash

# Exit on error
set -e

# Debug information
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -m django --version)"
echo "Environment: $DJANGO_SETTINGS_MODULE"

# Create necessary directories
mkdir -p media/portfolio media/summernote staticfiles static

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Test database connection
echo "Testing database connection..."
python manage.py check --database default

# Create migrations for all apps
echo "Creating migrations..."
python manage.py makemigrations django_summernote --noinput
python manage.py makemigrations --noinput

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput --force-color

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    try:
        User.objects.create_superuser(
            username='${DJANGO_SUPERUSER_USERNAME:-admin}',
            email='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
            password='${DJANGO_SUPERUSER_PASSWORD:-admin}'
        )
        print("Superuser created successfully")
    except Exception as e:
        print(f"Error creating superuser: {e}")
else:
    print("Superuser already exists")
EOF

# Start Gunicorn with debug logging
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance \
    --log-level debug
    