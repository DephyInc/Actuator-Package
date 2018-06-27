import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *

def fxOpenControl(devId):

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

	fxSetStreamVariables(devId, varsToStream)
	streamSuccess = fxStartStreaming(devId, 100, False, 1)
	if(not streamSuccess ):
		print("streaming failed...")
		sys.exit(-1)

	print("Setting open control...") 
	setControlMode(devId, CTRL_OPEN)
	numSteps = 100
	numSeconds = 1
	maxVoltage = 3000
	numTimes = 2
	for time in range(0, numTimes):

		for i in range(0, numSteps):
			sleep(numSeconds / numSteps)
			mV = maxVoltage * (i / numSteps)
			setMotorVoltage(devId, mV)
			data = fxReadDevice(devId, varsToStream)
			os.system('cls')
			print('Open control demo...')
			print("Ramping up open controller...") 
			printData(labels, data)
		
		for i in range(0, numSteps):
			sleep(numSeconds / numSteps)
			mV = maxVoltage * ((numSteps - i) / numSteps)
			setMotorVoltage(devId, mV)
			data = fxReadDevice(devId, varsToStream)
			os.system('cls')
			print('Open control demo...')
			print("Ramping down open controller...")
			printData(labels, data)

	fxStopStreaming(devId)

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxOpenControl(devId)	
	except Exception as e:
		print("Broke... ")
		print(str(e))