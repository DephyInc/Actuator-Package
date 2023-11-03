import platform
import sys
from typing import List

# We use sys instead of platform because that's what poetry uses to
# determine if a dependency should be installed or not
if sys.platform == "linux":
    import pyudev


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
#               find_stm_ports
# ============================================
def find_stm_ports() -> List[str]:
    if "windows" in get_os():
        raise OSError("This function only works on Linux.")

    # pylint: disable-next=used-before-assignment
    context = pyudev.Context()
    devicePorts = []

    for device in context.list_devices(ID_VENDOR="STMicroelectronics", block="tty"):
        devicePorts.append(device.device_node)

    return devicePorts
