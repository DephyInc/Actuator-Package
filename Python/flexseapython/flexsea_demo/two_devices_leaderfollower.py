import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

labels = ["State time", 				\
	"Accel X",	"Accel Y",	"Accel Z",	\
	"Gyro X", 	"Gyro Y", 	"Gyro Z",	\
	"Motor angle", "Motor voltage", "Motor current",	\
	"Battery voltage", "Battery current"				\
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,								\
	FX_MOT_VOLT, FX_MOT_CURR,				\
	FX_BATT_VOLT, FX_BATT_CURR 				\
]

def fxLeaderFollower(devId0, devId1):

	stream = StreamManager(port, printingRate =2, labels=labels, varsToStream=varsToStream)
	result = True
	stream()

	initialAngles = fxReadDevice(devId0, [FX_ENC_ANG]) + fxReadDevice(devId1, [FX_ENC_ANG])
	timeout = 10
	timeoutCount = 0

	while(None in initialAngles):
		timeoutCount = timeoutCount + 1
		if(timeoutCount > timeout):
			print("Timed out waiting for valid encoder value...")
			sys.exit(1)
		else:
			sleep(0.5)
			a = fxReadDevice(devId0, [FX_ENC_ANG])
			b = fxReadDevice(devId1, [FX_ENC_ANG])
			print(a)
			print(b)
			initialAngles = a + b
			print(initialAngles)


	print("Turning on position control for device {} to follow device {} ".format(devId1, devId0))


	# set first device to current controller with 0 current (0 torque)
	setControlMode(devId0, CTRL_CURRENT)
	setGains(devId0, 100, 20, 0, 0)
	setMotorCurrent(devId0, 0) # Start the current, holdCurrent is in mA 

	# set position controller for second device
	setPosition(devId1, initialAngles[1])
	setControlMode(devId1, CTRL_POSITION)
	setPosition(devId1, initialAngles[1])
	setGains(devId1, 50, 3, 0, 0)

	count = 0
	try:
		while(True):
			sleep(0.05)
			angle0 = fxReadDevice(devId0, [FX_ENC_ANG])[0]
			if(angle0 != None):
				diff0 = angle0 - initialAngles[0]
				setPosition(devId1, initialAngles[1] + 3*diff0)

			count = (count + 1) % 10
			if(count == 0):
				clearTerminal()
				print("device {} following device {}".format(devId1, devId0))
				for devId in [devId0, devId1]:
					data = fxReadDevice(devId, varsToStream)
					print("Device [{}]:".format(devId))
					printData(labels, data)

	except:
		pass

	print('Turning off position control...')
	setControlMode(devId0, CTRL_NONE)
	setControlMode(devId1, CTRL_NONE)

	# sleep so that the commmand makes it through before we stop streaming
	sleep(0.2)
	fxStopStreaming(devId0)
	fxStopStreaming(devId1)

if __name__ == '__main__':
	ports = sys.argv[1:3]
	devIds = loadAndGetDevice(ports)
	try:
		fxLeaderFollower(devIds[0], devIds[1])	
	except Exception as e:
		print("broke: " + str(e))
		pass
