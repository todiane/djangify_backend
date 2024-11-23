#!/bin/bash

# Enable error handling and command printing
set -e
set -x

echo "==============================================="
echo "Starting Django Deployment Process $(date)"
echo "==============================================="

# Log environment information
echo "Environment Details:"
echo "Python Version: $(python --version)"
echo "Current Directory: $(pwd)"
echo "Django Settings Module: $DJANGO_SETTINGS_MODULE"
echo "Database URL Check: ${DATABASE_URL:0:20}..." # Show only beginning for security

# Create necessary directories with verbose output
echo "Creating required directories..."
mkdir -p media/portfolio media/summernote staticfiles static
echo "Directories created successfully"

# Test database connection
echo "Testing database connection..."
python << END
import django
from django.conf import settings
from django.db import connections
django.setup()
db = connections['default']
try:
    c = db.cursor()
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {str(e)}")
    raise
END

# Collect static files with detailed output
echo "Collecting static files..."
python manage.py collectstatic --noinput -v 2

# Run migrations with detailed output
echo "Running database migrations..."
python manage.py migrate --noinput --force-color -v 2

# Check for superuser
echo "Checking for superuser..."
python << END
import django
django.setup()
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
END

echo "==============================================="
echo "Starting Gunicorn $(date)"
echo "==============================================="

# Start Gunicorn with enhanced logging
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output \
    --enable-stdio-inheritance