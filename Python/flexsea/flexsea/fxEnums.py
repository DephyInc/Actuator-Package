"""
Enum codes
"""
# pylint: disable=invalid-name
import ctypes as c

# High Speed Stress/Test Experiments:
(HSS_POSITION, HSS_CURRENT, HSS_MIXED) = map(c.c_int, range(3))

# Motor Controller
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

# Error Code
(FX_SUCCESS, FX_FAILURE, FX_INVALID_PARAM, FX_INVALID_DEVICE, FX_NOT_STREAMING) = map(
	c.c_int, range(5)
)

# App Type
(FX_INVALID_APP, FX_ACT_PACK, FX_EB5X, FX_NET_MASTER, FX_BMS) = map(
	c.c_int, range(-1, 4)
)

class FW(c.Structure):
	_fields_ = [("Mn", c.c_uint32), ("Ex", c.c_uint32), ("Re", c.c_uint32), ("Habs", c.c_uint32)]
