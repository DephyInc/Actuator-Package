import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import Stream

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

def fxPositionControl(port, time = 2, time_step = 0.1,  resolution = 100):

	stream = Stream(port,printingRate = 2, labels=labels,varsToStream = varsToStream)
	sleep(0.4)
	result = True
	initialData = stream()
	stream.printData()
	initialAngle = stream([FX_ENC_ANG])[0]	
	timeout = 100
	timeoutCount = 0
	while(initialAngle == None):
		timeoutCount = timeoutCount + 1
		if(timeoutCount > timeout):
			print("Timed out waiting for valid encoder value...")
			sys.exit(1)
		else:
			sleep(0.1)
			initialAngle = stream([FX_ENC_ANG])[0]

	setPosition(stream.devId, initialAngle)
	setControlMode(stream.devId, CTRL_POSITION)
	setPosition(stream.devId, initialAngle)
	setGains(stream.devId, 50, 3, 0, 0)
	num_time_steps = int(time/time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		preamble = "Holding position: {}...".format(initialAngle)
		stream()
		stream.printData(message=preamble)
		currentAngle = stream([FX_ENC_ANG])[0]
		result ^= (abs(initialAngle - currentAngle) < resolution)

	setControlMode(stream.devId, CTRL_NONE)

	del stream
	return result

if __name__ == '__main__':
	ports = sys.argv[1:2]
	try:
		fxPositionControl(ports)	
	except Exception as e:
		print("broke: " + str(e))
		pass
