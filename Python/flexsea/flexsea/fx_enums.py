"""
Enum codes
"""
import ctypes as c


# ============================================
#    High Speed Stress/Test Experiments
# ============================================
(HSS_POSITION, HSS_CURRENT, HSS_MIXED) = map(c.c_int, range(3))


# ============================================
#              Motor Controller
# ============================================
(
    FX_POSITION,
    FX_VOLTAGE,
    FX_CURRENT,
    FX_IMPEDANCE,
    FX_NONE,
    FX_CUSTOM,
    FX_MEAS_RES,
    FX_STALK,
) = map(c.c_int, range(8))


# ============================================
#                 Error Codes
# ============================================
(FX_SUCCESS, FX_FAILURE, FX_INVALID_PARAM, FX_INVALID_DEVICE, FX_NOT_STREAMING) = map(
    c.c_int, range(5)
)

# ============================================
#                  App Types
# ============================================
(
    FX_APP_ERROR,
    FX_APP_UNCLASSIFIED,
    FX_APP_ACTPACK,
    FX_APP_ACTPACKPLUS,
    FX_APP_EXO,
    FX_APP_MD,
    FX_APP_NETMASTER,
    FX_APP_BMS,
    FX_APP_HABS,
    FX_APP_CELLSCREENER,
    FX_APP_BATTCYCLER,
) = map(c.c_int, range(0, 11))


# ============================================
#                  Firmware
# ============================================
# pylint: disable=R0903
class FW(c.Structure):
    """Firmware version"""

    _fields_ = [
        ("Mn", c.c_uint32),
        ("Ex", c.c_uint32),
        ("Re", c.c_uint32),
        ("Habs", c.c_uint32),
    ]
