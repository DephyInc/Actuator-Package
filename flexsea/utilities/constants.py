import ctypes as c
from pathlib import Path

import semantic_version as sem

# ============================================
#             Path Configuration
# ============================================

# All dephy-related files are stored here (libs, firmware, device
# specs, api specs, and bootloading tools)
dephyPath = Path.home().joinpath(".dephy").expanduser().absolute()

# libsDir is the name of the directory (mirrored on S3), whereas
# libsPath is the full path to that directory on the local file system
libsDir = "precompiled_c_libs"
libsPath = dephyPath.joinpath(libsDir)

# Each operating system potentially has its own library file name
libFiles = {
    "windows_64bit": "libfx_plan_stack.dll",
    "windows_32bit": "libfx_plan_stack.dll",
    "linux_64bit": "libfx_plan_stack.so",
    "linux_32bit": "libfx_plan_stack.so",
}

# legacyDeviceSpecsDir is the name of the directory (mirrored on S3), whereas
# legacyDeviceSpecsPath is the full path to that directory on the local file system
legacyDeviceSpecsDir = "legacy_device_specs"
legacyDeviceSpecsPath = dephyPath.joinpath(legacyDeviceSpecsDir)


# ============================================
#              S3 Configuration
# ============================================

# This bucket is public and holds all of the pre-compiled c libraries, device
# specs, api specs, and bootloader tools
dephyPublicFilesBucket = "dephy-public-files"


# ============================================
#           Version Configuration
# ============================================

# Firmware before this version had a very different communication protocol,
# method of reading data, did not contain device side information, the
# libraries did not have information about their own version, different device
# error codes, and a different way of obtaining the device name. We call
# devices with firmware prior to this cutoff legacy devices
legacyCutoff = sem.Version("10.0.0")


# ============================================
#                 Constants
# ============================================
baudRate = 230400
minHeartbeat = 50


# ============================================
#                 Controllers
# ============================================

# These values are used by the fxSendMotorCommand function to tell the firmware
# what quantity we are trying to command
controllers = {
    "position": c.c_int(0),
    "voltage": c.c_int(1),
    "current": c.c_int(2),
    "impedance": c.c_int(3),
    "none": c.c_int(4),
}


# ============================================
#                 Bootloader
# ============================================

# These values are used to tell the firmware which chip we're trying to flash
bootloaderTargets = {
    "habs": 0,
    "re": 1,
    "ex": 2,
    "mn": 3,
    "bt": 4,
    "xbee": 5,
}


# ============================================
#                Error Codes
# ============================================

# These values encode the meaning of the various return values for the
# C functions being called from the library
deviceErrorCodes = {
    "UNDEFINED": c.c_int(0),
    "SUCCESS": c.c_int(1),
    "FAILURE": c.c_int(2),
    "INVALID_PARAM": c.c_int(3),
    "INVALID_DEVICE": c.c_int(4),
    "NOT_STREAMING": c.c_int(5),
}

legacyDeviceErrorCodes = {
    "SUCCESS": c.c_int(0),
    "FAILURE": c.c_int(1),
    "INVALID_PARAM": c.c_int(2),
    "INVALID_DEVICE": c.c_int(3),
    "NOT_STREAMING": c.c_int(4),
}


# ============================================
#                    Habs
# ============================================

# It's easier to list the devices that don't have habs
noHabs = [
    "actpack",
]


# ============================================
#                Device Names
# ============================================

# Only applies to legacy devices. These values encode the name of the device
INVALID_APP = c.c_int(-1)
ACTPACK = c.c_int(0)
EXO = c.c_int(1)  # XCs are reported as exos
MD = c.c_int(2)  # NOTE: This is only true for v9.1. For < 9.1, it's
# NetMaster, but those devices are not in the wild

deviceNames = {
    ACTPACK.value: "actpack",
    EXO.value: "exo",
    MD.value: "md",
}
