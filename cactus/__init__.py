from __future__ import annotations

from pkg_resources import DistributionNotFound, get_distribution, resource_filename

try:
    __version__ = "1.8.0" #get_distribution("cactus-blockchain").version
except DistributionNotFound:
    # package is not installed
    __version__ = "unknown"

PYINSTALLER_SPEC_PATH = resource_filename("cactus", "pyinstaller.spec")
