"""
A settings file with the bare minimum attributes.
"""
import os
from pathlib import Path

import environ
from multisite import SiteID

APP_NAME = "meta_edc"
BASE_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)
ENV_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)

env = environ.Env()
env.read_env(os.path.join(ENV_DIR, ".env"))

EDC_SITES_MODULE_NAME = env.str("EDC_SITES_MODULE_NAME")
ETC_DIR = env.str("DJANGO_ETC_FOLDER")
SECRET_KEY = "blahblahblah"  # nosec B105
ALLOWED_HOSTS = ["*"]
SITE_ID = SiteID(default=1)  # 1 is not a site
