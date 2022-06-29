from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa


SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
ALLOWED_HOSTS = [
    "mnazi-moja.tz.meta3.clinicedc.org",
    "mbagala.tz.meta3.clinicedc.org",
    "mwananyamala.tz.meta3.clinicedc.org",
    "hindu-mandal.tz.meta3.clinicedc.org",
    "temeke.tz.meta3.clinicedc.org",
    "amana.tz.meta3.clinicedc.org",
    "mwananyamala.tz.meta.clinicedc.org",
    "hindu-mandal.tz.meta.clinicedc.org",
    "temeke.tz.meta.clinicedc.org",
    "amana.tz.meta.clinicedc.org",
    "localhost",
]
