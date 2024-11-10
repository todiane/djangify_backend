# config/settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Frontend URL for development
FRONTEND_URL = "http://localhost:3000"  # Default development frontend URL

# Database configuration with fallbacks
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "djangify_backend"),
        "USER": os.environ.get("DATABASE_USER", "djangifybe_user"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", ""),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
