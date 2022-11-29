from .specs.device_specs import all_devices as fxd


# ============================================
#                Device Names
# ============================================
(INVALID_APP, ACTPACK) = map(int, range(-1, 1))

deviceNames = {
    ACTPACK: "actpack",
}


# ============================================
#               Device States
# ============================================
deviceStateDicts = {
    "actpack": fxd.ActPackState(),
}


# ============================================
#                    Habs
# ============================================
hasHabs = []


# ============================================
#                 Controllers
# ============================================
controllers = {
    "position": 0,
    "voltage": 1,
    "current": 2,
    "impedance": 3,
    "none": 4,
}


# ============================================
#                 Bootloader
# ============================================
bootloaderTargets = {
    "habs": 0,
    "re": 1,
    "ex": 2,
    "mn": 3,
    "bt": 4,
    "xbee": 5,
}


# ============================================
#                 Error Codes
# ============================================
(SUCCESS, FAILURE, INVALID_PARAM, INVALID_DEVICE, NOT_STREAMING) = map(int, range(5))
