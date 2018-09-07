import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.pyFlexsea import *
from flexseapython.pyFlexsea_def import *
from flexseapython.fxUtil import *

labels = ["State time", 											\
"accel x", "accel y", "accel z", "gyro x", "gyro y", "gyro z", 		\
"encoder angle", "ankle angle","motor voltage"
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,	FX_ANKLE_ANG,				\
	FX_MOT_VOLT								\
]

def fxReadOnly(devId):

	fxSetStreamVariables(devId, varsToStream)
	streamSuccess = fxStartStreaming(devId, 100, False, 0)
	if(not streamSuccess ):
		print("streaming failed...")
		sys.exit(-1)

	for i in range(0, 250):
		sleep(0.1)
		clearTerminal()
		data = fxReadDevice(devId, varsToStream)
		printData(labels, data)

	fxStopStreaming(devId)


if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxReadOnly(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
