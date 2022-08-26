from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")  # noqa


SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
EDC_CONSENT_BYPASS_CONSENT_DATETIME_VALIDATION = True
ALLOWED_HOSTS = [
    "amana.uat.tz.meta3.clinicedc.org",
    "hindu-mandal.uat.tz.meta3.clinicedc.org",
    "mbagala.uat.tz.meta3.clinicedc.org",
    "mnazi-moja.uat.tz.meta3.clinicedc.org",
    "mwananyamala.uat.tz.meta3.clinicedc.org",
    "temeke.uat.tz.meta3.clinicedc.org",
]

# edc_model_admin
EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"
LIVE_SYSTEM = False
