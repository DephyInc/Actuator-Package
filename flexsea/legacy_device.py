import ctypes as c
from time import sleep
from typing import List
from typing import Self

from . import config as cfg
from . import enums as fxe
from . import utilities as fxu
from .device import Device
from .specs.api_spec import apiSpec


# ============================================
#                LegacyDevice
# ============================================
class LegacyDevice(Device):
    """
    Representation of one of Dephy's devices using old comms and
    functionality (e.g., device doesn't know side info).
    """

    # -----
    # constructor
    # -----
    def __init__(
        self,
        port: str,
        baudRate: int,
        cLibVersion: str = cfg.LTS,
        logLevel: int = 4,
        loggingEnabled: bool = True,
    ) -> None:

        super().__init__(port, baudRate, cLibVersion, logLevel, loggingEnabled)
        self._state: c.Structure | None = None 

    # -----
    # _version_check
    # -----
    def _version_check(self, using: str) -> None:
        inUse = ver.pkg_resources.parse_version(cLibVersion)
        cutoff = ver.pkg_resources.parse_version(cfg.legacyCutoff)

        if inUse >= cutoff:
            msg = f"For versions of the pre-compiled C libraries >= {cfg.legacyCutoff} "
            msg += "please use the `Device` class."
            raise ValueError(msg)

    # -----
    # _setup
    # -----
    def _setup(self) -> None:
        """
        Gets device meta-info after establishing a connection. This
        is the part of opening that differs from that of Device.
        """
        deviceTypeValue = self._clib.get_device_type_value(self.deviceID)
        self._deviceName = fxe.deviceNames[deviceTypeValue]

        if self._deviceName in fxe.hasHabsLegacy:
            self.hasHabs = True

        self._state = fxe.deviceStateDicts[self.deviceName]

        # The read function is set here and not with other c functions
        # because we need the device name, which we can't get without
        # calling open, for which we need the c library loaded
        rf = apiSpec[self.cLibVersion]["read_functions"][self._deviceName]

        for key in ("", "all_"):
            func = getattr(self._clib, rf[key + "name"])
            func.argtypes = rf[key + "argTypes"]
            func.restype = rf[key + "returnType"]
            setattr(self._clib, key + "read", func)

    # -----
    # deviceSide
    # -----
    @property
    def deviceSide(self) -> None:
        raise RuntimeError("Legacy devices don't have this functionality.")

    # -----
    # libs_version
    # -----
    @property
    def libsVersion(self) -> None:
        raise RuntimeError("Legacy devices don't have this functionality.")

    # -----
    # _read
    # -----
    def _read(self) -> dict:
        if self._clib.read(self.deviceID, c.byref(self._state)) != fxe.SUCCESS.value:
            raise RuntimeError("Error: read command failed.")
        return {f[0]:getattr(self._state, f[0])for f in self._state._fields_}

    # -----
    # _read_all
    # -----
    def _read_all(self) -> List[dict]:
        # fxReadDeviceAll(const unsigned int deviceId, ActPackState* readData, const unsigned int n) is the prototype
        # What's "returned" is readData, which is an array of ActPackState structs
        raise NotImplementedError
        returnCode = self._clib.all_read(
            self.deviceID, c.byref(self._state), self.queueSize
        )
