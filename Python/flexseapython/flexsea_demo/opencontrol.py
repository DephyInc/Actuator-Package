import os, sys
from time import sleep
from flexseapython.fxUtil import *

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

def fxOpenControl(port, baudRate, time = 2, num_times = 5,
		time_resolution = 0.1, maxVoltage = 3000, sign = -1):
	devId = fxOpen(port, baudRate, logLevel = 6)
	fxStartStreaming(devId, 100, shouldLog = False)
	appType = fxGetAppType(devId)
	print("Setting open control...")
	fxSendMotorCommand(devId, FxVoltage, 0)
	sleep(0.5)
	numSteps = int((time/2)/time_resolution)
	direction = 1

	for time in range(num_times):
		direction = direction * sign

		#Ramp-up:
		for i in range(numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * (i*1.0 / numSteps)
			fxSendMotorCommand(devId, FxVoltage, mV)
			clearTerminal()
			print('Ramping up motor voltage...\n')
			if(appType == FxActPack):
				data0 = fxReadDevice(devId)
				printDevice(data0)
			elif(appType == FxExo):
				data0 = fxReadExoDevice(devId)
				printExo(data0)

		#Ramp-down:
		for i in range(numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * ((numSteps - i)*1.0 / numSteps)
			fxSendMotorCommand(devId, FxVoltage, mV)
			clearTerminal()
			print('Ramping down motor voltage...\n')
			if(appType == FxActPack):
				data0 = fxReadDevice(devId)
				printDevice(data0)
			elif(appType == FxExo):
				data0 = fxReadExoDevice(devId)
				printExo(data0)

	fxClose(devId)
	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxOpenControl(baudRate)
	except Exception as e:
		print("Broke... ")
		print(str(e))
