from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
ALLOWED_HOSTS = [
    "amana.tz.meta.clinicedc.org",
    "hindu-mandal.tz.meta.clinicedc.org",
    "temeke.tz.meta.clinicedc.org",
    "localhost",
]
