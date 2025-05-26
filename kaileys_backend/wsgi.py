"""
WSGI config for kaileys_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaileys_backend.settings')



# Auto-create superuser if not exists
try:
    from kaileys_app.create_admin import run
    run()
except Exception as e:
    print("Superuser creation error:", e)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
