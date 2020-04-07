import os

from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=10)
EDC_SITES_UAT_DOMAIN = False
DEBUG = True
ALLOWED_HOSTS = [
    "hindu-mandal.tz.meta.clinicedc.org",
    "localhost",
]  # env.list('DJANGO_ALLOWED_HOSTS')
# ETC_DIR = os.path.join(BASE_DIR, "tests", "etc")  # noqa
# KEY_PATH = os.path.join(ETC_DIR, "crypto_fields")
# # KEY_PATH = os.path.join(BASE_DIR, ".etc", "meta", "crypto_fields")
#
# if os.path.exists(BASE_DIR) and not os.path.exists(KEY_PATH):  # noqa
#     os.makedirs(KEY_PATH)
#     AUTO_CREATE_KEYS = True
SECURE_SSL_REDIRECT = False
