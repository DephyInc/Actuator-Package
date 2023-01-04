import setuptools.version as ver

from . import config as cfg
from .current_device import CurrentDevice
from .legacy_device import LegacyDevice


# ============================================
#                   Device
# ============================================
class Device:
    """
    Metaclass for instantaiting the correct device class based on the
    desired version of the pre-compiled C libraries.
    """

    # -----
    # __new__
    # -----
    def __new__(
        cls,
        port: str,
        baudRate: int,
        cLibVersion: str = cfg.LTS,
        logLevel: int = 4,
        loggingEnabled: bool = True,
    ) -> CurrentDevice | LegacyDevice:
        inUse = ver.pkg_resources.parse_version(cLibVersion)
        cutoff = ver.pkg_resources.parse_version(cfg.legacyCutoff)

        if inUse < cutoff:
            return LegacyDevice(port, baudRate, cLibVersion, logLevel, loggingEnabled)
        return CurrentDevice(port, baudRate, cLibVersion, logLevel, loggingEnabled)
