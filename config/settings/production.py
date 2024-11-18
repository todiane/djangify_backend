# config/settings/production.py
from .base import *
import dj_database_url

DEBUG = False


ALLOWED_HOSTS = [
    "djangify.up.railway.app",
    "djangify.railway.app",
    "*railway.app",
    "djangify.com",
    "djangifybackend.railway.app"
]


# Basic security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    os.environ.get("FRONTEND_URL"),
    "https://djangify.up.railway.app",
    "http://localhost:3000",
    "https://djangify.com",
    "https://djangifybackend.up.railway.app"
]

FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://djangify.railway.app,https://djangify.com")


# WhiteNoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True

