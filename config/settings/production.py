# config/settings/production.py
from .base import *


DEBUG = False
ALLOWED_HOSTS = ['djangify.up.railway.app','djangify.com','djangifybackend.up.railway.app']  

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PGDATABASE', 'railway'),
        'USER': os.getenv('PGUSER', 'postgres'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST', 'postgres.railway.internal'),
        'PORT': os.getenv('PGPORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# Database connection settings
CONN_MAX_AGE = 60
CONN_HEALTH_CHECKS = True

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

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET')
}

# Media files
MEDIA_URL = "media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Static files
STATIC_URL = "/static/"
STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
