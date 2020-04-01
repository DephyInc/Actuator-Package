import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def fxOpenControl(port, baudRate, time = 2, num_times = 5,
		time_resolution = 0.1, maxVoltage = 3000, sign = -1):
	devId = fxOpen(port, baudRate, logLevel = 6)
	fxStartStreaming(devId, 100, shouldLog = False)
	print("Setting open control...")
	fxSendMotorCommand(devId, FxVoltage, 0)
	sleep(0.5)
	numSteps = int((time/2)/time_resolution)
	direction = 1

	for time in range(num_times):
		direction = direction * sign

		for i in range(numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * (i*1.0 / numSteps)
			fxSendMotorCommand(devId, FxVoltage, mV)
			clearTerminal()
			print(u"\u2191", 'Ramping up open controller...')
			data0 = fxReadDevice(devId)
			printDevice(data0)

		for i in range(numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * ((numSteps - i)*1.0 / numSteps)
			fxSendMotorCommand(devId, FxVoltage, mV)
			clearTerminal()
			print(u"\u2193", 'Ramping down open controller...')
			data0 = fxReadDevice(devId)
			printDevice(data0)

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxOpenControl(baudRate)
	except Exception as e:
		print("Broke... ")
		print(str(e))
