import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

labels = ["State time", 											\
"encoder angle", "motor current"									\
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ENC_ANG,								\
	FX_MOT_CURR								\
]

def fxCurrentControl(devId):

	holdCurrent = 1000
	fxSetStreamVariables(devId, varsToStream)
	streamSuccess = fxStartStreaming(devId, 100, False, 0)

	print('Setting controller to current...')
	setControlMode(devId, CTRL_CURRENT)
	setZGains(devId, 20, 1, 0, 0)
	setMotorCurrent(devId, holdCurrent) # Start the current, holdCurrent is in mA 

	try:
		while(True):
			pass
	except:
		pass

	print('Turning off current control...')
	# ramp down first
	n = 4
	for i in range(0, n):
		setMotorCurrent(devId, holdCurrent * (n-i)/n)
		sleep(0.2)

	setControlMode(devId, CTRL_NONE)
	# sleep so that the commmand makes it through before we stop streaming
	sleep(0.2)
	fxStopStreaming(devId)

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxCurrentControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass