import importlib.metadata

from .celery import app as celery_app

try:
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__", "celery_app"]
