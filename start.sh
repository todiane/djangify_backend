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

# Determine environment and configure database
if [[ "$DJANGO_SETTINGS_MODULE" == *"development"* ]]; then
    echo "Running in development environment with SQLite"
    # Ensure SQLite file is created with proper permissions
    touch db.sqlite3
    chmod 666 db.sqlite3
else
    echo "Running in production environment with PostgreSQL"
    # Test database connection
    python test_db_connection.py || {
        echo "Failed to connect to PostgreSQL database"
        exit 1
    }
fi

# Apply migrations
echo "Applying migrations..."
python manage.py makemigrations --force-color
python manage.py migrate --force-color

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME:-admin}',
        email='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        password='${DJANGO_SUPERUSER_PASSWORD:-admin}'
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF

# Start server based on environment
if [[ "$DJANGO_SETTINGS_MODULE" == *"development"* ]]; then
    echo "Starting development server..."
    python manage.py runserver 0.0.0.0:${PORT:-8000}
else
    echo "Starting Gunicorn..."
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:${PORT:-8000} \
        --workers 2 \
        --threads 2 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
        --log-level debug
fi