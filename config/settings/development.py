# config/settings/development.py
import dj_database_url
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Ensure SSL redirect is disabled in development
SECURE_SSL_REDIRECT = False

# Ensure session cookies are not marked as secure in development
SESSION_COOKIE_SECURE = False



CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_COOKIE_SECURE = False  # Set to True in production
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'

# Frontend URL for development
FRONTEND_URL = "http://localhost:3000"  # Default development frontend URL

# Determine if PostgreSQL should be used locally
POSTGRES_LOCALLY = False  # Set to True to deploy to Railway or False tuse locally

# Database configuration
if os.environ.get('ENVIRONMENT') == 'production' or POSTGRES_LOCALLY:
    # Ensure the DATABASE_URL environment variable is set
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
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

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend development server
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]


LOGGING["loggers"]["django"]["level"] = "DEBUG"
LOGGING["loggers"]["apps"]["level"] = "DEBUG"
