# config/settings/production.py
from .base import *
import dj_database_url

DEBUG = False


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") + [
    ".railway.app",
    os.environ.get("RAILWAY_STATIC_URL", ""),
]


# Basic security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    os.environ.get("FRONTEND_URL", "https://djangify.railway.app"),
    "http://localhost:3000",
] + [f"https://{host}" for host in ALLOWED_HOSTS if host]

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://djangify.railway.app")


# Storage configuration

# Storage configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }
}

# WhiteNoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True

