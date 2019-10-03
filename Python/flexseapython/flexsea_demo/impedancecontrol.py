import os, sys
from time import sleep, time, strftime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('WebAgg')

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import Stream

# Control gain constants
kp = 100
ki = 32
K = 325
B = 0

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

def fxImpedanceControl(port, baudRate, expTime = 5, time_step = 0.01, delta = 7500, transition_time = 1.5, resolution = 500):

	stream = Stream(port, baudRate, printingRate = 2, labels=labels, varsToStream=varsToStream, updateFreq=500)
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
			
	# Initialize lists - matplotlib
	requests = []
	measurements = []
	times = []
	#cycleStopTimes = []
	i = 0
	t0 = 0

	# Intial position
	setPosition(stream.devId, initialAngle)
	setControlMode(stream.devId, CTRL_IMPEDANCE)
	setPosition(stream.devId, initialAngle)
	# Set gains
	setGains(stream.devId, K, B, kp, ki)

	# Select transition rate and positions
	currentPos = 0
	num_time_steps = int(expTime/time_step)
	positions = [initialAngle,initialAngle + delta]
	sleep(0.4)
	
	# Record start time of experiment
	t0 = time()
	
	# Run demo
	print(result)
	for i in range(num_time_steps):
		measuredPos = stream([FX_ENC_ANG])[0]
		if i % transition_steps == 0:
			delta = abs(positions[currentPos] - measuredPos)
			result &= delta < resolution
			currentPos = (currentPos + 1) % 2
			setPosition(stream.devId, positions[currentPos])
		sleep(time_step)
		stream()
		preamble = "Holding position: {}...".format(positions[currentPos])
		stream.printData(message = preamble)
		# Plotting:
		measurements.append(measuredPos)
		times.append(time() - t0)
		requests.append(positions[currentPos])

	# Disable controller:
	setControlMode(stream.devId, CTRL_NONE)
	sleep(0.1)
	
	# Plot before we exit:
	title = "Impedance Control Demo"
	plt.plot(times, requests, color = 'b', label = 'Desired position')
	plt.plot(times, measurements, color = 'r', label = 'Measured position')
	plt.xlabel("Time (s)")
	plt.ylabel("Encoder position")
	plt.title(title)
	plt.legend(loc='upper right')
	plt.show()
	
	del stream
	return result

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxPositionControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
