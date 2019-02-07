import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from streamManager import StreamManager

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

def fxPositionControl(devId, resolution = 100):

	stream = StreamManager(devId,printingRate = 2, labels=labels,varsToStream = varsToStream)
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

	setPosition(devId, initialAngle)
	setControlMode(devId, CTRL_POSITION)
	setPosition(devId, initialAngle)
	setZGains(devId, 50, 3, 0, 0)

	for i in range(0, 100):
		sleep(0.1)
		preamble = "Holding position: {}...".format(initialAngle)
		stream()
                stream.printData(message=preamble)
                currentAngle = stream([FX_ENC_ANG])[0]
                result ^= (abs(initialAngle - currentAngle) < resolution)

	setControlMode(devId, CTRL_NONE)

	del stream
        return result

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxPositionControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
