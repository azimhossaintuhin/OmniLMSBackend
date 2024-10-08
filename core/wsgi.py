"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

# Set the DJANGO_SETTINGS_MODULE based on the PRODUCTION environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production' if config('PRODUCTION', cast=bool) else 'core.settings.development')

application = get_wsgi_application()