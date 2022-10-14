import os  # noqa

from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=30)
EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "mnazi-moja.tz.meta3.clinicedc.org",
    "mbagala.tz.meta3.clinicedc.org",
    "mwananyamala.tz.meta3.clinicedc.org",
    "hindu-mandal.tz.meta3.clinicedc.org",
    "temeke.tz.meta3.clinicedc.org",
    "amana.tz.meta3.clinicedc.org",
]

SECURE_SSL_REDIRECT = False
EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"

if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
    os.makedirs(KEY_PATH)  # noqa
    AUTO_CREATE_KEYS = True
