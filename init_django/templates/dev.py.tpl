# Development-specific settings

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts allowed in development
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
]

# Add any development-specific apps
# INSTALLED_APPS += []

# Add any development-specific middleware
# MIDDLEWARE += []

# Email backend for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# You can add other development-specific settings here
