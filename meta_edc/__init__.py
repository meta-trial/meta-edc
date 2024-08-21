import os
import sys
from importlib.metadata import PackageNotFoundError, version

if "meta_edc.celery.live:app" in sys.argv:
    from .celery.live import app as celery_app
elif "meta_edc.celery.uat:app" in sys.argv:
    from .celery.uat import app as celery_app
else:
    from .celery.debug import app as celery_app

try:
    __version__ = version(os.getcwd().split(os.sep)[-1])
except PackageNotFoundError:
    __version__ = None


__all__ = ["celery_app", "__version__"]
