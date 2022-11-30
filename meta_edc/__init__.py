import os
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(os.getcwd().split(os.sep)[-1])
except PackageNotFoundError:
    __version__ = None
