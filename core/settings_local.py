"""Local settings for development.

Use this configuration when running Django locally with Docker PostgreSQL.
This file intentionally ignores DATABASE_URL so tests and local work do not
accidentally connect to production Supabase.
"""

from .settings import *  # noqa: F401,F403

# Local development should never use production host binding.
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1', 'http://localhost']

# Force local Docker PostgreSQL for local development and tests.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='trading_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Avoid accidentally using DATABASE_URL from local environment files.
DATABASE_URL = ''

# Keep CORS relaxed for local development.
CORS_ALLOW_ALL_ORIGINS = True
