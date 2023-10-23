import ctypes as c
import os
import platform
import sys
from typing import List

from serial.tools.list_ports import comports

import flexsea.utilities.constants as fxc


# ============================================
#                   get_os
# ============================================
def get_os() -> str:
    """
    Returns the operating system and "bitness" (64 or 32 bit).
    Can be:
        * windows_32bit
        * windows_64bit
        * pi_32bit
        * pi_64bit
        * linux_32bit
        * linux_64bit
    Returns
    -------
    os : str
        The name and "bitness" of the current operating system.
    """
    system = platform.system().lower()

    if system == "linux":
        machine = platform.machine()
        if machine.startswith("arm") or machine.startswith("aarch"):
            system = "pi"

    return system + "_" + platform.architecture()[0]


# ============================================
#             find_device_ports
# ============================================
def find_device_ports(clib: c.CDLL, baudRate: int = 230400) -> List[str]:
    stdout = sys.stdout
    devicePorts = []

    with open(os.devnull, "w") as fd:
        sys.stdout = fd
        for _port in comports():
            p = _port.device
            if p.startswith("/dev/ttyACM"):
                deviceID = clib.fxOpen(p.encode("utf-8"), baudRate, 0)
                if deviceID in (
                    fxc.deviceErrorCodes["INVALID_DEVICE"].value,
                    fxc.legacyDeviceErrorCodes["INVALID_DEVICE"].value,
                    -1,
                ):
                    continue
                devicePorts.append(p)
                clib.fxClose(deviceID)

    sys.stdout = stdout
    if len(devicePorts) == 0:
        raise RuntimeError("Could not find a valid device.")

    return devicePorts
