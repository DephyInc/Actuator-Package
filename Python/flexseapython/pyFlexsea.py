from ctypes import *
import os
import sys
import platform
from enum import Enum

global flexsea

################### Motor Controller Enums #######################

(FxPosition,
 FxVoltage,
 FxCurrent,
 FxImpedance) = map(c_int, range(4))

###################### Error Code Enums ##########################

(FxSuccess,
 FxFailure,
 FxInvalidParam,
 FxInvalidDevice,
 FxNotStreaming) = map(c_int, range(5))

###################### App Type Enums #############################

(FxInvalidApp,
 FxActPack,
 FxExo,
 FxNetMaster,
 FxBMS) = map(int, range(-1,4))

##################### Redefine ActPackState Structure #################
# See "actpack_struct.h" for C definition

class ActPackState(Structure):
	_fields_ = [
			("rigid"	  , c_int),
			("id"		  , c_int),
			("timestamp"	  , c_int),
			("accelx"	  , c_int),
			("accely"	  , c_int),
			("accelz"	  , c_int),
			("gyrox"	  , c_int),
			("gyroy"	  , c_int),
			("gyroz"	  , c_int),
			("encoderAngle"   , c_int),
			("encoderVelocity", c_int),
			("encoderAccel"   , c_int),
			("motorCurrent"   , c_int),
			("motorVoltage"   , c_int),
			("batteryVoltage" , c_int),
			("batteryCurrent" , c_int),
			("batteryTemp" 	  , c_int),
			("deviceStatus"   , c_int),
			("motorStatus"	  , c_int),
			("batteryStatus"  , c_int),
			("genVar"    , c_int * 10),
			("ankleAngle"	  , c_int),
			("ankleVelocity"  , c_int)]

class NetNodeState(Structure):
	_fields_ = [
			("accelx"	  , c_int),
			("accely"	  , c_int),
			("accelz"	  , c_int),
			("gyrox"	  , c_int),
			("gyroy"	  , c_int),
			("gyroz"	  , c_int),
			("pressure"	  , c_int),
			("status"	  , c_int)]

class NetMasterState(Structure):
	_fields_ = [
			("netmaster"	  , c_int),
			("id"		  , c_int),
			("timestamp"	  , c_int),
			("genvar"     , c_int * 4),
			("status"	  , c_int),
			("netNode", NetNodeState * 8)]

class BMSState(Structure):
	_fields_ = [
			("bms" 		  , c_int),
			("id"		  , c_int),
			("timestamp"	  , c_int),
			("cellVoltage"     , c_int * 9),
			("status"	  , c_int),
			("current"	  , c_int),
			("timer"	  , c_int),
			("balancing"	  , c_int),
			("stackVoltage"	  , c_int),
			("packImbalance"  , c_int),
			("temperature"	  , c_int * 4),
			("genvar", c_int * 4)]


####################### Begin API ##################################

### Device ID is an alphanumeric ID used to refer to a specific FlexSEA device.
### Device ID is returned by fxOpen upon establishing a connection with a
### FlexSEA device, and is used by most of the functions in this library to
### specify which device to run that function on.

def fxOpen(port, baudRate, logLevel = 4):
	"""
	Establish a connection with a FlexSEA device.

	Parameters:
	portName (string): The name of the serial port to open (e.g. "COM3")

	baudRate (int): The baud rate used i.e. 115200, 230400, etc.

	logLevel (int): is the logging level for this device. 0 is most verbose and
	6 is the least verbose. Values greater than 6 are floored to 6.

	Raises:
	IOError if we fail to open the device.
	"""
	global flexsea

	devId = flexsea.fxOpen(port.encode('utf-8'), baudRate, logLevel)

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
	if (retCode == FxInvalidDevice):
		raise ValueError('fxClose: invalid device ID')

def fxCloseAll():
	"""
	Disconnect from all FlexSEA devices
	"""
	global flexsea
	flexsea.fxCloseAll()

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

def fxStartStreaming(devId, frequency, shouldLog):
	"""
	Start streaming data from a FlexSEA device.

	Parameters:
	devId (int): The device ID

	frequency (int): The desired frequency of communication

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
		retCode = flexsea.fxStartStreaming(devId, frequency, 1)
	else:
		retCode = flexsea.fxStartStreaming(devId, frequency, 0)

	if (retCode == FxInvalidDevice):
		raise ValueError('fxStartStreaming: invalid device ID')
	elif (retCode == FxFailure):
		raise RuntimeError('fxStartStreaming: stream failed')

def fxStopStreaming(devId):
	"""
	Stop streaming data from a FlexSEA device.

	Parameters:
	devId (int): Is the device ID
	"""
	global flexsea

	retCode = flexsea.fxStopStreaming(devId)
	if (retCode == FxInvalidDevice):
		raise ValueError('fxStopStreaming: invalid device ID')
	elif (retCode == FxFailure):
		raise RuntimeError('fxStopStreaming: stream failed')


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

	actPackState = ActPackState();
	retCode = flexsea.fxReadDevice(devId, byref(actPackState))

	if (retCode == FxInvalidDevice):
		raise ValueError('fxReadDevice: invalid device ID')
	elif (retCode == FxNotStreaming):
		raise RuntimeError('fxReadDevice: no read data')

	return actPackState


def fxReadDeviceAll(devId, dataQueueSize):
	"""
	Read all data from a streaming FlexSEA device stream.
	MUST call fxStartStreaming before calling this.

	Parameters:
	devId: Device ID of the device to read from.

	dataQueueSize: Size of readData.

	Raise:
	ValueError if invalid device ID

	Return:
	Actual number of entries read. You will probably need to use this number.
	"""
	global flexsea

	actPackStateDataQueue = [ActPackState() for count in range(dataQueueSize)];

	itemsRead = flexsea.fxReadDeviceAll(devId, byref(actPackStateDataQueue), dataQueueSize)
	if (itemsRead == -1):
		raise ValueError('fxGetReadDataQueueSize: Invalid device ID')
	return itemsRead

def fxReadNetMasterDevice(devId):
	"""
	Read the most recent data from a streaming FlexSEA NetMaster device stream.
	IMPORTANT! Must call fxStartStreaming before calling this.

	Parameters:
	devId (int): The device ID of the device to read from.

	Returns:
	netMasterState (NetMasterState): Contains the most recent data from the device

	Raises:
	ValueError if invalid device ID
	RuntimeError if no read data
	"""
	global flexsea

	netMasterState = NetMasterState();
	retCode = flexsea.fxReadNetMasterDevice(devId, byref(netMasterState))

	if (retCode == FxInvalidDevice):
		raise ValueError('fxReadDevice: invalid device ID')
	elif (retCode == FxNotStreaming):
		raise RuntimeError('fxReadDevice: no read data')

	return netMasterState

def fxReadBMSDevice(devId):
	"""
	Read the most recent data from a streaming FlexSEA BMS device stream.
	IMPORTANT! Must call fxStartStreaming before calling this.

	Parameters:
	devId (int): The device ID of the device to read from.

	Returns:
	bmsState (BMSState): Contains the most recent data from the device

	Raises:
	ValueError if invalid device ID
	RuntimeError if no read data
	"""
	global flexsea

	bmsState = BMSState();
	retCode = flexsea.fxReadBMSDevice(devId, byref(bmsState))

	if (retCode == FxInvalidDevice):
		raise ValueError('fxReadDevice: invalid device ID')
	elif (retCode == FxNotStreaming):
		raise RuntimeError('fxReadDevice: no read data')

	return bmsState

def fxReadDeviceAll(devId, dataQueueSize):
	"""
	Read all data from a streaming FlexSEA device stream.
	MUST call fxStartStreaming before calling this.

	Parameters:
	devId: Device ID of the device to read from.

	dataQueueSize: Size of readData.

	Raise:
	ValueError if invalid device ID

	Return:
	Actual number of entries read. You will probably need to use this number.
	"""
	global flexsea

	actPackStateDataQueue = [ActPackState() for count in range(dataQueueSize)]

	itemsRead = flexsea.fxReadDeviceAll(devId, byref(actPackStateDataQueue), dataQueueSize)
	if (itemsRead == -1):
		raise ValueError('fxReadDeviceAll: Invalid device ID')
	return itemsRead

def fxReadNetMasterDeviceAll(devId, dataQueueSize):
	"""
	Read all data from a streaming FlexSEA NetMaster device stream.
	MUST call fxStartStreaming before calling this.

	Parameters:
	devId: Device ID of the device to read from.

	dataQueueSize: Size of readData.

	Raise:
	ValueError if invalid device ID

	Return:
	Actual number of entries read. You will probably need to use this number.
	"""
	global flexsea

	netMasterStateDataQueue = [NetMasterState() for count in range(dataQueueSize)];

	itemsRead = flexsea.fxReadNetMasterDeviceAll(devId, byref(netMasterStateDataQueue), dataQueueSize)
	if (itemsRead == -1):
		raise ValueError('fxReadNetMasterDeviceAll: Invalid device ID')
	return itemsRead

def fxReadBMSDeviceAll(devId, dataQueueSize):
	"""
	Read all data from a streaming FlexSEA BMS device stream.
	MUST call fxStartStreaming before calling this.

	Parameters:
	devId: Device ID of the device to read from.

	dataQueueSize: Size of readData.

	Raise:
	ValueError if invalid device ID

	Return:
	Actual number of entries read. You will probably need to use this number.
	"""
	global flexsea

	bmsStateDataQueue = [BMSState() for count in range(dataQueueSize)]

	itemsRead = flexsea.fxReadNetMasterDeviceAll(devId, byref(bmsStateDataQueue), dataQueueSize)
	if (itemsRead == -1):
		raise ValueError('fxReadBMSDeviceAll: Invalid device ID')
	return itemsRead


def fxSetReadDataQueueSize(devId, readDataQueueSize):
	"""
	Set the maximum read data queue size of a device.

	Parameters:
	devId (int): The device ID: ID of the device to get the read data queue size from.

	readDataQueueSize: Size to set the read data queue size to.

	Raises:
	fxInvalidDevice if invalid device.
	fxInvalidParam if size is invalid
	"""
	global flexsea

	retCode = flexsea.fxSetReadDataQueueSize(devId, readDataQueueSize)
	if (retCode == FxInvalidDevice):
		raise ValueError('fxSetReadDataQueueSize: Invalid device ID')
	elif (retCode == FxInvalidParam):
		raise ValueError('fxSetReadDataQueueSize: Invalid readDataQueueSize')

def fxGetReadDataQueueSize(devId):
	"""
	Get the maximum read data queue size of a device.

	Parameters:
	devId (int): The device ID: ID of the device to get the read data queue size from.

	Returns:
	Maximum read data queue size of a device.  -1 if invalid device ID.
	"""
	global flexsea

	retVal = flexsea.fxGetReadDataQueueSize(devId)
	if (retVal == -1):
		raise ValueError('fxGetReadDataQueueSize: Invalid device ID')
	return retVal


def fxSetGains(devId, kp, ki, kd, K, B):
	"""
	Sets the gains used by PID controllers on the FlexSEA device.

	Parameters:
	devId (int): The device ID.

	kp (int): Proportional gain

	ki (int): Integral gain

	kd (int): Differential gain

	K (int): Stiffness (used in impedence control only)

	B (int): Damping (used in impedance control only)

	Raises:
	ValueError if the device ID is invalid
	"""
	global flexsea
	retCode = flexsea.fxSetGains(devId, kp, ki, kd, K, B)

	if (retCode == FxInvalidDevice):
		raise ValueError('fxSetGains: invalid device ID')

def fxSendMotorCommand(devId, controlMode, value):
	"""
	Send a command to the device.

	Parameters:
	devId (int): The device ID.

	controlMode (c_int): The control mode we will use to send this command.
	Possible values are: FxPosition, FxCurrent, FxVoltage, FxImpedence

	value (int): The value to use for the controlMode.
	FxPosition - encoder value
	FxCurrent - current in mA
	FxVoltage - voltage in mV
	FxImpedence - current in mA

	Raises:
	ValueError if invalid device ID
	ValueError if invalid controlType
	"""
	global flexsea

	retCode = flexsea.fxSendMotorCommand(devId, controlMode, c_int(int(value)))

	if (retCode == FxInvalidDevice):
		raise ValueError('fxSendMotorCommand: invalid device ID')
	if (retCode == FxFailure):
		raise IOError('fxSendMotorCommand: command failed')
	if (retCode == FxInvalidParam):
		raise ValueError('fxSendMotorCommand: invalid controlType')

def fxGetAppType(devId):
	"""
	Get the device application type

	Parameters:
	devId (int): The device ID.

	Returns:
	App Type (int)

	-1 if invalid
	0 if ActPack
	1 if Exo
	2 if NetMaster
	"""
	global flexsea

	return flexsea.fxGetAppType(devId)

def fxFindPoles(devId):
	"""
	DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
	Find the motor poles

	Parameters:
	devId (int): The device ID.

	Returns:
	FxInvalidDevice if deviceId is invalid
	FxSuccess otherwise

	DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
	"""
	if (flexsea.fxFindPoles(devId) == FxInvalidDevice):
		raise ValueError('fxFindPoles: invalid device ID')

# Loads the library from the c lib
def loadFlexsea():
	global flexsea
	#Init code:
	print('[pyFlexsea Module]\n')

	loadSucceeded  = False
	# is_64bits = sys.maxsize > 2**32
	if (sys.maxsize > 2**32):
		print('You are using 64-bit Python. This program requires 32-bit Python')
		return False
	sysOS = platform.system().lower()
	dir_path = os.path.dirname(os.path.realpath(__file__))

	# we currently support Ubuntu and Raspbian so need to make sure we are pulling
	# in correct library depending on which version of linux
	# linux_distro = platform.linux_distribution()[0]

	print('>>> dir_path:', dir_path)
	# check whether we are running on a 32 or 64 bit machine
	architecture = platform.architecture()[0]
	librarypaths = []
	if("win" in sysOS):
		# load proper library based on host architecture
		if architecture == "32bit":
			lpath_base = os.path.join(dir_path,'../../libs/win32')
		else:
			lpath_base = os.path.join(dir_path,'../../libs/win64')
		librarypaths = [os.path.join(lpath_base,'libfx_plan_stack.dll')]
		# Python 3.8+ requires location of all DLLs AND their dependencies be explicitly
		# stated. Provide location of DLLs that libfx_plan_stack.dll depends on
		if sys.version_info.minor >= 8:
			os.add_dll_directory(os.path.join(dir_path,'../'))
	else:
		# Try to load the full linux lib first (that's x86_64), if that
		# fails, fall back to the raspberryPi lib.
		librarypaths = [
				os.path.join(dir_path,'../../libs/linux','libfx_plan_stack.so'),
				os.path.join(dir_path,'../../libs/raspberryPi','libfx_plan_stack.so'),
		]

	for librarypath in librarypaths:
		try:
			print("loading... " + librarypath)
			flexsea = cdll.LoadLibrary(librarypath)
		except OSError as arg:
			print("\n\nThere was a problem loading the library\n {0}\n".format(arg))
		else:
			loadSucceeded = True
			break

	if(loadSucceeded  != True):
		return False

	print("Loaded!")

	# set arg types
	flexsea.fxOpen.argtypes = [c_char_p, c_uint, c_uint]
	flexsea.fxOpen.restype = c_int

	flexsea.fxIsOpen.argtypes = [c_uint]
	flexsea.fxIsOpen.restype = c_bool

	flexsea.fxClose.argtypes = [c_uint]
	flexsea.fxClose.restype = c_int

	flexsea.fxCloseAll.argtypes = []
	flexsea.fxCloseAll.resType = []

	flexsea.fxGetDeviceIds.argtypes = [POINTER(c_int), c_uint]

	flexsea.fxStartStreaming.argtypes = [c_uint, c_uint, c_bool]
	flexsea.fxStartStreaming.restype = c_int

	flexsea.fxStopStreaming.argtypes = [c_uint]
	flexsea.fxStopStreaming.restype = c_int

	flexsea.fxReadDevice.argtypes = [c_uint, POINTER(ActPackState)]
	flexsea.fxReadDevice.restype = c_int

	flexsea.fxReadDeviceAll.argtypes = [c_uint, POINTER(ActPackState), c_uint]
	flexsea.fxReadDeviceAll.restype = c_int

	flexsea.fxReadNetMasterDevice.argtypes = [c_uint, POINTER(NetMasterState)]
	flexsea.fxReadDevice.restype = c_int

	flexsea.fxReadNetMasterDeviceAll.argtypes = [c_uint, POINTER(NetMasterState), c_uint]
	flexsea.fxReadNetMasterDeviceAll.restype = c_int

	flexsea.fxSetReadDataQueueSize.argtypes = [c_uint, c_uint]
	flexsea.fxSetReadDataQueueSize.restype  = c_uint

	flexsea.fxGetReadDataQueueSize.argtypes = [c_uint]
	flexsea.fxGetReadDataQueueSize.restype  = c_int

	flexsea.fxSetGains.argtypes = [c_uint, c_uint, c_uint, c_uint, c_uint, c_uint]
	flexsea.fxSetGains.restype = c_int

	flexsea.fxSendMotorCommand.argtypes = [c_uint, c_int, c_int]
	flexsea.fxSendMotorCommand.restype = c_int

	flexsea.fxGetAppType.argtypes = [c_uint]
	flexsea.fxSendMotorCommand.restype = c_int

	return True

def list_to_int_arr(l):
	c_arr = (c_int * len(l))(*l)
	c_len = c_uint(len(l))
	return c_arr, c_len

