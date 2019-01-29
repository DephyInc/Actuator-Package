import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from streamManager import StreamManager

labels = ["State time", 											\
"Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z", 		\
"Motor angle", "Motor voltage"									\
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,								\
	FX_MOT_VOLT								\
]

def fxOpenControl(devId):
	stream = StreamManager(devId,printingRate =10,labels=labels,varsToStream = varsToStream)
	stream.InitCSV("test.csv")
	print("Setting open control...") 
	setControlMode(devId, CTRL_OPEN)
	numSteps = 100
	numSeconds = 1.0
	maxVoltage = 3000
	numTimes = 2
	sleepInterval = numSeconds / numSteps

	for time in range(0, numTimes):

		for i in range(0, numSteps):
			sleep(numSeconds / numSteps)
			mV = maxVoltage * (i*1.0 / numSteps)
			setMotorVoltage(devId, mV)
			preamble = """Open control demo... \nRamping up open controller..."""
			stream()
			stream.printData(message=preamble)
			stream.writeToCSV()

		for i in range(0, numSteps):
			sleep(numSeconds / numSteps)
			mV = maxVoltage * ((numSteps - i)*1.0 / numSteps)
			setMotorVoltage(devId, mV)
			preamble = """Open control demo...\nRamping down open controller..."""
			stream()
			stream.printData(message=preamble)
			stream.writeToCSV()

        	del stream

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxOpenControl(devId)	
	except Exception as e:
		print("Broke... ")
		print(str(e))
