# config/settings/production.py
from .base import *
import dj_database_url
    
DEBUG = False
ALLOWED_HOSTS = ['djangify.up.railway.app','djangify.com','djangifybackend.up.railway.app']  

# Production database settings
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )
}

# Production allowed hosts
ALLOWED_HOSTS = [
    "djangify.up.railway.app",
    "djangifybackend.up.railway.app",
]


# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'


# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://djangify.up.railway.app",
    "https://djangifybackend.up.railway.app",
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://djangify.up.railway.app",
    "https://djangifybackend.up.railway.app",
]

CORS_ALLOW_CREDENTIALS = True

# Frontend URL
FRONTEND_URL = "https://djangify.up.railway.app"

# WhiteNoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True

# Ensure static files are properly handled
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"