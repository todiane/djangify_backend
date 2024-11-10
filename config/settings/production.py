# config/settings/production.py
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Database configuration
database_url = os.environ.get("DATABASE_PUBLIC_URL") or os.environ.get("DATABASE_URL")

# If we have explicit Postgres settings, use those instead
if all(
    [
        os.environ.get("PGUSER"),
        os.environ.get("PGPASSWORD"),
        os.environ.get("PGHOST"),
        os.environ.get("PGPORT"),
        os.environ.get("PGDATABASE"),
    ]
):
    database_url = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get("PGUSER"),
        os.environ.get("PGPASSWORD"),
        os.environ.get("PGHOST"),
        os.environ.get("PGPORT"),
        os.environ.get("PGDATABASE"),
    )

DATABASES = {
    "default": dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

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
