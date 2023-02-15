import ctypes as c


# ============================================
#                  Firmware
# ============================================
class Firmware(c.Structure):
    """
    Holds the integer values representing the firmware versions of
    each microcontroller as returned from the C library. These need to
    be decoded before they make sense.
    """

    _fields_ = [
        ("mn", c.c_uint32),
        ("ex", c.c_uint32),
        ("re", c.c_uint32),
        ("habs", c.c_uint32),
    ]
