import os
import sys

from multisite import SiteID

from .defaults import *  # noqa

sys.stdout.write(f"Settings file {__file__}\n")

# clear cache after changing site, for example:
# from django.core.cache import cache
# cache.clear()
# TZ Sites:
# SITE_ID = SiteID(default=20)  # Amana
# SITE_ID = SiteID(default=10)  # Hindu Mandal
# SITE_ID = SiteID(default=40)  # Mwananyamala
# SITE_ID = SiteID(default=50)  # Mbagala
# SITE_ID = SiteID(default=60)  # Mnazi-Moja
SITE_ID = SiteID(default=30)  # Temeke

INDEX_PAGE = "http://localhost:8000"
EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "mnazi-moja.tz.meta4.clinicedc.org",
    "mbagala.tz.meta4.clinicedc.org",
    "mwananyamala.tz.meta4.clinicedc.org",
    "hindu-mandal.tz.meta4.clinicedc.org",
    "temeke.tz.meta4.clinicedc.org",
    "amana.tz.meta4.clinicedc.org",
]

SECURE_SSL_REDIRECT = False
EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"

if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
    os.makedirs(KEY_PATH)  # noqa
    AUTO_CREATE_KEYS = True

# if debugging, run `export DJANGO_DEBUG=True` before running runserver
# CELERY_TASK_ALWAYS_EAGER = os.getenv("DJANGO_DEBUG", "False") == "True"
# CELERY_TASK_EAGER_PROPAGATES = CELERY_TASK_ALWAYS_EAGER

EDC_PDF_REPORTS_WATERMARK_WORD = "SAMPLE"
EDC_PDF_REPORTS_WATERMARK_FONT = ("Helvetica", 100)
EDC_PHARMACY_LABEL_WATERMARK_WORD = "DO NOT USE"
