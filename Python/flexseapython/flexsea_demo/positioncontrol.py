import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def printDevice(actPackState):
	print('State time: ', actPackState.timestamp)
	print('Accel X: ', actPackState.accelx, ', Accel Y: ', actPackState.accely, ' Accel Z: ', actPackState.accelz)
	print('Gyro X: ', actPackState.gyrox, ', Gyro Y: ', actPackState.gyroy, ' Gyro Z: ', actPackState.gyroz)
	print('Motor angle: ', actPackState.encoderAngle, ', Motor voltage: ', actPackState.motorVoltage)

def fxPositionControl(port, baudRate, time = 5, time_step = 0.1,  resolution = 100):
	
	devId = fxOpen(port, baudRate, 0)
	fxStartStreaming(devId, resolution, True)
	sleep(0.1)

	actPackState = fxReadDevice(devId)
	printDevice(actPackState)
	initialAngle = actPackState.encoderAngle

	fxSetGains(devId, 50, 3, 0, 0, 0)

	fxSendMotorCommand(devId, FxPosition, initialAngle)

	num_time_steps = int(time/time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		preamble = "Holding position: {}...".format(initialAngle)
		print(preamble)

		actPackState = fxReadDevice(devId)
		printDevice(actPackState)
		currentAngle = actPackState.encoderAngle
		
		print("Measured delta is: ", currentAngle - initialAngle, flush=True)

	fxClose(devId)

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxPositionControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
