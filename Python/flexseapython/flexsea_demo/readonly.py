import os, sys
from time import sleep
from flexseapython.fxUtil import *

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)

def printBMSState(devId):
	bmsState = fxReadBMSDevice(devId)
	for i in range(9):
		print('cellVoltage[', i, ']: ', bmsState.cellVoltage[i])
	for i in range(3):
		print('temperature[', i, ']: ', bmsState.temperature[i])

def fxReadOnly(port, baudRate, time = 8, time_step = 0.1):
	debugLoggingLevel = 0	# 6 is least verbose, 0 is most verbose
	dataLog = True 			# False means no logs will be saved
	devId =	fxOpen(port, baudRate, debugLoggingLevel)
	fxStartStreaming(devId, frequency = 100, shouldLog = dataLog)
	appType = fxGetAppType(devId)

	if (appType == FxActPack):
		print('\nYour device is an ActPack.\n')
		input("Press Enter to continue...")
	elif (appType == FxNetMaster):
		print('\nYour device is a NetMaster.\n')
		input("Press Enter to continue...")
	elif (appType == FxBMS):
		print('\nYour device is a BMS.\n')
		input("Press Enter to continue...")
	elif (appType == FxExo):
		print('\nYour device is an Exo or ActPack Plus.\n')
		input("Press Enter to continue...")
	else:
		raise RuntimeError('Unsupported application type: ', appType)

	totalLoopCount = int(time / time_step)
	for i in range(totalLoopCount):
		printLoopCount(i, totalLoopCount)
		sleep(time_step)
		clearTerminal()
		myData = fxReadDevice(devId)
		printDeviceAll(myData, appType)
	fxClose(devId)
	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxReadOnly(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
