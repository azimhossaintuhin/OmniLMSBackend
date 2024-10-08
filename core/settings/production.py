# core/settings/production.py

from .base import *

# Production-specific settings
DEBUG = False  # Ensure this is False for production

ALLOWED_HOSTS = ["*"]

# Add any other production-specific settings here
