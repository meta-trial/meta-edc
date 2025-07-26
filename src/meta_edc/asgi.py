import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.debug")

application = get_asgi_application()
