# config/settings/production.py
from .base import *
import dj_database_url
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("django.db.backends")
logger.setLevel(logging.DEBUG)

DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Database configuration with additional options
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # Replace postgres:// with postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    DATABASES = {
        "default": {
            **dj_database_url.config(
                default=database_url,
                conn_max_age=60,  # 60 second connection lifetime
                ssl_require=True,  # Enable SSL
            ),
            "OPTIONS": {
                "connect_timeout": 30,  # Increased from 10 to 30 seconds
                "keepalives": 1,
                "keepalives_idle": 60,  # Increased from 30 to 60 seconds
                "keepalives_interval": 10,
                "keepalives_count": 5,
                "sslmode": "require",  # Enforce SSL
            },
        }
    }
else:
    raise Exception("DATABASE_URL environment variable is not set!")

# Security settings (existing settings remain the same)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CORS settings for production (existing settings remain the same)
CORS_ALLOWED_ORIGINS = [
    os.environ.get("FRONTEND_URL", "https://djangify_frontend.railway.app"),
    "https://djangify.com",
    "https://www.djangify.com",
    "http://localhost:3000",
]
