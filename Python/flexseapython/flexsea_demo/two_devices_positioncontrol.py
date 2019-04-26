import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *
from .streamManager import Stream

labels = ["State time", 											\
"Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", 		\
"Motor angle", "Motor voltage", "Motor current",					\
"Battery voltage", "Battery current"								\
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,								\
	FX_MOT_VOLT, FX_MOT_CURR,				\
	FX_BATT_VOLT, FX_BATT_CURR 				\
]

def fxTwoDevicePositionControl(port0, port1):

	dev0 = Stream(port0, printingRate =2, labels=labels, varsToStream=varsToStream)
	dev1 = Stream(port1, printingRate =2, labels=labels, varsToStream=varsToStream)

	# Concatenates angles of both stream together
	initialAngles = dev0([FX_ENC_ANG]) + dev1([FX_ENC_ANG])
	timeout = 10
	timeoutCount = 0

	while(None in initialAngles):
		timeoutCount = timeoutCount + 1
		if(timeoutCount > timeout):
			raise Exception("Timed out trying to read data")
		else:
			sleep(0.5)
			# Concatenates angles of both stream together
			a = dev0([FX_ENC_ANG])
			b = dev1([FX_ENC_ANG])
			initialAngles = a + b

	# set position controller for both devices
	for i, devId in enumerate( [dev0.devId, dev1.devId] ):
		setPosition(devId, initialAngles[i])
		setControlMode(devId, CTRL_POSITION)
		setPosition(devId, initialAngles[i])
		setGains(devId, 50, 3, 0, 0)

	try:
		while(True):
			sleep(0.2)
			os.system('cls')
			preamble = "Holding position, two devices: "
			dev0()
			dev1()
			dev0.printData(message = preamble)
			dev1.printData(clear_terminal = False)
	except:
		pass

	print('Turning off position control...')
	setControlMode(dev0.devId, CTRL_NONE)
	setControlMode(dev1.devId, CTRL_NONE)

	# sleep so that the commmand makes it through before we stop streaming
	sleep(0.2)
	del followerStream
	sleep(0.2)
	del leadStream

if __name__ == '__main__':
	ports = sys.argv[1:3]
	try:
		fxTwoDevicePositionControl(ports[0], ports[1])	
	except Exception as e:
		print("broke: " + str(e))
