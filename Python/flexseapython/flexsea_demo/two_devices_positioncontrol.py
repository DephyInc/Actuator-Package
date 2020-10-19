import os, sys
from time import sleep
from flexseapython.fxUtil import *

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

def fxTwoDevicePositionControl(port0, baudRate, port1):

	expTime = 8
	time_step = 0.1

	devId0 = fxOpen(port0, baudRate, 0)
	devId1 = fxOpen(port1, baudRate, 0)

	fxStartStreaming(devId0, 200, shouldLog = False)
	sleep(0.1)
	fxStartStreaming(devId1, 200, shouldLog = False)
	sleep(0.1)

	actPackState0 = fxReadDevice(devId0)
	actPackState1 = fxReadDevice(devId1)

	initialAngle0 = actPackState0.mot_ang
	initialAngle1 = actPackState1.mot_ang

	fxSetGains(devId0, 50, 3, 0, 0, 0)
	fxSetGains(devId1, 50, 3, 0, 0, 0)
	
	fxSendMotorCommand(devId0, FxPosition, initialAngle0)
	fxSendMotorCommand(devId1, FxPosition, initialAngle1)

	num_time_steps = int(expTime/time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		clearTerminal()

		actPackState0 = fxReadDevice(devId0)
		actPackState1 = fxReadDevice(devId1)
		currentAngle0 = actPackState0.mot_ang
		currentAngle1 = actPackState1.mot_ang

		print('Device 0:\n---------\n')
		print('Desired:              ', initialAngle0)
		print('Measured:             ', currentAngle0)
		print('Difference:           ', currentAngle0 - initialAngle0, '\n')
		printDevice(actPackState0,FxActPack)

		print('\nDevice 1:\n---------\n')
		print('Desired:              ', initialAngle1)
		print('Measured:             ', currentAngle1)
		print('Difference:           ', currentAngle1 - initialAngle1, '\n', flush=True)
		printDevice(actPackState1,FxActPack)

		printLoopCount(i, num_time_steps)

	print('Turning off position control...')
	fxSetGains(devId0, 0, 0, 0, 0, 0)
	fxSetGains(devId1, 0, 0, 0, 0, 0)
	fxSendMotorCommand(devId1, FxNone, 0)
	fxSendMotorCommand(devId0, FxNone, 0)
	sleep(0.5)
	fxClose(devId0)
	fxClose(devId1)

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:4]
	try:
		fxTwoDevicePositionControl(ports[0], ports[1], baudRate)
	except Exception as e:
		print("broke: " + str(e))
