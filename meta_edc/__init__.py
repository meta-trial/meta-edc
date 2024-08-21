import os
from importlib.metadata import PackageNotFoundError, version

from .celery import app as celery_app

# from .celery.live import app as celery_live
# from .celery.uat import app as celery_uat

try:
    __version__ = version(os.getcwd().split(os.sep)[-1])
except PackageNotFoundError:
    __version__ = None


# __all__ = ["celery_live", "celery_uat", "celery_debug", "__version__"]
__all__ = ["__version__", "celery_app"]
