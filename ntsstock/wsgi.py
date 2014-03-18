"""
WSGI config for ntsstock project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os,sys
sys.path.append(os.path.abspath( os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ntsstock.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
