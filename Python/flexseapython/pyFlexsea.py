from ctypes import *
import os
import sys
import platform
from enum import Enum

global flexsea

################### Motor Controller Enums #######################

(EPosition,
 EVoltage,
 ECurrent,
 EImpedance) = map(c_int, range(4))

###################### Error Code Enums ##########################

(ESuccess,
 EFailure,
 EInvalidParam,
 EInvalidDevice,
 ENotStreaming,
 EStreamFailed,
 ENoReadData) = map(c_int, range(7))

##################### Redefine ExoState Structure #################
# See "Exo.h" for C definition

MAX_STRING_LENGTH = 32

class GenericVariables(Structure):
	_fields_ = [("_gv0", c_long),
		("_gv1", c_long),
		("_gv2", c_long),
		("_gv3", c_long),
		("_gv4", c_long),
		("_gv5", c_long),
		("_gv6", c_long),
		("_gv7", c_long),
		("_gv8", c_long),
		("_gv9", c_long)]


class ImuData(Structure):
	_fields_ = [("_accelx", c_long),
		("_accely", c_long),
		("_accelz", c_long),
		("_gyrox", c_long),
		("_gyroy", c_long),
		("_gyroz", c_long)]

class ManageState(Structure):
	_fields_ = [("_status", c_ulong),
		("_software_version_len", c_int),
		("_software_version", c_char * MAX_STRING_LENGTH),
		("_imu", ImuData),
		("_ankle_angle", c_long),
		("_ankle_angle_velocity", c_long)]

class MotorData(Structure):
	_fields_ = [("_motor_angle", c_long),
		("_motor_velocity", c_long),
		("_motor_acceleration", c_long),
		("_motor_current", c_long),
		("_motor_voltage", c_long)]

class ExecuteState(Structure):
	_fields_ = [("_status", c_ulong),
		("_motor_data", MotorData),
		("_software_version_len", c_int),
		("_software_version", c_char * MAX_STRING_LENGTH)]

class BatteryData(Structure):
	_fields_ = [("_battery_voltage", c_ulong),
		("_battery_current", c_long),
		("_battery_temperature", c_long)]

class RegulateState(Structure):
	_fields_ = [("_status", c_ulong),
		("_battery", BatteryData),
		("_software_version_len", c_int),
		("_software_version", c_char * MAX_STRING_LENGTH)]

class ExoState(Structure):
	_fields_ = [("_timestamp", c_ulong),
	        ("_board_id", c_ulong),
		("_manage", ManageState),
		("_execute", ExecuteState),
		("_regulate", RegulateState),
		("_genvars", GenericVariables)]

####################### Begin API ##################################

### Device ID is an alphanumeric ID used to refer to a specific FlexSEA device.
### Device ID is returned by fxOpen upon establishing a connection with a 
### FlexSEA device, and is used by most of the functions in this library to 
### specify which device to run that function on.

def fxOpen(port, baudRate, frequency = 100, logLevel = 4):
	"""
	Establish a connection with a FlexSEA device.

	Parameters:
	portName (string): The name of the serial port to open (e.g. "COM3")

	baudRate (int): The baud rate used i.e. 115200, 230400, etc.

	frequency (int): The frequency of communcation with the FlexSEA device. 
	This applies for streaming device data as well as sending commands to the 
	device.

	logLevel (int): is the logging level for this device. 0 is most verbose and
	6 is the least verbose. Values greater than 6 are floored to 6.
	
	Raises:
	IOError if we fail to open the device.
	"""
	global flexsea

	devId = flexsea.fxOpen(port.encode('utf-8'), baudRate, frequency, logLevel)

	if (devId == -1):
		raise IOError('Failed to open device')

	return devId

def fxClose(devId):
	"""
	Disconnect from a FlexSEA device with the given device ID.
	
	Parameters:
	devId (int): The ID of the device to close
	
	Raises:
	ValueError if the device ID is invalid
	"""
	global flexsea
	retCode = flexsea.fxClose(devId)
	if (retCode == EInvalidDevice):
		raise ValueError('fxClose: invalid device ID')

def fxGetDeviceIds():
	"""
	Get the device IDs of all connected FlexSEA devices. 
	
	The device ID is used by the functions in this API to specify which 
	FlexSEA device to communicate with. The C library requires a fixed
	array so we give a size of n = 10 but feel free to increase this.

	Returns:
	A list containing either valid device IDs or -1 (invalid device).
	"""
	global flexsea
	n = 10
	l = [-1] * 10
	c_l, c_n = list_to_int_arr(l)
	flexsea.fxGetDeviceIds(c_l, c_n)
	asList = c_l[:n]
	asList = asList[: asList.index(-1) ]
	return asList

def fxStartStreaming(devId, shouldLog):
	"""
	Start streaming data from a FlexSEA device.

	Parameters:
	devId (int): The device ID 

	shouldLog (bool): If set true, the program logs all received data to
	a file.

	The name of the file is formed as follows:

	< FlexSEA model >_id< device ID >_< date and time >.csv

	for example:

	rigid_id3904_Tue_Nov_13_11_03_50_2018.csv

	The file is formatted as a CSV file. The first line of the file will be 
	headers for all columns. Each line after that will contain the data read 
	from the device.
	
	Raises:
	ValueError if the device ID is invalid
	RuntimeError if the stream failed
	"""
	global flexsea

	if (shouldLog == True):
		retCode = flexsea.fxStartStreaming(devId, 1)
	else:
		retCode = flexsea.fxStartStreaming(devId, 0)

	if (retCode == EInvalidDevice):
		raise ValueError('fxStartStreaming: invalid device ID')
	elif (retCode == EFailure):
		raise RuntimeError('fxStartStreaming: stream failed')

def fxStopStreaming(devId):
	"""
	Stop streaming data from a FlexSEA device.

	Parameters:
	devId (int): Is the device ID 
	"""
	global flexsea
	flexsea.fxStopStreaming(devId)

def fxSetCommunicationFrequency(devId, frequency):
	"""
	Set the communication frequency with the FlexSEA device. This
	applies for streaming device data as well as sending commands to the
	device.

	Parameters:
	devId (int): The device ID

	frequency (int): The desired frequency of communication

	Raises:
	ValueError if invalid device ID
	"""
	global flexsea
	if (flexsea.fxSetCommuncationFrequency(devId, frequency) == EInvalidDevice):
		raise ValueError('fxSetCommunicationFrequency: invalid device ID')

def fxReadDevice(devId):
	"""
	Read the most recent data from a streaming FlexSEA device stream.
	IMPORTANT! Must call fxStartStreaming before calling this.

	Parameters:
	devId (int): The device ID of the device to read from.

	Returns:
	exoState (ExoState): Contains the most recent data from the device

	Raises:
	ValueError if invalid device ID
	RuntimeError if no read data
	"""
	global flexsea

	exoState = ExoState();
	retCode = flexsea.fxReadDevice(devId, byref(exoState))
	
	if (retCode == EInvalidDevice):
		raise ValueError('fxReadDevice: invalid device ID')
	elif (retCode == ENoReadData):
		raise RuntimeError('fxReadDevice: no read data')

	return exoState 

def fxSetGains(devId, g0, g1, g2, g3):
	"""
	Sets the gains used by PID controllers on the FlexSEA device.
	
	Parameters:
	devId (int): The device ID.

	g0 (int): Proportional gain (Kp) 

	g1 (int): Integral gain (Ki)

	g2 (int): Stiffness (K) (used in impedence control only)

	g3 (int): Damping (B) (used in impedance control only)

	Raises:
	ValueError if the device ID is invalid
	"""
	global flexsea
	retCode = flexsea.fxSetGains(devId, g0, g1, g2, g3)
		
	if (retCode == EInvalidDevice):
		raise ValueError('fxSetGains: invalid device ID')

def fxSendMotorCommand(devId, controlType, value):
	"""
	Send a command to the device.
	
	Parameters:
	devId (int): The device ID.

	controlMode (c_int): The control mode we will use to send this command.
	Possible values are: EPosition, ECurrent, EVoltage, EImpedence

	value (int): The value to use for the controlMode. 
	EPosition - encoder value
	ECurrent - current in mA
	EVoltage - voltage in mV
	EImpedence - current in mA
	
	Raises:
	ValueError if invalid device ID
	ValueError if invalid controlType
	"""
	global flexsea

	retCode = flexsea.fxSendMotorCommand(devId, controlType, c_int(int(value)))

	if (retCode == EInvalidDevice):
		raise ValueError('fxSendMotorCommand: invalid device ID')
	if (retCode == EFailure):
		raise IOError('fxSendMotorCommand: command failed')	
	if (retCode == EInvalidParam):
		raise ValueError('fxSendMotorCommand: invalid controlType')	



# Loads the library from the c lib
def loadFlexsea():
	global flexsea
	#Init code:
	print('[pyFlexsea Module]\n')

	loadSucceeded  = False
	is_64bits = sys.maxsize > 2**32
	sysOS = platform.system().lower()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	# we currently support Ubuntu and Raspbian so need to make sure we are pulling
	# in correct library depending on which version of linux
	linux_distro = platform.linux_distribution()[0]
	# check whether we are running on a 32 or 64 bit machine
	architecture = platform.architecture()[0]
	librarypath=""
	print(platform)
	if("win" in sysOS):
		# load proper library based on host architecture
		if architecture == "32bit":
			lpath_base = os.path.join(dir_path,'../../fx_plan_stack/libs/win32')
		else:
			lpath_base = os.path.join(dir_path,'../../fx_plan_stack/libs/win64')
		librarypath = os.path.join(lpath_base,'libfx_plan_stack.dll')
	elif("Ubuntu" in linux_distro):
		lpath_base = os.path.join(dir_path,'../../fx_plan_stack/libs/linux')
		librarypath = os.path.join(lpath_base,'libfx_plan_stack.so')
	else:
		# TODO: as of now we'll assume we're compiling for a raspberry Pi if it's not Ubuntu
		# or windows but we'll likely want to make OS library versions clearer
		lpath_base = os.path.join(dir_path,'../../fx_plan_stack/libs/raspberryPi')
		librarypath = os.path.join(lpath_base,'libfx_plan_stack.so')

	try:
		print("loading... " + librarypath)
		flexsea = cdll.LoadLibrary(librarypath)
	except OSError as arg:
		print( "\n\nThere was a problem loading the library\n {0}\n".format(arg))
	else:
		loadSucceeded  = True

	if(loadSucceeded  != True):
		return False

	print("Loaded!")
	
	# set arg types
	flexsea.fxOpen.argtypes = [c_char_p, c_uint, c_uint, c_uint]
	flexsea.fxOpen.restype = c_int
	
	flexsea.fxClose.argtypes = [c_uint]
	flexsea.fxClose.restype = c_int

	flexsea.fxGetDeviceIds.argtypes = [POINTER(c_int), c_uint]

	flexsea.fxStartStreaming.argtypes = [c_uint, c_bool]
	flexsea.fxStartStreaming.restype = c_int
	
	flexsea.fxStopStreaming.argtypes = [c_uint]
	flexsea.fxStopStreaming.restype = c_int

	flexsea.fxSetCommunicationFrequency.argtypes = [c_uint, c_uint]
	flexsea.fxSetCommunicationFrequency.restype = c_int

	flexsea.fxReadDevice.argtypes = [c_uint, POINTER(ExoState)]
	flexsea.fxReadDevice.restype = c_int

	flexsea.fxSetGains.argtypes = [c_uint, c_uint, c_uint, c_uint, c_uint]
	flexsea.fxSetGains.restype = c_int

	flexsea.fxSendMotorCommand.argtypes = [c_uint, c_int, c_int]
	flexsea.fxSendMotorCommand.restype = c_int

	return True

def list_to_int_arr(l):
	c_arr = (c_int * len(l))(*l)
	c_len = c_int(len(l))
	return c_arr, c_len

