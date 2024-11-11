# config/settings/logging.py

import os
from pathlib import Path

# Get the project root directory (keep your existing BASE_DIR and LOGS_DIR setup)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Common logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
        "performance": {
            "format": "{asctime} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGS_DIR / "error.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 90,  # 90 days retention
            "formatter": "verbose",
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGS_DIR / "info.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,  # 30 days retention
            "formatter": "simple",
        },
        "file_security": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGS_DIR / "security.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 90,  # 90 days retention
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
        },
        "performance_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGS_DIR / "performance.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "formatter": "performance",
        },
        "api_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOGS_DIR / "api.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_info"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file_error", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file_security", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {  # Your application logs
            "handlers": ["console", "file_info", "file_error"],
            "level": "INFO",
            "propagate": True,
        },
        "performance": {
            "handlers": ["performance_file"],
            "level": "INFO",
            "propagate": False,
        },
        "api": {
            "handlers": ["api_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
