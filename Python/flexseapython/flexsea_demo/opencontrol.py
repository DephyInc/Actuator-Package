import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import Stream

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

def fxOpenControl(port, time = 2,num_times = 2, time_resolution = 0.1, maxVoltage = 3000, sign = -1):
	stream = Stream(port,printingRate = 2,labels=labels,varsToStream = varsToStream)
	#stream.InitCSV("test.csv")
	print("Setting open control...")
	setMotorVoltage(stream.devId,0)
	setControlMode(stream.devId, CTRL_OPEN)
	setMotorVoltage(stream.devId,0)
	sleep(0.5)
	numSteps = int((time/2)/time_resolution)
	direction = 1
	for time in range(0, num_times):
		direction = direction * sign

		for i in range(0, numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * (i*1.0 / numSteps)
			setMotorVoltage(stream.devId, mV)
			preamble = """Open control demo... \nRamping up open controller..."""
			stream()
			stream.printData(message=preamble)
			#stream.writeToCSV()

		for i in range(0, numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * ((numSteps - i)*1.0 / numSteps)
			setMotorVoltage(stream.devId, mV)
			preamble = """Open control demo...\nRamping down open controller..."""
			stream()
			stream.printData(message=preamble)
			#stream.writeToCSV()

	del stream
	return True

if __name__ == '__main__':
	ports = sys.argv[1:2]
	try:
		fxOpenControl(ports)	
	except Exception as e:
		print("Broke... ")
		print(str(e))
