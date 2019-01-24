import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

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

def fxTwoDevicePositionControl(devId0, devId1):

	fxSetStreamVariables(devId0, varsToStream)
	fxSetStreamVariables(devId1, varsToStream)
	streamSuccess0 = fxStartStreaming(devId0, 100, False, 0)
	streamSuccess1 = fxStartStreaming(devId1, 100, False, 0)

	if(not (streamSuccess0 and streamSuccess1)):
		print("streaming failed...")
		sys.exit(-1)

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

	# set position controller for both devices
	for i, devId in enumerate( [devId0, devId1] ):
		setPosition(devId, initialAngles[i])
		setControlMode(devId, CTRL_POSITION)
		setPosition(devId, initialAngles[i])
		setZGains(devId, 50, 3, 0, 0)

	try:
		while(True):
			sleep(0.2)
			os.system('cls')
			print("Holding position, two devices: ")
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
		fxTwoDevicePositionControl(devIds[0], devIds[1])	
	except Exception as e:
		print("broke: " + str(e))
		pass
