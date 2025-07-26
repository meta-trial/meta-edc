from multisite import SiteID

from .defaults import *  # noqa

print(f"Settings file {__file__}")

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"
LIVE_SYSTEM = True
EDC_SITES_DOMAIN_SUFFIX = "meta4.clinicedc.org"
