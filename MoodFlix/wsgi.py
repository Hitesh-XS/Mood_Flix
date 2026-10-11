"""
WSGI config for MoodFlix project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoodFlix.settings')

application = get_wsgi_application()

if os.getenv('VERCEL'):
    try:
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Startup migration failed: {e}")
