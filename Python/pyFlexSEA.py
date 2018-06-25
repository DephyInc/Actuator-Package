from ctypes import *
import os
import sys
import platform

global flexsea
initialized = False

def list_to_arr(l):
	c_arr = (c_int * len(l))(*l)
	c_len = c_int(len(l))
	return c_arr, c_len

def fxOpen(port, idx):
	global flexsea
	flexsea.fxOpen( port , idx)

def fxIsOpen(idx):
	global flexsea
	return flexsea.fxIsOpen(idx)

def fxGetDeviceIds():
	global flexsea
	c_l, c_n = list_to_arr([-1, -1, -1, -1, -1, -1])
	flexsea.fxGetDeviceIds(c_l, c_n)
	return c_l

def fxStartStreaming(devId, freq, shouldLog, shouldAuto):
	global flexsea
	return	flexsea.fxStartStreaming(devId, freq, shouldLog, shouldAuto)

def fxStopStreaming(devId):
	global flexsea
	return	flexsea.fxStopStreaming(devId)

def fxSetStreamVariables(devId, fieldIds):
	global flexsea
	c_fi, c_n = list_to_arr(fieldIds)
	flexsea.fxSetStreamVariables(devId, c_fi, c_n)

def fxReadDevice(devId, fieldIds):
	global flexsea
	n = len(fieldIds)
	c_fi, c_n = list_to_arr(fieldIds)
	result = flexsea.fxReadDevice(devId, c_fi, c_n)
	asList = result[:n]
	return asList

def setControlMode(devId, ctrlMode):
	global flexsea
	flexsea.setControlMode(devId, int(ctrlMode))

def setMotorVoltage(devId, mV):
	global flexsea
	flexsea.setMotorVoltage(devId, int(mV))

def setMotorCurrent(devId, cur):
	global flexsea
	flexsea.setMotorCurrent(devId, int(cur))

def setPosition(devId, pos):
	global flexsea
	flexsea.setPosition(devId, int(pos))

def setZGains(devId, z_k, z_b, i_kp, i_ki):
	global flexsea
	flexsea.setZGains(devId, int(z_k), int(z_b), int(i_kp), int(i_ki))

def loadFlexsea():
	global flexsea
	#Init code:
	print('[pySerial Module]\n')

	loadSucceeded  = False
	is_64bits = sys.maxsize > 2**32
	sysOS = platform.system().lower()
	dir_path = os.path.dirname(os.path.realpath(__file__))

	lpath_base = dir_path + '/../fx_plan_stack/build'
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
		loadSucceeded = True
		
	except:
		pass

	if(not loadSucceeded):
		print("Failed to load shared library. Check library path\n")
		return False

	print("Loaded!")
	initialized = True
	flexsea.fxSetup()
	# set arg types
	flexsea.fxOpen.argtypes = [c_char_p, c_int]

	flexsea.fxStartStreaming.argtypes = [c_int, c_int, c_bool, c_int]
	flexsea.fxStopStreaming.argtypes = [c_int]
	flexsea.fxReadDevice.restype = POINTER(c_int)

	flexsea.setControlMode.argtypes = [c_int, c_int]
	flexsea.setMotorVoltage.argtypes = [c_int, c_int]
	flexsea.setMotorCurrent.argtypes = [c_int, c_int]

	return True