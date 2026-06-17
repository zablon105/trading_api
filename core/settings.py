"""
Django settings for trading_api project.
Supports both local development and production deployment on Render with Supabase.
"""

from pathlib import Path

import dj_database_url
from decouple import config

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

# Secret key for Django sessions and cryptography
# In production, Render will generate a secure value automatically
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# Debug mode: False in production, True in development
DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed hosts: Domains/IPs that can access this application
# In production on Render, add your service URL here
ALLOWED_HOSTS = [host.strip() for host in config('ALLOWED_HOSTS', default='*').split(',') if host.strip()]

# CORS trusted origins for cross-origin requests
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if origin.strip()]

# ============================================================================
# INSTALLED APPS
# ============================================================================

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party packages
    'rest_framework',  # Django REST Framework for API
    'corsheaders',  # Handle Cross-Origin Resource Sharing
    # Our custom apps
    'trades',  # Trading API application
]

# ============================================================================
# MIDDLEWARE
# ============================================================================
# Middleware processes requests/responses

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Allow cross-origin requests
    'django.middleware.security.SecurityMiddleware',  # Security headers
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently in production
    'django.contrib.sessions.middleware.SessionMiddleware',  # User sessions
    'django.middleware.common.CommonMiddleware',  # Common functionality
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# URL configuration
ROOT_URLCONF = 'core.urls'

# ============================================================================
# TEMPLATES
# ============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application for deployment
WSGI_APPLICATION = 'core.wsgi.application'

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# Production: Uses DATABASE_URL from Render (Supabase connection string)
# Development: Uses individual DB_* environment variables for local PostgreSQL

DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Production: Parse DATABASE_URL from Supabase
    # This URL format: postgresql://user:password@host:port/database
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,  # Connection pooling timeout (seconds)
            ssl_require=True   # Enforce SSL for Supabase
        )
    }
else:
    # Development: Use individual environment variables for local database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL database engine
            'NAME': config('DB_NAME', default='trading_db'),      # Database name
            'USER': config('DB_USER', default='postgres'),         # Database user
            'PASSWORD': config('DB_PASSWORD', default=''),         # Database password
            'HOST': config('DB_HOST', default='127.0.0.1'),       # Database host (localhost)
            'PORT': config('DB_PORT', default='5432'),            # Database port
        }
    }

# ============================================================================
# PRODUCTION SECURITY SETTINGS
# ============================================================================

if not DEBUG:
    # Tell Django that HTTPS is being used (for Render behind a proxy)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================
# Rules for validating user passwords

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'  # Set to East African Time
USE_I18N = True  # Enable internationalization
USE_TZ = True   # Use timezone-aware datetimes

# ============================================================================
# STATIC FILES (CSS, JavaScript, Images)
# ============================================================================
# WhiteNoise serves static files efficiently in production

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where to collect static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# REST FRAMEWORK CONFIGURATION
# ============================================================================
# Settings for Django REST Framework API

REST_FRAMEWORK = {
    # How users authenticate with the API
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',  # Login via sessions
    ],
    # Who can access the API
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Only authenticated users
    ],
}

# ============================================================================
# CORS SETTINGS (Cross-Origin Resource Sharing)
# ============================================================================
# Allow API requests from other domains (frontend)

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (adjust in production for security)