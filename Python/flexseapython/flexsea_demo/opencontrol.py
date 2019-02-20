import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import StreamManager

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

def fxOpenControl(devId, time = 2,num_times = 2, time_resolution = 0.1, maxVoltage = 3000, sign = -1):
	stream = StreamManager(devId,printingRate = 2,labels=labels,varsToStream = varsToStream)
	#stream.InitCSV("test.csv")
	print("Setting open control...")
	setMotorVoltage(devId,0)
	setControlMode(devId, CTRL_OPEN)
	setMotorVoltage(devId,0)
	sleep(0.5)
	numSteps = int((time/2)/time_resolution)
	direction = 1
	for time in range(0, num_times):
		direction = direction * sign

		for i in range(0, numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * (i*1.0 / numSteps)
			setMotorVoltage(devId, mV)
			preamble = """Open control demo... \nRamping up open controller..."""
			stream()
			stream.printData(message=preamble)
			#stream.writeToCSV()

		for i in range(0, numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * ((numSteps - i)*1.0 / numSteps)
			setMotorVoltage(devId, mV)
			preamble = """Open control demo...\nRamping down open controller..."""
			stream()
			stream.printData(message=preamble)
			#stream.writeToCSV()

	del stream
	return True

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxOpenControl(devId)	
	except Exception as e:
		print("Broke... ")
		print(str(e))
