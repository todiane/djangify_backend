# config/settings/production.py
from .base import *

DEBUG = False

# Database Configuration
DATABASE_URL = os.environ.get('DATABASE_PRIVATE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
    
    # Updated database options with correct PostgreSQL settings
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5,
        'connect_timeout': 30,
    }



ALLOWED_HOSTS = ['djangify.up.railway.app','djangifybackend.up.railway.app']

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
