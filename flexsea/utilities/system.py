import os
import platform


# ============================================
#                   get_os
# ============================================
def get_os() -> str:
    """
    Returns the operating system and "bitness" (64 or 32 bit):

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
        machine = os.uname().machine
        if machine.startswith("arm") or machine.startswith("aarch"):
            system = "pi"

    return system + "_" + platform.architecture()[0]
