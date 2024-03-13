from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = True
EDC_MODEL_ADMIN_CSS_THEME = "edc_purple"
LIVE_SYSTEM = False
EDC_CONSENT_BYPASS_CONSENT_DATETIME_VALIDATION = True
