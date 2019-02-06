import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from streamManager import StreamManager

labels = ["State time", 		\
"Motor angle", "Motor current",	\
"Battery voltage", "Battery current" \
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ENC_ANG,								\
	FX_MOT_CURR,								\
	FX_BATT_VOLT, FX_BATT_CURR \
]

def fxCurrentControl(devId):
   	stream = StreamManager(devId,printingRate = 2,labels=labels, varsToStream = varsToStream)
	holdCurrent = 1000
	fxSetStreamVariables(devId, varsToStream)
	print('Setting controller to current...')
	setControlMode(devId, CTRL_CURRENT)
	setZGains(devId, 100, 20, 0, 0)
	setMotorCurrent(devId, holdCurrent) # Start the current, holdCurrent is in mA 

	try:
		while(True):
			sleep(0.1)
			preamble = "Holding Current: {} mA...".format(holdCurrent)
			stream()
			stream.printData()

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
	lastAngle = stream([FX_ENC_ANG])[0]
	sleep(0.2)
	currentAngle = stream([FX_ENC_ANG])[0]
	while( abs(currentAngle - lastAngle) > 100):
		lastAngle = currentAngle
		sleep(0.2)
		currentAngle = stream([FX_ENC_ANG])[0]

	setControlMode(devId, CTRL_NONE)
	del stream

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxCurrentControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
