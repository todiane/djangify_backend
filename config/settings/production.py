# config/settings/production.py
from .base import *


DEBUG = False

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") + [
    ".railway.app",
    os.environ.get("RAILWAY_STATIC_URL", ""),
]

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
        OPTIONS={
            "sslmode": "require",
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
    )
}

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
