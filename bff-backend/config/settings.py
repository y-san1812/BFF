import os
from pathlib import Path
from datetime import timedelta
import environ

# Install PyMySQL as MySQLdb driver fallback
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

from config.security import (  # noqa: E402
    INSECURE_DEFAULT_SECRET_KEY,
    validate_production_settings,
)

# Fail closed: DEBUG defaults to False unless explicitly enabled via environment variable.
DEBUG = env.bool('DEBUG', default=False)

# SECRET_KEY: read from environment; raise a clear error if missing in production (DEBUG=False).
SECRET_KEY = env('SECRET_KEY', default='')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = INSECURE_DEFAULT_SECRET_KEY
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(
            'SECRET_KEY environment variable is missing! '
            'You must set SECRET_KEY in production when DEBUG=False.'
        )

# ALLOWED_HOSTS: parsed from environment variable (comma-separated), e.g. "bharat-freeze-dry-foods-production.up.railway.app,localhost"
raw_allowed_hosts = env('ALLOWED_HOSTS', default='')
if raw_allowed_hosts:
    ALLOWED_HOSTS = [h.strip() for h in raw_allowed_hosts.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'] if DEBUG else []

validate_production_settings(
    debug=DEBUG,
    secret_key=SECRET_KEY,
    allowed_hosts=ALLOWED_HOSTS,
)

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Installed Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Packages
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'drf_spectacular',

    # BFF Apps
    'apps.users',
    'apps.catalog',
    'apps.enquiries',
    'apps.crm',
    'apps.media_library',
    'apps.cms',
    'apps.newsletter',
    'apps.activity_log',
]

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration — MySQL via env vars (MYSQLHOST, MYSQLPORT, MYSQLDATABASE, MYSQLUSER, MYSQLPASSWORD)
# or DATABASE_URL, with local-dev fallbacks (localhost:3306) so app runs locally without env vars set.
DB_HOST = os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST') or '127.0.0.1'
DB_PORT = os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT') or '3306'
DB_NAME = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DATABASE') or 'bff'
DB_USER = os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER') or 'root'
DB_PASSWORD = os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD') or 'Gargi@2275'

if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': env.db('DATABASE_URL')
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

_db_engine = DATABASES['default'].get('ENGINE', '')
if 'mysql' in _db_engine:
    DATABASES['default'].setdefault('OPTIONS', {
        'charset': 'utf8mb4',
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    })

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # B11: fail closed — views must explicitly AllowAny when public.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # otp_send: IP throttle for POST /auth/send-otp/ (see SendOTPIPThrottle).
    'DEFAULT_THROTTLE_RATES': {
        'otp_send': '10/hour',
    },
}

# Simple JWT Settings
SIMPLE_JWT = {
    # B12: short-lived access; silent refresh (F5) renews transparently.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS — never allow all origins. Configure CORS_ALLOWED_ORIGINS for staging/production.
# Local dev ports: 8080 (TanStack/Lovable), 5173 (Vite), 8082, 3000.
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        'http://localhost:8080',
        'http://127.0.0.1:8080',
        'http://localhost:8081',   # add this
    'http://127.0.0.1:8081',   
        'http://localhost:8082',
        'http://127.0.0.1:8082',
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ] if DEBUG else [],
)

if not DEBUG and not CORS_ALLOWED_ORIGINS:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        'CORS_ALLOWED_ORIGINS must be set when DEBUG is False '
        '(comma-separated frontend origins, e.g. https://www.example.com).'
    )

# CSRF trusted origins must match SPA origins when frontend/API are on different
# hosts/ports (required for cookie-authenticated refresh/logout with X-CSRFToken).
CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS',
    default=list(CORS_ALLOWED_ORIGINS) if DEBUG else [],
)
if not DEBUG and not CSRF_TRUSTED_ORIGINS:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured(
        'CSRF_TRUSTED_ORIGINS must be set when DEBUG is False '
        '(comma-separated frontend origins, e.g. https://www.example.com).'
    )

# F5 refresh cookie: httpOnly; Secure in production; SameSite=Lax for same-site
# SPA<->API (e.g. www + api subdomains). Use SameSite=None only if frontend and API
# are truly cross-site (different registrable domains) — then Secure must be True.
REFRESH_COOKIE_SECURE = env.bool('REFRESH_COOKIE_SECURE', default=not DEBUG)
REFRESH_COOKIE_SAMESITE = env('REFRESH_COOKIE_SAMESITE', default='Lax')

# OpenAPI Schema Metadata
SPECTACULAR_SETTINGS = {
    'TITLE': 'Bharat Freeze Dry Foods (BFF) API',
    'DESCRIPTION': 'REST API engine powering the BFF public marketplace and B2B admin dashboard.',
    'VERSION': '1.0.0',
}

# Razorpay config: use test keys in development and swap to production keys before go-live.
RAZORPAY_KEY_ID = env('RAZORPAY_KEY_ID', default='')
RAZORPAY_KEY_SECRET = env('RAZORPAY_KEY_SECRET', default='')
RAZORPAY_WEBHOOK_SECRET = env('RAZORPAY_WEBHOOK_SECRET', default='')

# Email — console backend locally; set EMAIL_HOST* in .env for real SMTP delivery.
EMAIL_BACKEND = env(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@bff-foods.com')

# Branded OTP emails
OTP_EMAIL_SITE_NAME = env('OTP_EMAIL_SITE_NAME', default='Bharat Freeze Dry Foods')
FRONTEND_URL = env('FRONTEND_URL', default='http://localhost:8080')
# Optional: public HTTPS logo URL for emails (e.g. https://yoursite.com/logo.png)
OTP_EMAIL_LOGO_URL = env('OTP_EMAIL_LOGO_URL', default='')

# Unpaid checkout stock hold TTL (minutes). release_abandoned_orders restores
# stock for orders older than this that never reached a paid/terminal status.
ABANDONED_ORDER_TIMEOUT_MINUTES = env.int('ABANDONED_ORDER_TIMEOUT_MINUTES', default=45)