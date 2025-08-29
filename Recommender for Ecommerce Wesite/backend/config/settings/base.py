import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv('SECRET_KEY','dev-secret')
DEBUG = os.getenv('DEBUG','1') == '1'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS','*').split(',')

INSTALLED_APPS = [
  'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
  'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
  'rest_framework','corsheaders','drf_spectacular',
  # Feature-first apps
  'apps.common.apps.CommonConfig',
  'apps.users.apps.UsersConfig', 
  'apps.catalog.apps.CatalogConfig',
  'apps.orders.apps.OrdersConfig',
  # Minimal placeholder apps (can be expanded later)
  'apps.payments.apps.PaymentsConfig',
  'apps.activities.apps.ActivitiesConfig', 
  'apps.cart.apps.CartConfig',
  'apps.recommendations.apps.RecommendationsConfig',
]

# Optionally include drf_spectacular_sidecar if installed (provides local swagger assets)
try:
  import drf_spectacular_sidecar  # type: ignore
  INSTALLED_APPS.append('drf_spectacular_sidecar')
except Exception:
  pass

MIDDLEWARE = [
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'

# Custom user model
AUTH_USER_MODEL = 'users.User'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.getenv('MYSQL_DATABASE','BookStore'),
    'USER': os.getenv('MYSQL_USER','root'),
    'PASSWORD': os.getenv('MYSQL_PASSWORD',''),
    'HOST': os.getenv('MYSQL_HOST','127.0.0.1'),
    'PORT': os.getenv('MYSQL_PORT','3306'),
    'OPTIONS': {
        'charset': 'utf8mb4',
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
  }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

JWT_SECRET = os.getenv('JWT_SECRET', SECRET_KEY)
JWT_ACCESS_TTL_MINUTES = int(os.getenv('JWT_ACCESS_TTL_MINUTES', '15'))
JWT_REFRESH_TTL_DAYS = int(os.getenv('JWT_REFRESH_TTL_DAYS', '7'))

REST_FRAMEWORK = {
  "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
  "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
  "DEFAULT_VERSION": "v1",
  "ALLOWED_VERSIONS": ("v1",),
  "DEFAULT_AUTHENTICATION_CLASSES": [
      "apps.users.auth.JWTAuthentication",
      "rest_framework.authentication.SessionAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
  "TITLE": "E-commerce API (Cloud DB)",
  "DESCRIPTION": "DRF over existing MariaDB schema: catalog, orders, payments, activities.",
  "VERSION": "1.0.0",
  "SERVE_INCLUDE_SCHEMA": False,
  "SERVERS": [{"url": "http://localhost:8000", "description": "Local"}],
}

# CORS settings for frontend connection (dev)
CORS_ALLOWED_ORIGINS = [
  "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True

# Default language and timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Use signed cookie session backend to avoid creating django_session table on the
# remote managed database (we don't run migrations against it).
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
