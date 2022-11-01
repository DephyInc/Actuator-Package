import ctypes as c

from .dev_specs import AllDevices as fxd


# ============================================
#              Motor Controllers
# ============================================
(
    POSITION,
    VOLTAGE,
    CURRENT,
    IMPEDANCE,
    NONE,
    CUSTOM,
    MEAS_RES,
    STALK,
) = map(int, range(8))


# ============================================
#                 Error Codes
# ============================================
(SUCCESS, FAILURE, INVALID_PARAM, INVALID_DEVICE, NOT_STREAMING) = map(int, range(5))


# ============================================
#                  App Types
# ============================================
(INVALID_APP, ACT_PACK, EB5X, MD, NET_MASTER, BMS) = map(int, range(-1, 5))

device_state_dicts = {
    ACT_PACK : fxd.ActPackState(),
    EB5X : fxd.EB5xState(),
    MD : fxd.MD10State(),
    NET_MASTER : fxd.NetMasterState(),
    BMS : fxd.BMSState(),
}

deviceTypes = {
    ACT_PACK : "actpack",
    EB5X : "exoboot",
    MD : "md",
    NET_MASTER : "netmaster",
    BMS : "bms"
}


# ============================================
#                 Bootloader
# ============================================
bootloader_targets = {
    "habs" : 0,
    "re" : 1,
    "ex" : 2,
    "mn" : 3,
    "bt" : 4,
    "xbee" : 5,
}


# ============================================
#                  Firmware
# ============================================
class FW(c.Structure):
    """
    Firmware version
    """

    _fields_ = [
        ("Mn", c.c_uint32),
        ("Ex", c.c_uint32),
        ("Re", c.c_uint32),
        ("Habs", c.c_uint32),
    ]
