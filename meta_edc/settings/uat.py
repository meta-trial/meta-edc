from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
ALLOWED_HOSTS = [
    "amana.uat.tz.meta.clinicedc.org",
    "hindu-mandal.uat.tz.meta.clinicedc.org",
    "temeke.uat.tz.meta.clinicedc.org",
    "localhost",
]
