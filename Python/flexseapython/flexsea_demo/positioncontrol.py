import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

labels = ["State time", 											\
"accel x", "accel y", "accel z", "gyro x", "gyro y", "gyro z", 		\
"encoder angle", "motor voltage"									\
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,								\
	FX_MOT_VOLT								\
]

def fxPositionControl(devId):

	fxSetStreamVariables(devId, varsToStream)
	streamSuccess = fxStartStreaming(devId, 100, False, 0)
	if(not streamSuccess ):
		print("streaming failed...")
		sys.exit(-1)

	sleep(0.4)
	data = fxReadDevice(devId, varsToStream)

	printData(labels, data)
	
	initialAngle = fxReadDevice(devId, [FX_ENC_ANG])[0]	
	timeout = 100
	timeoutCount = 0
	while(initialAngle == None):
		timeoutCount = timeoutCount + 1
		if(timeoutCount > timeout):
			print("Timed out waiting for valid encoder value...")
			sys.exit(1)
		else:
			sleep(0.1)
			fxReadDevice(devId, [FX_ENC_ANG])[0]

	setPosition(devId, initialAngle)
	setControlMode(devId, CTRL_POSITION)
	setPosition(devId, initialAngle)
	setZGains(devId, 50, 3, 0, 0)

	for i in range(0, 100):
		sleep(0.1)
		data = fxReadDevice(devId, varsToStream)
		clearTerminal()
                print("Holding position: {}...".format(initialAngle))
		printData(labels, data)


	setControlMode(devId, CTRL_NONE)
	sleep(0.1)
	fxStopStreaming(devId)


if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxPositionControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
