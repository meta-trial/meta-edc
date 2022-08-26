from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa


SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
ALLOWED_HOSTS = [
    "amana.tz.meta3.clinicedc.org",
    "hindu-mandal.tz.meta3.clinicedc.org",
    "mbagala.tz.meta3.clinicedc.org",
    "mnazi-moja.tz.meta3.clinicedc.org",
    "mwananyamala.tz.meta3.clinicedc.org",
    "temeke.tz.meta3.clinicedc.org",
]
EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"
LIVE_SYSTEM = True
