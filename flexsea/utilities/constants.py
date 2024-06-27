import ctypes as c
from pathlib import Path

import semantic_version as sem

# ============================================
#             Path Configuration
# ============================================

# All dephy-related files are stored here (libs, firmware, device
# specs, api specs, and bootloading tools)
dephyPath = Path.home().joinpath(".dephy").expanduser().absolute()

firmwareVersionCacheFile = dephyPath.joinpath("available_versions.yaml")

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
    "pi_64bit": "libfx_plan_stack.so",
    "pi_32bit": "libfx_plan_stack.so",
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

# On Windows, several dll files from mingw are needed in order for the
# library to work correctly
winDllsDir = "win_dlls"
winDllsPath = dephyPath.joinpath(winDllsDir)


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
#              Training States
# ============================================
training_states = {
    0: "loading",
    1: "in_progress",
    2: "done",
    3: "walk_training_in_progress",
    4: "run_training_in_progress",
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
    "bt121": 4,
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


# ============================================
#                   UTTs
# ============================================
# This isn't great, but getting the number of UTTs depends on a function that
# was introduced in version 10, but it turns out the UTT functions themselves
# were available before then. However, when trying to use the utt functions
# from version 9, we still need to know how many there are, so, since we're
# past v9, the number of UTTs is fixed, so we hard code it here, though it makes
# me sad to do so
nUttsV9 = 15


# ============================================
#               Battery Types
# ============================================
BATTERY_TYPE_UNKNOWN = c.c_int(0)
BATTERY_TYPE_6_CELL = c.c_int(1)
BATTERY_TYPE_8_CELL = c.c_int(2)
BATTERY_TYPE_10_CELL = c.c_int(3)
BATTERY_TYPE_11_CELL = c.c_int(4)
BATTERY_TYPE_12_CELL = c.c_int(5)
POWER_SUPPLY = c.c_int(6)

batteryTypes = {
    BATTERY_TYPE_UNKNOWN.value: "unknown",
    BATTERY_TYPE_6_CELL.value: "6 cell",
    BATTERY_TYPE_8_CELL.value: "8 cell",
    BATTERY_TYPE_10_CELL.value: "10 cell",
    BATTERY_TYPE_11_CELL.value: "11 cell",
    BATTERY_TYPE_12_CELL.value: "12 cell",
    POWER_SUPPLY.value: "power supply",
}


# ============================================
#               LED Sequences
# ============================================
UNIDENTIFIED_LED_SEQUENCE = c.c_int(0)
SET_GREEN_BREATHE = c.c_int(1)
SET_RED_BREATHE = c.c_int(2)
SET_CYAN_BREATHE = c.c_int(3)
SET_BLUE_BREATHE = c.c_int(4)
SET_WHITE_BREATHE = c.c_int(5)
SET_YELLOW_BREATHE = c.c_int(6)
SET_GREEN_ON = c.c_int(7)
SET_YELLOW_ON = c.c_int(8)
SET_RED_ON = c.c_int(9)
SET_CYAN_ON = c.c_int(10)
SET_CYLON = c.c_int(11)
SET_RED_FADE = c.c_int(12)
SET_YELLOW_FADE = c.c_int(13)
SET_GREEN_FADE = c.c_int(14)
SET_TO_DISPLAY_BATTERY_LEVEL = c.c_int(15)
SET_TO_WHITE_BLINK = c.c_int(16)
ALL_LEDS_OFF = c.c_int(17)

ledSequences = {
    UNIDENTIFIED_LED_SEQUENCE.value: "uidentified",
    SET_GREEN_BREATHE.value: "green breathe",
    SET_RED_BREATHE.value: "red breathe",
    SET_CYAN_BREATHE.value: "cyan breathe",
    SET_BLUE_BREATHE.value: "blue breathe",
    SET_WHITE_BREATHE.value: "white breathe",
    SET_YELLOW_BREATHE.value: "yellow breathe",
    SET_GREEN_ON.value: "green on",
    SET_YELLOW_ON.value: "yellow on",
    SET_RED_ON.value: "red on",
    SET_CYAN_ON.value: "cyan on",
    SET_CYLON.value: "cylon",
    SET_RED_FADE.value: "red fade",
    SET_YELLOW_FADE.value: "yellow fade",
    SET_GREEN_FADE.value: "green fade",
    SET_TO_DISPLAY_BATTERY_LEVEL.value: "display battery level",
    SET_TO_WHITE_BLINK.value: "white blink",
    ALL_LEDS_OFF.value: "all off",
}
