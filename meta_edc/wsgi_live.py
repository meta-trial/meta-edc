import os

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "meta_edc.settings.live"

application = get_wsgi_application()
