import os, sys
from time import sleep
from flexseapython.fxUtil import *

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

def fxPositionControl(port, baudRate, time = 8, time_step = 0.1,  resolution = 100):

	devId = fxOpen(port, baudRate, logLevel = 6)
	fxStartStreaming(devId, resolution, shouldLog = False)
	sleep(0.1)

	actPackState = fxReadDevice(devId)
	printDevice(actPackState,FxActPack)
	initialAngle = actPackState.mot_ang

	fxSetGains(devId, 50, 3, 0, 0, 0, 0)

	fxSendMotorCommand(devId, FxPosition, initialAngle)

	num_time_steps = int(time / time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		clearTerminal()
		actPackState = fxReadDevice(devId)
		currentAngle = actPackState.mot_ang
		print('Desired:              ', initialAngle)
		print('Measured:             ', currentAngle)
		print('Difference:           ', currentAngle - initialAngle, '\n', flush=True)
		printDevice(actPackState,FxActPack)
		printLoopCount(i, num_time_steps)

	# When we exit we want the motor to be off
	fxSendMotorCommand(devId, FxNone, 0)
	sleep(0.5)
	fxClose(devId)

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxPositionControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
