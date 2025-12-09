"""
WSGI config for theatre_booking project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theatre_booking.settings')

application = get_wsgi_application()
