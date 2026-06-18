"""Test settings for Django test runs.

This ensures tests run against a local Docker PostgreSQL instance and do not
accidentally connect to production database services.
"""

from .settings import *  # noqa: F401,F403

DEBUG = False

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

# Disable sending of CSRF headers during tests.
CSRF_TRUSTED_ORIGINS = []

# Use single origin test host pattern.
ALLOWED_HOSTS = ['testserver']

# Do not use any production-level CORS configuration while testing.
CORS_ALLOW_ALL_ORIGINS = True
