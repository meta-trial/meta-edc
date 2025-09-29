"""
A settings file with the bare minimum attributes.
"""

from pathlib import Path

import environ
from multisite import SiteID

APP_NAME = "meta_edc"
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(ENV_DIR / ".env")

EDC_SITES_MODULE_NAME = env.str("EDC_SITES_MODULE_NAME")
ETC_DIR = env.str("DJANGO_ETC_FOLDER")
SECRET_KEY = "blahblahblah"  # noqa: S105
ALLOWED_HOSTS = ["*"]
SITE_ID = SiteID(default=1)  # 1 is not a site
