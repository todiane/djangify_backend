# config/settings/production.py
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Database
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    os.environ.get("FRONTEND_URL", "https://djangify_frontend.railway.app"),
    "https://djangify.com",  # Your future production frontend
    "https://www.djangify.com",
    "http://localhost:3000",  # For Next.js local development
]
