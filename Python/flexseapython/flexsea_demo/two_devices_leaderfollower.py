import os, sys
from time import sleep
from flexseapython.fxUtil import *
import traceback

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

def fxLeaderFollower(leaderPort, baudRate, followerPort):

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
	loopCount=200
	try:
		#while(True):
		for i in range(loopCount):
			sleep(0.05)
			clearTerminal()
			leaderData   = fxReadDevice(devId0)
			followerData = fxReadDevice(devId1)
			angle0 = leaderData.encoderAngle
			diff = angle0 - initialAngle0
			fxSendMotorCommand(devId1, FxPosition, initialAngle1 + diff)
			# print("device {} following device {}".format(devId1, devId0))
			print('\nloop ',i,' of ',loopCount,'\n')
			print('Device', devId1, ' following device',  devId0)
			printDevice(followerData)
			printDevice(leaderData)
	except Exception as e:
		print(traceback.format_exc())

	fxSetGains(devId0, 0, 0, 0, 0, 0)
	fxSetGains(devId1, 0, 0, 0, 0, 0)

	fxSendMotorCommand(devId1, FxNone, initialAngle1)
	fxSendMotorCommand(devId0, FxNone, initialAngle1)

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
