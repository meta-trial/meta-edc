import os
from importlib.metadata import PackageNotFoundError, version

# from .celery import app

try:
    __version__ = version(os.getcwd().split(os.sep)[-1])
except PackageNotFoundError:
    __version__ = None


__all__ = ["__version__"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meta_edc.settings.debug")
