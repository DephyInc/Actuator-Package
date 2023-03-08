import ctypes as c
from typing import List

from . import enums as fxe
from .dephy_device import DephyDevice
from .specs.api_spec import apiSpec


# ============================================
#                LegacyDevice
# ============================================
class LegacyDevice(DephyDevice):
    """
    Representation of one of Dephy's devices using old comms and
    functionality (e.g., device doesn't know side info).
    """

    SUCCESS = fxe.legacyDeviceErrorCodes["SUCCESS"]
    FAILURE = fxe.legacyDeviceErrorCodes["FAILURE"]
    INVALID_PARAM = fxe.legacyDeviceErrorCodes["INVALID_PARAM"]
    INVALID_DEVICE = fxe.legacyDeviceErrorCodes["INVALID_DEVICE"]
    NOT_STREAMING = fxe.legacyDeviceErrorCodes["NOT_STREAMING"]

    # -----
    # constructor
    # -----
    def __init__(
        self,
        port: str,
        baudRate: int,
        cLibVersion: str,
        logLevel: int,
        loggingEnabled: bool,
        libFile: str = "",
    ) -> None:
        super().__init__(port, baudRate, cLibVersion, logLevel, loggingEnabled, libFile)
        self._state: c.Structure | None = None

    # -----
    # _setup
    # -----
    def _setup(self) -> None:
        """
        Gets device meta-info after establishing a connection. This
        is the part of opening that differs from that of Device.
        """
        self._deviceName = self.deviceName

        if self._deviceName in fxe.hasHabsLegacy:
            self._hasHabs = True

        self._state = fxe.deviceStateDicts[self._deviceName]()

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
    # deviceName
    # -----
    @property
    def deviceName(self) -> str:
        if self._deviceName:
            return self._deviceName

        deviceTypeValue = self._clib.get_device_type_value(self.deviceId)
        return fxe.deviceNames[deviceTypeValue]

    # -----
    # deviceSide
    # -----
    @property
    def deviceSide(self) -> str:
        raise RuntimeError("Legacy devices don't have this functionality.")

    # -----
    # libs_version
    # -----
    @property
    def libsVersion(self) -> str:
        raise RuntimeError("Legacy devices don't have this functionality.")

    # -----
    # _read
    # -----
    def _read(self) -> dict:
        if self._clib.read(self.deviceId, c.byref(self._state)) != self.SUCCESS.value:
            raise RuntimeError("Error: read command failed.")
        return {f[0]: getattr(self._state, f[0]) for f in self._state._fields_}

    # -----
    # _read_all
    # -----
    def _read_all(self) -> List[dict]:
        qs = self.queueSize
        data = (c.POINTER(fxe.deviceStateDicts[self._deviceName]) * qs)()
        allData = []

        nRead = self._clib.all_read(self.deviceId, data, qs)

        try:
            assert nRead == qs
        except AssertionError as err:
            raise RuntimeError("Could not read all data.") from err

        for i in range(nRead):
            allData.append({f[0]: getattr(data[i], f[0]) for f in data[i]._fields_})

        return allData

    # -----
    # rigidVersion
    # -----
    @property
    def rigidVersion(self) -> str:
        raise RuntimeError("Devices don't currently know their own hardware version.")
