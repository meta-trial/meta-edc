import sys

from multisite import SiteID

from .defaults import *  # noqa

sys.stdout.write(f"Settings file {__file__}\n")

SITE_ID = SiteID(default=1)
EDC_SITES_UAT_DOMAIN = False
EDC_MODEL_ADMIN_CSS_THEME = "edc_indigo"
LIVE_SYSTEM = True
EDC_SITES_DOMAIN_SUFFIX = "meta4.clinicedc.org"
AUTO_CREATE_KEYS = False
