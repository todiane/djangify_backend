from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Logs directory
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database configuration - comment out local database and set debug to false in production. For local use comment out production database and set debug to true.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') or [
    'djangifybackend.up.railway.app',
    'djangify.up.railway.app',
    '.up.railway.app',
    'djangifybackend-production.up.railway.app',
    'djangify-production.up.railway.app',
    '127.0.0.1',
    '0.0.0.0'
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "corsheaders",
    "django_filters",
    "whitenoise.runserver_nostatic",
    "cloudinary",
    "cloudinary_storage",
    'django_ckeditor_5',
    # Local apps
    "apps.core.apps.CoreConfig",
    "apps.portfolio.apps.PortfolioConfig",
]

MIDDLEWARE = [
    "apps.core.middleware.ErrorHandlingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Security settings
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Static and media files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Update Cloudinary storage settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'MEDIA_TAG': 'media',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
    'INVALID_IMAGE_ERROR_MESSAGE': 'Please upload a valid image file.',
    'STATIC_TAG': 'static',
}


DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# CORS settings
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "https://djangify.up.railway.app",
        "https://djangifybackend.up.railway.app",
    ]

CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "https://djangify.up.railway.app",
    "https://djangifybackend.up.railway.app",
]

if DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ])


# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "ORDERING_PARAM": "ordering",
}

# Image settings
PORTFOLIO_IMAGE_SIZE = (1200, 800)
PORTFOLIO_GALLERY_IMAGE_SIZE = (1200, 800)
PORTFOLIO_IMAGE_QUALITY = 85

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# In settings.py, add after the existing configurations

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'error_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_DIR / 'error.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        'portfolio_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_DIR / 'portfolio.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'simple',
            'level': 'INFO',
        },
        'security_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_DIR / 'security.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'cloudinary_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOGS_DIR / 'cloudinary.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.portfolio': {
            'handlers': ['portfolio_file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'cloudinary': {
            'handlers': ['cloudinary_file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
# CKEditor configuration settings 

CKEDITOR_5_UPLOAD_PATH = "uploads/"

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
        'height': '300px',
        'width': '100%',
    },
}

CKEDITOR_5_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'