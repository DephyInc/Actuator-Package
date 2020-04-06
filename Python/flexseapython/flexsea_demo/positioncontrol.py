import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def fxPositionControl(port, baudRate, time = 8, time_step = 0.1,  resolution = 100):

	devId = fxOpen(port, baudRate, logLevel = 6)
	fxStartStreaming(devId, resolution, shouldLog = False)
	sleep(0.1)

	actPackState = fxReadDevice(devId)
	printDevice(actPackState)
	initialAngle = actPackState.encoderAngle

	fxSetGains(devId, 50, 3, 0, 0, 0)

	fxSendMotorCommand(devId, FxPosition, initialAngle)

	num_time_steps = int(time/time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		clearTerminal()
		actPackState = fxReadDevice(devId)
		currentAngle = actPackState.encoderAngle
		print('Desired:              ', initialAngle)
		print('Measured:             ', currentAngle)
		print('Difference:           ', currentAngle - initialAngle, '\n', flush=True)
		printDevice(actPackState)
		
	fxClose(devId)

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxPositionControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
