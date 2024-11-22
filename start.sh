#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=config.settings

echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -m django --version)"
echo "Environment: $DJANGO_SETTINGS_MODULE"

mkdir -p media/portfolio media/summernote staticfiles static

python manage.py collectstatic --noinput
python manage.py check --database default
python manage.py migrate --noinput --force-color

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

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 2 \
    --timeout 120
    