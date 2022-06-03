"""
Loads the pre-compiles C libraries.
"""
import ctypes as c
import os
import platform

from .dev_spec import AllDevices as fxd
from . import fx_enums as fxe


__version__ = "8.1.0"


# ============================================
#                  _get_os
# ============================================
def _get_os() -> str:
	"""
	Determines which operating system we're running on.

	Returns
	-------
	str:
		The name of the operating system. Matches the directory inside
		`libs` containing the c libraries appropriate for that OS.
	"""
	operating_system = "linux"
	# Windows
	if "win" in platform.system().lower():
		# 32 bit
		if platform.architecture()[0] == "32bit":
			operating_system = "win32"
		# 64 bit
		else:
			operating_system = "win64"
	# Pi - 32 bit
	elif os.uname().machine.startswith("arm"):
		operating_system = "raspberryPi"
	# Pi - 64 bit
	elif os.uname().machine.startswith("aarch64"):
		operating_system = "raspberryPi64"
	else:
		raise OSError("Unknown operating system!")
	return operating_system


# ============================================
#                  _add_dlls
# ============================================
def _add_dlls(lib_path: str) -> None:
	"""
	Explicitly adds the appropriate directories to the `PATH` on Windows.

	Parameters
	----------
	lib_path : str
		The full path to the directory containing the Windows
		precompiled libraries.
	"""
	for extra_path in os.environ["PATH"].split(";"):
		if os.path.exists(extra_path) and "mingw" in extra_path:
			os.add_dll_directory(extra_path)
	os.add_dll_directory(lib_path)


# ============================================
#             _set_data_types
# ============================================
def _set_data_types(clib: c.CDLL) -> c.CDLL:
	"""
	Defines the function prototypes.

	Parameters
	----------
	clib : c.CDLL
		The Python object interfacing with the C libraries we're
		setting the prototypes for.

	Returns
	-------
	clib : c.CDLL
		The Python object interfacing with the C libraries for which
		we've set the prototypes.
	"""
	clib.fxOpen.argtypes = [c.c_char_p, c.c_uint, c.c_uint]
	clib.fxOpen.restype = c.c_int

	clib.fxIsOpen.argtypes = [c.c_uint]
	clib.fxIsOpen.restype = c.c_bool

	clib.fxClose.argtypes = [c.c_uint]
	clib.fxClose.restype = c.c_int

	clib.fxCloseAll.argtypes = []
	clib.fxCloseAll.resType = []

	clib.fxGetDeviceIds.argtypes = [c.POINTER(c.c_int), c.c_uint]

	clib.fxStartStreaming.argtypes = [c.c_uint, c.c_uint, c.c_bool]
	clib.fxStartStreaming.restype = c.c_int

	clib.fxStopStreaming.argtypes = [c.c_uint]
	clib.fxStopStreaming.restype = c.c_int

	clib.fxReadDevice.argtypes = [c.c_uint, c.POINTER(fxd.ActPackState)]
	clib.fxReadDevice.restype = c.c_int

	clib.fxReadDeviceAll.argtypes = [
		c.c_uint,
		c.POINTER(fxd.ActPackState),
		c.c_uint,
	]
	clib.fxReadDeviceAll.restype = c.c_int

	clib.fxReadMdDeviceAll.argtypes = [
		c.c_uint,
		c.POINTER(fxd.MD10State),
		c.c_uint,
	]
	clib.fxReadMdDeviceAll.restype = c.c_int
	clib.fxReadMdDevice.argtypes = [c.c_uint, c.POINTER(fxd.MD10State)]
	clib.fxReadMdDeviceAll.restype = c.c_int

	clib.fxReadNetMasterDevice.argtypes = [c.c_uint, c.POINTER(fxd.NetMasterState)]
	clib.fxReadDevice.restype = c.c_int

	clib.fxReadNetMasterDeviceAll.argtypes = [
		c.c_uint,
		c.POINTER(fxd.NetMasterState),
		c.c_uint,
	]
	clib.fxReadNetMasterDeviceAll.restype = c.c_int

	clib.fxSetReadDataQueueSize.argtypes = [c.c_uint, c.c_uint]
	clib.fxSetReadDataQueueSize.restype = c.c_uint

	clib.fxGetReadDataQueueSize.argtypes = [c.c_uint]
	clib.fxGetReadDataQueueSize.restype = c.c_int

	clib.fxSetGains.argtypes = [
		c.c_uint,
		c.c_uint,
		c.c_uint,
		c.c_uint,
		c.c_uint,
		c.c_uint,
		c.c_uint,
	]
	clib.fxSetGains.restype = c.c_int

	clib.fxSendMotorCommand.argtypes = [c.c_uint, c.c_int, c.c_int]
	clib.fxSendMotorCommand.restype = c.c_int

	clib.fxGetAppType.argtypes = [c.c_uint]

	clib.fxActivateBootloader.argtypes = [c.c_uint, c.c_uint8]
	clib.fxActivateBootloader.restype = c.c_int

	clib.fxIsBootloaderActivated.argtypes = [c.c_uint]
	clib.fxIsBootloaderActivated.restype = c.c_int

	clib.fxRequestFirmwareVersion.argtypes = [c.c_uint]
	clib.fxRequestFirmwareVersion.restype = c.c_int

	clib.fxGetLastReceivedFirmwareVersion.argtypes = [c.c_uint]
	clib.fxGetLastReceivedFirmwareVersion.restype = fxe.FW

	return clib


# ============================================
#                 _load_clib
# ============================================
def _load_clib() -> c.CDLL:
	"""
	Uses `ctypes` to load the appropriate C libraries depending on the
	OS.

	Raises
	------
	OSError:
		Raised if the precompiled libraries fail to load.

	Returns
	-------
	clib : ctypes.cdll.CDLL
		The Python object from which we can call the flexsea C
		functions.
	"""
	nix_lib = "libfx_plan_stack.so"
	win_lib = "libfx_plan_stack.dll"
	libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs")
	os.environ["PATH"] += libs_path

	operating_system = _get_os()
	lib_path = os.path.join(libs_path, operating_system)

	if "win" in operating_system:
		try:
			_add_dlls(lib_path)
			clib = c.cdll.LoadLibrary(os.path.join(lib_path, win_lib))
		except OSError as err:
			msg = f"\n[!] Error loading the {win_lib} precompiled libraries.\n"
			msg += (
				"The most likely cause is a mismatch between the Python, pip and shell "
				"architectures.\n"
			)
			msg += "To solve this, ensure all three are either 32 or 64 bit.\n"
			msg += "Keep different versions isolated by virtual environments.\n"
			msg += "For additional help, follow the installation instructions here: "
			msg += "https://github.com/DephyInc/Actuator-Package\n"
			msg += "--------------------------------------------\n\n"
			msg += f"Detailed error message for debugging:\n{err}\n"
			print(msg)
	else:
		clib = c.cdll.LoadLibrary(os.path.join(lib_path, nix_lib))

	return _set_data_types(clib)


# ============================================
#                    main
# ============================================
_clib = _load_clib()
