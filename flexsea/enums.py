import ctypes as c

from .specs.device_specs import all_devices as fxd


# ============================================
#                Device Names
# ============================================
(INVALID_APP, ACTPACK, EXO) = map(c.c_int, range(-1, 2))

deviceNames = {
    ACTPACK.value: "actpack",
    EXO.value: "exo",
}


# ============================================
#               Device States
# ============================================
deviceStateDicts = {
    "actpack": fxd.ActPackState,
    "exo": fxd.EB60State,
}


# ============================================
#                    Habs
# ============================================
hasHabs = [
    "exo",
]

hasHabsLegacy = [
    "exo",
]


# ============================================
#                 Controllers
# ============================================
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
(SUCCESS, FAILURE, INVALID_PARAM, INVALID_DEVICE, NOT_STREAMING) = map(
    c.c_int, range(5)
)
