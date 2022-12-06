from .specs.device_specs import all_devices as fxd


# ============================================
#                Device Names
# ============================================
(INVALID_APP, ACTPACK, EXO) = map(int, range(-1, 2))

deviceNames = {
    ACTPACK: "actpack",
    EXO: "exo",
}


# ============================================
#               Device States
# ============================================
deviceStateDicts = {
    "actpack": fxd.ActPackState(),
    "exo": fxd.EB60State(),
}


# ============================================
#                    Habs
# ============================================
hasHabs = ["exo",]


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
