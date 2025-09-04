"""
Production settings for Render deployment
"""
import os
from .base import *

# Safe import for production dependencies
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Security
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here-change-this")

# Hosts - configurable from environment
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "ecomtech.onrender.com,*.onrender.com,localhost,127.0.0.1").split(",")

# CSRF and CORS - configurable from environment
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "https://ecomtech.onrender.com").split(",")

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "https://ecomtech.onrender.com,http://localhost:3000").split(",")

CORS_ALLOW_CREDENTIALS = True

# URLs with safe defaults
BACKEND_URL = os.environ.get("BACKEND_URL", "https://ecomtech.onrender.com")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://ecomtech.onrender.com")

# Database - PostgreSQL for Render
if os.environ.get("DATABASE_URL") and dj_database_url:
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
else:
    # Fallback to SQLite for development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# WhiteNoise for static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# PayPal Configuration with safe defaults
PAYPAL_SETTINGS = {
    "CLIENT_ID": os.environ.get("PAYPAL_CLIENT_ID", ""),
    "CLIENT_SECRET": os.environ.get("PAYPAL_CLIENT_SECRET", ""),
    "BASE_URL": os.environ.get("PAYPAL_BASE_URL", "https://api-m.sandbox.paypal.com"),
    "SANDBOX": os.environ.get("PAYPAL_SANDBOX", "True").lower() == "true",
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "apps": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
