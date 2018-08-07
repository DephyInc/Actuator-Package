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

	holdCurrent = 500
	fxSetStreamVariables(devId, varsToStream)
	streamSuccess = fxStartStreaming(devId, 100, False, 0)

	print('Setting controller to current...')
	setControlMode(devId, CTRL_CURRENT)
	setZGains(devId, 100, 20, 0, 0)
	setMotorCurrent(devId, holdCurrent) # Start the current, holdCurrent is in mA 

	try:
		while(True):
			sleep(0.1)
			data = fxReadDevice(devId, varsToStream)
			clearTerminal()
                        print("Holding Current: {} mA...".format(holdCurrent))
			printData(labels, data)

	except:
		pass

	print('Turning off current control...')
	# ramp down first
	n = 50
	for i in range(0, n):
		setMotorCurrent(devId, holdCurrent * (n-i)/n)
		sleep(0.04)

	# wait for motor to spin down

	setMotorCurrent(devId, 0)
	lastAngle = fxReadDevice(devId, [FX_ENC_ANG])[0]
	sleep(0.2)
	currentAngle = fxReadDevice(devId, [FX_ENC_ANG])[0]
	while( abs(currentAngle - lastAngle) > 100):
		lastAngle = currentAngle
		sleep(0.2)
		currentAngle = fxReadDevice(devId, [FX_ENC_ANG])[0]

	setControlMode(devId, CTRL_NONE)
	fxStopStreaming(devId)

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxCurrentControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
