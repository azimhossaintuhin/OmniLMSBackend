# core/settings/development.py

from .base import *

# Development-specific settings
DEBUG = True  # Set to True for development

ALLOWED_HOSTS = ["*"]





# Add any other development-specific settings here
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = False