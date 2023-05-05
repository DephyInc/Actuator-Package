import semantic_version as sem

from . import config as cfg
from .dephy_device import DephyDevice
from .legacy_device import LegacyDevice


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
        port: str | None = None,
        baudRate: int = cfg.baudRate,
        cLibVersion: str | None = None,
        logLevel: int = 4,
        loggingEnabled: bool = True,
        libFile: str = "",
    ) -> DephyDevice | LegacyDevice:
        if cLibVersion is None:
            raise ValueError("Please provide a valid version for `cLibVersion`.")

        if port is None:
            raise ValueError("Please provide the port your device is connected to.")

        inUse = sem.Version(cLibVersion)
        cutoff = sem.Version(cfg.legacyCutoff)

        if inUse < cutoff:
            return LegacyDevice(
                port, baudRate, cLibVersion, logLevel, loggingEnabled, libFile
            )
        return DephyDevice(
            port, baudRate, cLibVersion, logLevel, loggingEnabled, libFile
        )
