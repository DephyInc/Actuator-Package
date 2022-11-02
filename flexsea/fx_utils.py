import boto3
import ctypes as c
import os
from pathlib import Path
import platform

import numpy as np
import yaml

from . import config as cfg
from . import fx_enums as fxe
from .dev_specs import AllDevices as fx_devs


# ============================================
#                   is_win
# ============================================
def is_win():
    """
    Returns `True` if the OS is windows.
    """
    return "win" in platform.system().lower()


# ============================================
#                    is_pi
# ============================================
def is_pi():
    """
    Returns true if the OS is running on an arm. Used to detect
    Raspberry pi.
    """
    try:
        return os.uname().machine.startswith("arm")
    except AttributeError:
        return False


# ============================================
#                   is_pi64
# ============================================
def is_pi64():
    """
    Returns true if the OS is running on an Ubuntu 64 for Arm.
    Used to detect Raspberry pi aarch64.
    """
    try:
        return os.uname().machine.startswith("aarch64")
    except AttributeError:
        return False


# ============================================
#                    decode
# ============================================
def decode(val):
    """
    Returns decoded version number formatted as x.y.z
    """
    major = minor = bug = 0

    if val > 0:
        while val % 2 == 0:
            major += 1
            val /= 2

        while val % 3 == 0:
            minor += 1
            val /= 3

        while val % 5 == 0:
            bug += 1
            val /= 5

    return f"{major}.{minor}.{bug}"


# ============================================
#                clear_terminal
# ============================================
def clear_terminal():
    """
    Clears the terminal - use before printing new values
    """
    os.system("cls" if is_win() else "clear")


# ============================================
#               print_plot_exit
# ============================================
def print_plot_exit():
    """
    Prints plot exit message
    """
    if is_win():
        print("In Windows, press Ctrl+Break to exit. Ctrl+C may not work.")


# ============================================
#              print_loop_count
# ============================================
def print_loop_count(count, total):
    """
    Convenience function for printing run counts
    """
    print(f"\nRun {count + 1} of {total}")


# ============================================
#         print_loop_count_and_time
# ============================================
def print_loop_count_and_time(count, total, elapsed_time):
    """
    Convenience function for printing run counts and elapsed time in s.
    """
    print(f"\nLoop {count + 1} of {total} - Elapsed time: {round(elapsed_time)}s")


# ============================================
#                sin_generator
# ============================================
def sin_generator(amplitude, freq, command_freq):
    """
    Generate a sine wave of a specific amplitude and frequency
    """
    num_samples = command_freq / freq
    print(f"number of samples is: {int(num_samples)}")
    in_array = np.linspace(-np.pi, np.pi, int(num_samples))
    sin_vals = amplitude * np.sin(in_array)
    return sin_vals


# ============================================
#               line_generator
# ============================================
def line_generator(mag, length, command_freq):
    """
    Generate a line with specific magnitude
    """
    num_samples = np.int32(length * command_freq)
    line_vals = [mag for i in range(num_samples)]
    return line_vals


# ============================================
#                linear_interp
# ============================================
def linear_interp(start, end, points):
    """
    Interpolates between two positions (A to B)
    """
    return np.linspace(start, end, points)


# ============================================
#            load_ports_from_file
# ============================================
def load_ports_from_file(file_name):
    """
    Loads baud_rate and ports serial ports list from a yaml file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as com_file:
            vals = yaml.load(com_file, Loader=yaml.FullLoader)
            return vals["ports"], int(vals["baud_rate"])

    except IOError as err:
        print(f"Problem loading {file_name}: {err}")
        print(
            "Copy the ports_template.yaml to a file named ports.yaml"
            "Be sure to use the same format of baud rate on the first line,"
            "and com ports on preceding lines"
        )
        raise err
    except ValueError as err:
        print(f"Problem with the yaml file syntax or values: {err}")
        raise err


# ============================================
#                  _get_os
# ============================================
def _get_os() -> str:
    """
    Determines which operating system we're running on.

    Returns
    -------
    str:
            The name of the operating system. Matches the directory inside
            `libs` containing the c libraries appropriate for that OS.
    """
    # Windows
    if "win" in platform.system().lower():
        # 32 bit
        if platform.architecture()[0] == "32bit":
            operating_system = "win32"
        # 64 bit
        else:
            operating_system = "win64"
    # Pi - 32 bit
    elif os.uname().machine.startswith("arm"):
        operating_system = "raspberryPi"
    # Pi - 64 bit
    elif os.uname().machine.startswith("aarch64"):
        operating_system = "raspberryPi64"
    # This check is specifically after the pi check because the pi also
    # returns 'Linux' from platform.system()
    elif "linux" in platform.system().lower():
        operating_system = "linux"
    else:
        raise OSError("Unknown operating system!")
    return operating_system


# ============================================
#                  _add_dlls
# ============================================
def _add_dlls(lib_path: str) -> None:
    """
    Explicitly adds the appropriate directories to the `PATH` on Windows.

    Parameters
    ----------
    lib_path : str
            The full path to the directory containing the Windows
            precompiled libraries.
    """
    for extra_path in os.environ["PATH"].split(";"):
        if os.path.exists(extra_path) and "mingw" in extra_path:
            os.add_dll_directory(extra_path)
    os.add_dll_directory(lib_path)


# ============================================
#             _set_data_types
# ============================================
def _set_data_types(clib: c.CDLL) -> c.CDLL:
    """
    Defines the function prototypes.

    Parameters
    ----------
    clib : c.CDLL
            The Python object interfacing with the C libraries we're
            setting the prototypes for.

    Returns
    -------
    clib : c.CDLL
            The Python object interfacing with the C libraries for which
            we've set the prototypes.
    """
    clib.fxOpen.argtypes = [c.c_char_p, c.c_uint, c.c_uint]
    clib.fxOpen.restype = c.c_int

    clib.fxIsOpen.argtypes = [c.c_uint]
    clib.fxIsOpen.restype = c.c_bool

    clib.fxClose.argtypes = [c.c_uint]
    clib.fxClose.restype = c.c_int

    clib.fxCloseAll.argtypes = []
    clib.fxCloseAll.resType = []

    clib.fxGetDeviceIds.argtypes = [c.POINTER(c.c_int), c.c_uint]

    clib.fxStartStreaming.argtypes = [c.c_uint, c.c_uint, c.c_bool]
    clib.fxStartStreaming.restype = c.c_int

    clib.fxStopStreaming.argtypes = [c.c_uint]
    clib.fxStopStreaming.restype = c.c_int

    clib.fxReadDevice.argtypes = [c.c_uint, c.POINTER(fx_devs.ActPackState)]
    clib.fxReadDevice.restype = c.c_int

    clib.fxReadDeviceAll.argtypes = [
        c.c_uint,
        c.POINTER(fx_devs.ActPackState),
        c.c_uint,
    ]
    clib.fxReadDeviceAll.restype = c.c_int

    clib.fxReadMdDeviceAll.argtypes = [
        c.c_uint,
        c.POINTER(fx_devs.MD10State),
        c.c_uint,
    ]
    clib.fxReadMdDeviceAll.restype = c.c_int
    clib.fxReadMdDevice.argtypes = [c.c_uint, c.POINTER(fx_devs.MD10State)]
    clib.fxReadMdDeviceAll.restype = c.c_int

    clib.fxReadNetMasterDevice.argtypes = [c.c_uint, c.POINTER(fx_devs.NetMasterState)]
    clib.fxReadDevice.restype = c.c_int

    clib.fxReadNetMasterDeviceAll.argtypes = [
        c.c_uint,
        c.POINTER(fx_devs.NetMasterState),
        c.c_uint,
    ]
    clib.fxReadNetMasterDeviceAll.restype = c.c_int

    clib.fxSetReadDataQueueSize.argtypes = [c.c_uint, c.c_uint]
    clib.fxSetReadDataQueueSize.restype = c.c_uint

    clib.fxGetReadDataQueueSize.argtypes = [c.c_uint]
    clib.fxGetReadDataQueueSize.restype = c.c_int

    clib.fxSetGains.argtypes = [
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
    ]
    clib.fxSetGains.restype = c.c_int

    clib.fxSendMotorCommand.argtypes = [c.c_uint, c.c_int, c.c_int]
    clib.fxSendMotorCommand.restype = c.c_int

    clib.fxGetAppType.argtypes = [c.c_uint]

    clib.fxActivateBootloader.argtypes = [c.c_uint, c.c_uint8]
    clib.fxActivateBootloader.restype = c.c_int

    clib.fxIsBootloaderActivated.argtypes = [c.c_uint]
    clib.fxIsBootloaderActivated.restype = c.c_int

    clib.fxRequestFirmwareVersion.argtypes = [c.c_uint]
    clib.fxRequestFirmwareVersion.restype = c.c_int

    clib.fxGetLastReceivedFirmwareVersion.argtypes = [c.c_uint]
    clib.fxGetLastReceivedFirmwareVersion.restype = fxe.FW

    return clib


# ============================================
#                 _load_clib
# ============================================
def _load_clib(libsVersion: str) -> c.CDLL:
    """
    Uses `ctypes` to load the appropriate C libraries depending on the
    OS.

    Parameters
    ----------
    libsVersion : str
        The version of the pre-compiled libraries to use. The major version
        should match the major version of the firmware being used. If no
        libraries are found, then we download them from AWS.

    Raises
    ------
    OSError:
            Raised if the precompiled libraries fail to load.

    Returns
    -------
    clib : ctypes.cdll.CDLL
            The Python object from which we can call the flexsea C
            functions.
    """
    _os = _get_os()
    lib_dir = cfg.libsDir.joinpath(libsVersion, _os)

    if "win" in _os:
        lib = "libfx_plan_stack.dll"
    else:
        lib = "libfx_plan_stack.so"

    lib_path = lib_dir.joinpath(lib)

    if not lib_path.exists():
        lib_dir.mkdir(parents=True, exist_ok=True)
        lib_obj = str(Path("libs").joinpath(libsVersion, _os, lib).as_posix())
        s3 = boto3.resource("s3")
        s3.Bucket(cfg.libsBucket).download_file(lib_obj, str(lib_path))

        if not lib_path.exists():
            raise OSError("Unable to download firmware.")

    if "win" in _os:
        try:
            _add_dlls(str(lib_dir))
            clib = c.cdll.LoadLibrary(str(lib_path))
        except OSError as err:
            msg = f"\n[!] Error loading the {lib} precompiled libraries.\n"
            msg += (
                "The most likely cause is a mismatch between the Python, pip and shell "
                "architectures.\n"
            )
            msg += "To solve this, ensure all three are either 32 or 64 bit.\n"
            msg += "Keep different versions isolated by virtual environments.\n"
            msg += "For additional help, follow the installation instructions here: "
            msg += "https://github.com/DephyInc/Actuator-Package\n"
            msg += "--------------------------------------------\n\n"
            msg += f"Detailed error message for debugging:\n{err}\n"
            print(msg)
    else:
        clib = c.cdll.LoadLibrary(str(lib_path))

    return _set_data_types(clib)
