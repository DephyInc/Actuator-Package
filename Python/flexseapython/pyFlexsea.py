from ctypes import *
import os
import sys
import platform

global flexsea
initialized = False

# Opens the given serial port at the given index and looks for devices
def fxOpen(port, idx):
	global flexsea
	flexsea.fxOpen( port.encode('utf-8') , idx)

# Returns a boolean that indicates whether the port is open
def fxIsOpen(idx):
	global flexsea
	return flexsea.fxIsOpen(idx)

# Returns a list of device ids corresponding to connected devices
def fxGetDeviceIds():
	global flexsea
	n = 6
	l = [-1] * 6
	c_l, c_n = list_to_int_arr(l)
	flexsea.fxGetDeviceIds(c_l, c_n)
	asList = c_l[:n]
	asList = asList[: asList.index(-1) ]
	return asList

# Starts streaming data read commands and act pack commands for the given device
# params:
# 		devId 		: the id of the device to stream
# 		freq 		: the frequency to stream at
# 		shouldLog 	: whether to log data received from this device to a log file
# 		shouldAuto 	: whether to use autostreaming or manual streaming
# returns:
# 		c_bool value indicating whether the request was a success
def fxStartStreaming(devId, freq, shouldLog, shouldAuto):
	global flexsea
	return	flexsea.fxStartStreaming(devId, freq, shouldLog, shouldAuto)

# Stops streaming data read commands and act pack commands for the given device
# params:
# 		devId 		: the id of the device to stop streaming
# returns:
# 		c_bool value indicating whether the request was a success
def fxStopStreaming(devId):
	global flexsea
	return	flexsea.fxStopStreaming(devId)

# Sets the active stream variables for the given device
# Note: changing the stream variables during a logged stream has undefined behaviour
# params:
# 		devId 		: the id of the device to set fields for
# 		fieldIds 	: a list containing the fields to stream 
def fxSetStreamVariables(devId, fieldIds):
	global flexsea
	c_fi, c_n = list_to_int_arr(fieldIds)
	flexsea.fxSetStreamVariables(devId, c_fi, c_n)

# Reads the most recent data received from the device
# params:
# 		devId 		: the id of the device to read
# 		fieldIds 	: a list containing the fields to read 
# returns:
# 		a python list containing the values of the requested fields 
#		(in the order requested), or None for fields that errored
def fxReadDevice(devId, fieldIds):
	global flexsea
	n = len(fieldIds)	

	c_fieldIds, c_n = list_to_int_arr(fieldIds)
	c_successBools, c_n = list_to_bool_arr( [0] * n )

	result = flexsea.fxReadDevice(devId, c_fieldIds, c_successBools, c_n)

	valsAsList = result[:n]
	boolsAsList = c_successBools[:n]

	for i in range(0, n):
		if(boolsAsList[i] == 0):
			valsAsList[i] = None

	return valsAsList

# Sets the control mode for the given device
# params:
# 		devId 		: the id of the device 
# 		ctrlMode 	: the control mode to use [must be one of values provided in pyFlexsea_def.py]
def setControlMode(devId, ctrlMode):
	global flexsea
	flexsea.setControlMode(devId, int(ctrlMode))

# Sets the voltage setpoint for the given device
# params:
# 		devId 		: the id of the device 
# 		mV 			: the voltage to set in milliVolts
def setMotorVoltage(devId, mV):
	global flexsea
	flexsea.setMotorVoltage(devId, int(mV))

# Sets the current setpoint for the given device
# params:
# 		devId 		: the id of the device 
# 		cur			: the current to use as setpoint in milliAmps
def setMotorCurrent(devId, cur):
	global flexsea
	flexsea.setMotorCurrent(devId, int(cur))

# Sets the position setpoint for the given device
# params:
# 		devId 		: the id of the device 
# 		pos			: the absolute encoder position to use as setpoint
def setPosition(devId, pos):
	global flexsea
	flexsea.setPosition(devId, int(pos))

# Sets the PID controller gains for the given device
# params:
# 		devId 		: the id of the device 
# 		z_k			: the proportional gain to set for the active setpoint
# 		z_b			: the integral gain to set for the active setpoint
# 		i_kp		: the proportional gain to set for the underlying current controller (only relevant for impedance control)
# 		i_ki		: the integral gain to set for the underlying current controller (only relevant for impedance control)
def setZGains(devId, z_k, z_b, i_kp, i_ki):
	global flexsea
	flexsea.setZGains(devId, int(z_k), int(z_b), int(i_kp), int(i_ki))

# Sets the activation state for FSM2 on the given device
# params:
# 		devId 		: the id of the device 
# 		on			: whether to set the FSM on or off
def actPackFSM2(devId, on):
	global flexsea
	flexsea.actPackFSM2(devId, int(on))

# Tells the given device to run a find poles routine
# params:
# 		devId 		: the id of the device 
# 		block 		: whether to block for 60 seconds while the device runs the routine
def findPoles(devId, block):
	global flexsea
	flexsea.findPoles(devId, int(block))

# Loads the library from the c lib
def loadFlexsea():
	global flexsea
	#Init code:
	print('[pySerial Module]\n')

	loadSucceeded  = False
	is_64bits = sys.maxsize > 2**32
	sysOS = platform.system().lower()
	dir_path = os.path.dirname(os.path.realpath(__file__))

	lpath_base = dir_path + '/../../fx_plan_stack/build'
	librarypath=""

	if("win" in sysOS):
		if(is_64bits):
			librarypath = lpath_base + '/win64/libfx_plan_stack.dll'
		else:
			librarypath = lpath_base + '/win/libfx_plan_stack.dll'
	else:
		if(is_64bits):
			librarypath = lpath_base + '/unix64/libfx_plan_stack.so'
		else:
			librarypath = lpath_base + '/unix/libfx_plan_stack.so'	

	try:
		print("loading... " + librarypath)
		flexsea = cdll.LoadLibrary(librarypath)
		
	except OSError, arg:
                print "\n\nThere was a problem loading the library\n", arg
        else:
                loadSucceded = True;

	if(not loadSucceeded):
		return False

	print("Loaded!")
	initialized = True
	flexsea.fxSetup()
	# set arg types
	flexsea.fxOpen.argtypes = [c_char_p, c_int]
	flexsea.fxSetStreamVariables.restype = c_bool

	flexsea.fxStartStreaming.argtypes = [c_int, c_int, c_bool, c_int]
	flexsea.fxStopStreaming.argtypes = [c_int]
	flexsea.fxReadDevice.restype = POINTER(c_int)

	flexsea.setControlMode.argtypes = [c_int, c_int]
	flexsea.setMotorVoltage.argtypes = [c_int, c_int]
	flexsea.setMotorCurrent.argtypes = [c_int, c_int]

	return True

def list_to_int_arr(l):
	c_arr = (c_int * len(l))(*l)
	c_len = c_int(len(l))
	return c_arr, c_len

def list_to_bool_arr(l):
	c_arr = (c_bool * len(l))(*l)
	c_len = c_int(len(l))
	return c_arr, c_len
