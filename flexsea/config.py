import ctypes as c
from pathlib import Path

from .dev_specs import AllDevices as fx_devs


# ============================================
#              Path Configuration
# ============================================
cacheDir = Path.joinpath(Path.home(), ".dephy", "flexsea")
libsDir = cacheDir.joinpath("libs")


# ============================================
#              S3 Configuration
# ============================================
libsBucket = "dephy-public-binaries"


# ============================================
#               Read Functions
# ============================================
read_functions = {
    "actpack" : {
        "name" : "fxReadDevice",
        "args" : [c.c_uint, c.POINTER(fx_devs.ActPackState)],
        "return" : c.c_int,
        "all_name" : "fxReadDeviceAll",
        "all_args" : [c.c_uint, c.POINTER(fx_devs.ActPackState), c.c_uint],
        "all_return" : c.c_int
    },
}
