import ctypes as c
import os
from pathlib import Path
from typing import Tuple

from semantic_version import Version

import flexsea.utilities.constants as fxc

from .aws import s3_download
from .firmware import Firmware
from .system import get_os


# ============================================
#                get_c_library
# ============================================
def get_c_library(firmwareVersion: Version, libFile: Path | None) -> Tuple:
    """
    If we're given a library file to use, we make sure it exists. If
    we're not given a library file to use, we check for a cached file
    on disk corresponding to our firmware. If we don't have one, we try
    to download it from S3. We then use ctypes to load the library.
    """
    if libFile is not None:
        try:
            assert libFile.exists()
        except AssertionError as err:
            raise FileNotFoundError(f"Could not find library: {libFile}") from err
    else:
        _os = get_os()
        libFile = fxc.libsPath.joinpath(str(firmwareVersion), _os, fxc.libFiles[_os])
        if not libFile.exists():
            libFile.parent.mkdir(parents=True, exist_ok=True)
            libObj = f"{fxc.libsDir}/{firmwareVersion}/{_os}/{libFile.name}"
            s3_download(libObj, fxc.dephyPublicFilesBucket, str(libFile), None)

    return (_load_clib(libFile), libFile)


# ============================================
#                _load_clib
# ============================================
def _load_clib(libFile: str) -> c.CDLL:
    """
    Uses ctypes to actually create an interface to the library file. If
    we're on Windows, we have to additionally add several directories to
    the path.
    """
    if "win" in get_os():
        try:
            for extraPath in os.environ["PATH"].split(";"):
                if os.path.exists(extraPath) and "mingw" in extraPath:
                    os.add_dll_directory(extraPath)
            os.add_dll_directory(libFile)
        except OSError as err:
            msg = f"Error loading precompiled library: `{libFile}`\n"
            msg += "The most likely cause is a mismatch between the Python, pip and "
            msg += "shell architectures.\nPlease ensure all three are either 32 or 64 "
            msg += "bit.\nKeep different versions isolated by virtual environments.\n"
            print(msg)
            raise err

    return c.cdll.LoadLibrary(libFile)


# ============================================
#               set_prototypes
# ============================================
def set_prototypes(clib: c.CDLL, firmwareVersion: Version) -> c.CDLL:
    # pylint: disable=too-many-statements
    # Open
    clib.fxOpen.argtypes = [c.c_char_p, c.c_uint, c.c_uint]
    clib.fxOpen.restype = c.c_int

    # Close
    clib.fxClose.argtypes = [
        c.c_uint,
    ]
    clib.fxClose.restype = c.c_uint

    # Start streaming
    clib.fxStartStreaming.argtypes = [c.c_uint, c.c_uint, c.c_bool]
    clib.fxStartStreaming.restype = c.c_int

    # Start streaming with safety
    if firmwareVersion >= Version("9.1.2"):
        clib.fxStartStreamingWithSafety.argtypes = [
            c.c_uint,
            c.c_uint,
            c.c_bool,
            c.c_uint16,
        ]
        clib.fxStartStreamingWithSafety.restype = c.c_int

    # Stop streaming
    clib.fxStopStreaming.argtypes = [
        c.c_uint,
    ]
    clib.fxStopStreaming.restype = c.c_int

    # Set gains
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
    # Send motor command
    clib.fxSendMotorCommand.argtypes = [c.c_uint, c.c_int, c.c_int]
    clib.fxSendMotorCommand.restype = c.c_int

    # Find poles
    clib.fxFindPoles.argtypes = [
        c.c_uint,
    ]
    clib.fxFindPoles.restype = c.c_int

    # Activate bootloader
    clib.fxActivateBootloader.argtypes = [c.c_uint, c.c_uint8]
    clib.fxActivateBootloader.restype = c.c_int

    # Is bootloader active
    clib.fxIsBootloaderActivated.argtypes = [
        c.c_uint,
    ]
    clib.fxIsBootloaderActivated.restype = c.c_int

    # Request firmware version
    clib.fxRequestFirmwareVersion.argtypes = [
        c.c_uint,
    ]
    clib.fxRequestFirmwareVersion.restype = c.c_int

    # Get last received firmware version
    clib.fxGetLastReceivedFirmwareVersion.argtypes = [
        c.c_uint,
    ]
    clib.fxGetLastReceivedFirmwareVersion.restype = Firmware

    # Get device type value
    if firmwareVersion < Version("10.0.0"):
        clib.fxGetAppType.argtypes = [
            c.c_uint,
        ]
        clib.fxGetAppType.restype = c.c_int

    # Get read data queue size
    clib.fxGetReadDataQueueSize.argtypes = [
        c.c_uint,
    ]
    clib.fxGetReadDataQueueSize.restype = c.c_int

    if firmwareVersion >= Version("10.0.0"):
        # Get max device name length
        clib.fxGetMaxDeviceNameLength.argtypes = []
        clib.fxGetMaxDeviceNameLength.restype = c.c_int

        # Get device name
        clib.fxGetDeviceTypeNameWrapper.argtypes = [c.c_uint, c.c_char_p]
        clib.fxGetDeviceTypeNameWrapper.restype = c.c_int

        # Get max device side length
        clib.fxGetMaxDeviceSideNameLength.argtypes = []
        clib.fxGetMaxDeviceSideNameLength.restype = c.c_int

        # Get side
        clib.fxGetDeviceSideNameWrapper.argtypes = [c.c_uint, c.c_char_p]
        clib.fxGetDeviceSideNameWrapper.restype = c.c_int

        # Get libs version
        clib.fxGetLibsVersion.argtypes = [
            c.POINTER(c.c_uint16),
            c.POINTER(c.c_uint16),
            c.POINTER(c.c_uint16),
        ]
        clib.fxGetLibsVersion.restype = c.c_int

        # Get max field name length
        clib.fxGetMaxDataLabelLength.argtypes = []
        clib.fxGetMaxDataLabelLength.restype = c.c_int

        # Get fields
        clib.fxGetDataLabelsWrapper.argtypes = [
            c.c_uint,
            c.POINTER(c.POINTER(c.c_char)),
            c.POINTER(c.c_int),
        ]
        clib.fxGetDataLabelsWrapper.restype = c.c_int

        # Get max data elements
        clib.fxGetMaxDataElements.argtypes = []
        clib.fxGetMaxDataElements.restype = c.c_int

        # Request uvlo
        clib.fxRequestUVLO.argtypes = [
            c.c_uint,
        ]
        clib.fxRequestUVLO.restype = c.c_int

        # Read uvlo
        clib.fxGetLastReceivedUVLO.argtypes = [
            c.c_uint,
        ]
        clib.fxGetLastReceivedUVLO.restype = c.c_int

        # Set uvlo
        clib.fxSetUVLO.argtypes = [c.c_uint, c.c_uint]
        clib.fxSetUVLO.restype = c.c_int

        # Get num utts
        clib.fxGetNumUtts.argtypes = []
        clib.fxGetNumUtts.restype = c.c_int

        # Set utts
        clib.fxSetUTT.argtypes = [c.c_uint, c.POINTER(c.c_int), c.c_uint, c.c_byte]
        clib.fxSetUTT.restype = c.c_int

        # Reset utts
        clib.fxSetUTTsToDefault.argtypes = [
            c.c_uint,
        ]
        clib.fxSetUTTsToDefault.restype = c.c_int

        # Save utts
        clib.fxSaveUTTToMemory.argtypes = [
            c.c_uint,
        ]
        clib.fxSaveUTTToMemory.restype = c.c_int

        # Request utts
        clib.fxRequestUTT.argtypes = [
            c.c_uint,
        ]
        clib.fxRequestUTT.restype = c.c_int

        # Get last received utts
        clib.fxGetLastReceivedUTT.argtypes = [c.c_uint, c.POINTER(c.c_int), c.c_uint]
        clib.fxGetLastReceivedUTT.restype = c.c_int

        # IMU Calibration
        clib.fxSetImuCalibration.argtypes = [
            c.c_uint,
        ]
        clib.fxSetImuCalibration.restype = c.c_int

    return clib


# ============================================
#             set_read_functions
# ============================================
def set_read_functions(
    clib: c.CDLL, deviceName: str, isLegacy: bool, deviceType: c.Structure | None
) -> c.CDLL:
    """
    Sets the prototypes for the read and read_all functions. This
    is done here and not with the rest of the prototypes because,
    for legacy devices, we need the device name, which we can't get
    until we call open, for which we need the function prototypes...
    We do it here for non-legacy devices because it's easier than
    passing and worrying about the firmware version to set_prototypes
    """
    if isLegacy:
        if deviceName == "actpack":
            readFunc = getattr(clib, "fxReadDevice")
            readAllFunc = getattr(clib, "fxReadDeviceAll")
        # This also covers XCs, since thoes are reported as exos
        elif deviceName == "exo":
            readFunc = getattr(clib, "fxReadExoDevice")
            readAllFunc = getattr(clib, "fxReadExoDeviceAll")
        elif deviceName == "md":
            readFunc = getattr(clib, "fxReadMdDevice")
            readAllFunc = getattr(clib, "fxReadMdDeviceAll")
        else:
            raise ValueError(f"Unknown device: {deviceName}")

        readFunc.argtypes = [c.c_uint, c.POINTER(deviceType)]
        readFunc.restype = c.c_int
        setattr(clib, "read", readFunc)

        readAllFunc.argtypes = [c.c_uint, c.POINTER(deviceType), c.c_uint]
        readAllFunc.restype = c.c_int
        setattr(clib, "read_all", readAllFunc)

    else:
        readFunc = getattr(clib, "fxReadDevice")
        readFunc.argtypes = [c.c_uint, c.POINTER(c.c_int32), c.POINTER(c.c_int)]
        readFunc.restype = c.c_int
        setattr(clib, "read", readFunc)

        readAllFunc = getattr(clib, "fxReadDeviceAllWrapper")
        readAllFunc.argtypes = [
            c.c_uint,
            c.POINTER(c.POINTER(c.c_int32)),
            c.POINTER(c.c_int),
        ]
        readAllFunc.restype = None
        setattr(clib, "read_all", readAllFunc)

    return clib
