import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from streamManager import StreamManager

# Control gain constants
kp = 20
ki = 3

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

def fxTwoPositionControl(devId, delta = 10000, transition_time = 25, resolution = 100):

	stream = StreamManager(devId, printingRate =2, labels=labels, varsToStream=varsToStream)
	result = True
	sleep(0.4)
	stream()
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

	# Intial positions
	setPosition(devId, initialAngle)
	setControlMode(devId, CTRL_POSITION)
	setPosition(devId, initialAngle)
	# Set gains
	setZGains(devId, kp, ki, 0, 0)

	# Select transition rate and positions
	currentPos = 0
	total_time = 200
	positions = [initialAngle,initialAngle + delta]

		# Run demo
	for i in range(0,total_time):
		if i % transition_time == 0:
			result ^= (abs(positions[currentPos] - stream([FX_ENC_ANG])[0]) < resolution)
			currentPos = (currentPos + 1) % 2
			setPosition(devId, positions[currentPos])
		sleep(0.1)
		stream()
		preamble = "Holding position: {}...".format(positions[currentPos])
		stream.printData(message = preamble)

	setControlMode(devId, CTRL_NONE)
	sleep(0.1)
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
