from importlib.metadata import version as _version, PackageNotFoundError
from .file_manipulation import *
try:
    __version__ = _version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

# from .version import version as __version__

# __all__ = []
