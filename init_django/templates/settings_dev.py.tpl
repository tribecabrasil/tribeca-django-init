"""
Dev settings: desenvolvimento local.
"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    # apps de dev, se necessário
]
