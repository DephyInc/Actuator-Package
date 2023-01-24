import setuptools.version as ver

from . import config as cfg
from .dephy_device import DephyDevice
from .legacy_device import LegacyDevice
from .utilities import find_port


# ============================================
#                   Device
# ============================================
class Device(LegacyDevice):
    """
    The leaf of the device inheritance tree. The purpose of this class
    is to serve as the user-facing object.
    """

    # -----
    # __new__
    # -----
    def __new__(
        cls,
        port: str = "",
        baudRate: int = cfg.baudRate,
        cLibVersion: str = cfg.LTS,
        logLevel: int = 4,
        loggingEnabled: bool = True,
    ) -> DephyDevice | LegacyDevice:
        inUse = ver.pkg_resources.parse_version(cLibVersion)
        cutoff = ver.pkg_resources.parse_version(cfg.legacyCutoff)

        if not port:
            port = find_port(baudRate, cLibVersion)

        if inUse < cutoff:
            return LegacyDevice(port, baudRate, cLibVersion, logLevel, loggingEnabled)
        return DephyDevice(port, baudRate, cLibVersion, logLevel, loggingEnabled)
