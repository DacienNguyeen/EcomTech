"""
Production settings for Render deployment
"""
import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your Render domain and Vercel domain
ALLOWED_HOSTS = [
    'your-app-name.onrender.com',  # Replace with your Render app name
    'localhost',
    '127.0.0.1',
]

# Backend URL for image generation
BACKEND_URL = os.environ.get('BACKEND_URL', 'https://your-app-name.onrender.com')

# Database - MySQL on CloudMonster ASP
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'bookverse'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# CORS settings for frontend
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app",  # Replace with your Vercel domain
    "http://localhost:3000",  # For local development
]

CORS_ALLOW_CREDENTIALS = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
