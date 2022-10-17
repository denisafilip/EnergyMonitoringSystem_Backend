"""
WSGI config for DS2022_30441_Filip_Denisa_1_Backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DS2022_30441_Filip_Denisa_1_Backend.settings')

application = get_wsgi_application()
