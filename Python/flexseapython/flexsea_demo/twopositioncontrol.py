import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import StreamManager

# Control gain constants
kp = 50
ki = 5

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

def fxTwoPositionControl(devId, time = 4, time_step =  0.1, delta = 10000, transition_time = 1, resolution = 500):

	stream = StreamManager(devId, printingRate =2, labels=labels, varsToStream=varsToStream)
	result = True
	stream()
	stream.printData()
	initialAngle = stream([FX_ENC_ANG])[0]	
	timeout = 100
	timeoutCount = 0
	transition_steps = int(transition_time / time_step)
	while(initialAngle == None):
		timeoutCount = timeoutCount + 1
		if(timeoutCount > timeout):
			print("Timed out waiting for valid encoder value...")
			sys.exit(1)
		else:
			sleep(time_step)	
			initialAngle = stream([FX_ENC_ANG])[0]

	# Intial positions
	setPosition(devId, initialAngle)
	setControlMode(devId, CTRL_POSITION)
	setPosition(devId, initialAngle)
	# Set gains
	setZGains(devId, kp, ki, 0, 0)

	# Select transition rate and positions
	currentPos = 0
	num_time_steps = int(time/time_step)
	positions = [initialAngle,initialAngle + delta]
	sleep(0.4)
		# Run demo
	print(result)
	for i in range(num_time_steps):
		if i % transition_steps == 0:
			delta = abs(positions[currentPos] - stream([FX_ENC_ANG])[0])
			result &= delta < resolution
			currentPos = (currentPos + 1) % 2
			setPosition(devId, positions[currentPos])
		sleep(time_step)
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
