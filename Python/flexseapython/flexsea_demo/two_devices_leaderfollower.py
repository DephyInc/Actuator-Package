import os, sys
from time import sleep

import traceback

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def printDevice(actPackState):
	print('State time: ', actPackState.timestamp)
	print('Accel X: ', actPackState.accelx, ', Accel Y: ', actPackState.accely, ' Accel Z: ', actPackState.accelz)
	print('Gyro X: ', actPackState.gyrox, ', Gyro Y: ', actPackState.gyroy, ' Gyro Z: ', actPackState.gyroz)
	print('Motor angle: ', actPackState.encoderAngle, ', Motor voltage: ', actPackState.motorVoltage, flush=True)


def fxLeaderFollower(leaderPort, followerPort, baudRate):

	devId0 = fxOpen(leaderPort, baudRate, 0)
	devId1 = fxOpen(followerPort, baudRate, 0)

	fxStartStreaming(devId0, 200, True)
	fxStartStreaming(devId1, 200, True)

	sleep(0.2)

	actPackState0 = fxReadDevice(devId0)	
	actPackState1 = fxReadDevice(devId1)

	initialAngle0 = actPackState0.encoderAngle
	initialAngle1 = actPackState1.encoderAngle


	# set first device to current controller with 0 current (0 torque)
	fxSetGains(devId0, 100, 20, 0, 0, 0)
	fxSendMotorCommand(devId0, FxCurrent, 0)

	# set position controller for second device
	fxSetGains(devId1, 50, 3, 0, 0, 0)
	fxSendMotorCommand(devId1, FxPosition, initialAngle1)

	count = 0
	try:
		while(True):
			sleep(0.05)

			leaderData = fxReadDevice(devId0)
			followerData = fxReadDevice(devId1)

			angle0 = leaderData.encoderAngle
			
			diff = angle0 - initialAngle0
			fxSendMotorCommand(devId1, FxPosition, initialAngle1 + diff)
			
			print("device {} following device {}".format(devId1, devId0))
			
			printDevice(followerData)
			printDevice(leaderData)

	except Exception as e:
		print(traceback.format_exc())

	print('Turning off position control...')
	fxClose(devId0)
	fxClose(devId1)

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:4]
	try:
		fxLeaderFollower(ports[0], ports[1], baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
