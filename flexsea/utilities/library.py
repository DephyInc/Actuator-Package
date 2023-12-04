import ctypes as c
import os
from pathlib import Path
from typing import Tuple
import zipfile

from botocore.exceptions import EndpointConnectionError
from semantic_version import Version

import flexsea.utilities.constants as fxc

from .aws import s3_download
from .firmware import Firmware
from .system import get_os


# ============================================
#                get_c_library
# ============================================
def get_c_library(
    firmwareVersion: Version, libFile: Path | None, timeout: int = 60
) -> Tuple:
    """
    Loads the correct C library for interacting with the device.

    If we're given a library file to use, we make sure it exists. If
    we're not given a library file to use, we check for a cached file
    on disk corresponding to our firmware version. If we don't have one,
    we try to download it from S3. We then use ctypes to load the library.

    Parameters
    ----------
    firmwareVersion : Version
        The firmware version the library is built to interact with.

    libFile : Path, None
        The path to the local library file to load.

    timeout : int, optional
        Time, in seconds, spent trying to connect to S3 before an
        exception is raised.

    Raises
    ------
    EndpointConnectionError
        If we cannot connect to the internet in order to download the
        necessary library.

    Returns
    -------
    Tuple
        Contains the ``ctypes.CDLL``, the version of the library, and
        the full path to the library file.
    """
    if libFile is None:
        _os = get_os()
        libFile = fxc.libsPath.joinpath(str(firmwareVersion), _os, fxc.libFiles[_os])
        if not libFile.exists():
            libFile.parent.mkdir(parents=True, exist_ok=True)
            libObj = f"{fxc.libsDir}/{firmwareVersion}/{_os}/{libFile.name}"
            try:
                s3_download(
                    libObj, fxc.dephyPublicFilesBucket, str(libFile), None, timeout
                )
            except EndpointConnectionError as err:
                msg = "Error: could not connect to the internet to download the "
                msg += "necessary C library file. Please connect to the internet and "
                msg += "try again."
                print(msg)
                raise err

    clib = _load_clib(libFile, timeout)

    return (_set_prototypes(clib, firmwareVersion), libFile)


# ============================================
#                _load_clib
# ============================================
def _load_clib(libFile: Path, timeout: int = 60) -> c.CDLL:
    """
    Uses ctypes to actually create an interface to the library file. If
    we're on Windows, we have to additionally add several directories to
    the path.
    """
    if not libFile.is_absolute():
        libFile = libFile.expanduser().absolute()
    libFile = str(libFile)

    if "win" in get_os():
        _add_windows_dlls(libFile, timeout)

    return c.cdll.LoadLibrary(libFile)


# ============================================
#            _add_windows_dlls
# ============================================
def _add_windows_dlls(libFile: str, timeout: int = 60) -> None:
    """
    There are several dlls that are required for the precompiled C lib
    to work on Windows. These dlls come packaged with Git Bash, but if
    you're not using Git Bash and you don't have MinGW on your PATH,
    then trying to use the library will error out. As such, here we
    make sure that the necessary dlls are on the system and add them
    to the PATH. If they are not, we download them from S3 and then
    add them to the PATH.
    """
    opSys = get_os()
    dllZip = fxc.dephyPath.joinpath("bootloader_tools", opSys, "win_dlls.zip")
    base = dllZip.name.split(".")[0]
    extractedDest = Path(os.path.dirname(dllZip)).joinpath(base)

    if not dllZip.exists():
        obj = str(Path("bootloader_tools").joinpath(opSys, "win_dlls.zip").as_posix())
        bucket = fxc.dephyPublicFilesBucket
        s3_download(obj, bucket, str(dllZip), timeout=timeout)
        with zipfile.ZipFile(dllZip, "r") as archive:
            archive.extractall(extractedDest)
    os.add_dll_directory(extractedDest.joinpath("git_bash_mingw64", "bin"))
    try:
        os.add_dll_directory(libFile)
    except OSError as err:
        msg = f"Error loading precompiled library: `{libFile}`\n"
        msg += "The most likely cause is a mismatch between the Python, pip and "
        msg += "shell architectures.\nPlease ensure all three are either 32 or 64 "
        msg += "bit.\nKeep different versions isolated by virtual environments.\n"
        print(msg)
        raise err


# ============================================
#               _set_prototypes
# ============================================
def _set_prototypes(clib: c.CDLL, firmwareVersion: Version) -> c.CDLL:
    # pylint: disable=too-many-statements
    # Open
    clib.fxOpen.argtypes = [c.c_char_p, c.c_uint, c.c_uint]
    clib.fxOpen.restype = c.c_int

    clib.fxIsOpen.argtypes = [c.c_uint]
    clib.fxIsOpen.restype = c.c_bool

    # Limited open
    if firmwareVersion >= Version("12.0.0"):
        try:
            clib.fxOpenLimited.argtypes = [c.c_char_p]
            clib.fxOpenLimited.restype = c.c_int
        # v12 changed how versioning works and employs a development version
        # that we do not have access to. Further, the libs were uploaded to S3
        # all under 12.0.0 regardless of development version, so there are some
        # version 12s that don't have this function
        except AttributeError:
            pass

    # Close
    clib.fxClose.argtypes = [
        c.c_uint,
    ]
    clib.fxClose.restype = c.c_uint

    # Start streaming
    clib.fxStartStreaming.argtypes = [c.c_uint, c.c_uint, c.c_bool]
    clib.fxStartStreaming.restype = c.c_int

    clib.fxIsStreaming.argtypes = [c.c_uint]
    clib.fxIsStreaming.restype = c.c_bool

    # Log file specification
    if firmwareVersion >= Version("12.0.0"):
        try:
            clib.fxSetDataLogName.argtypes = [c.c_char_p, c.c_uint]
            clib.fxSetDataLogName.restype = None
            clib.fxSetLogFileSize.argtypes = [c.c_int, c.c_int]
            clib.fxSetLogFileSize.restype = None
            clib.fxSetLogDirectory.argtypes = [c.c_char_p, c.c_uint]
            clib.fxSetLogDirectory.restype = None

        # v12 changed how versioning works and employs a development version
        # that we do not have access to. Further, the libs were uploaded to S3
        # all under 12.0.0 regardless of development version, so there are some
        # version 12s that don't have this function
        except AttributeError:
            pass

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

    # Start training
    clib.fxStartTraining.argtypes = [c.c_uint]
    clib.fxStartTraining.restype = c.c_int

    # Set single user mode (training data is re-used between power cycles)
    clib.fxUseSavedTraining.argtypes = [c.c_uint]
    clib.fxUseSavedTraining.restype = c.c_int

    # Set multi user mode (training data is not re-used between power cycles)
    # Must re-train each time
    clib.fxDoNotUseSaveTraining.argtypes = [c.c_uint]
    clib.fxDoNotUseSaveTraining.restype = c.c_int

    # Is the device in single user mode?
    clib.fxIsUsingSavedTrainingData.argtypes = [c.c_uint, c.POINTER(c.c_bool)]
    clib.fxIsUsingSavedTrainingData.restype = c.c_int

    # Request updated training data from the device
    clib.fxUpdateTrainingData.argtypes = [c.c_uint]
    clib.fxUpdateTrainingData.restype = c.c_int

    # Training steps remaining
    clib.fxGetStepsRemaining.argtypes = [c.c_uint, c.POINTER(c.c_int)]
    clib.fxGetStepsRemaining.restype = c.c_int

    # Get training state
    clib.fxGetTrainingState.argtypes = [c.c_uint, c.POINTER(c.c_int)]
    clib.fxGetTrainingState.restype = c.c_int

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

        # Somehow, it appears 10.1 doesn't have these
        try:
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
            clib.fxGetLastReceivedUTT.argtypes = [
                c.c_uint,
                c.POINTER(c.c_int),
                c.c_uint,
            ]
            clib.fxGetLastReceivedUTT.restype = c.c_int
        except AttributeError:
            print("Warning: could not find UTT methods in library.")

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
    Sets the prototypes for the read and read_all functions.

    Done here and not with the rest of the prototypes because,
    for legacy devices, we need the device name, which we can't get
    until we call open, for which we need the function prototypes...
    We do it here for non-legacy devices because it's easier than
    passing and worrying about the firmware version to set_prototypes

    Parameters
    ----------
    clib : CDLL
        The object on which the prototypes will be set.

    deviceName : str
        The name of the device, e.g., actpack. Used to set the correct
        function.

    isLegacy : bool
        Whether or not the device is a legacy device. The two types
        handle reading quite differently, so we need to know the type
        in order to set the methods appropriately.

    deviceType : Structure, None
        For legacy devices, this includes the fields and data types of
        the device's data.

    Raises
    ------
    ValueError
        If the device type is unknown.

    Returns
    -------
    CDLL
        The library object with the set prototypes.
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
