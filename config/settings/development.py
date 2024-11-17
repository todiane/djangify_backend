# config/settings/development.py
import dj_database_url
from .base import *



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

    
# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

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
