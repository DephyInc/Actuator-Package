import os, sys
from time import sleep, time, strftime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('WebAgg')
from fxUtil import *

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

def printDevice(actPackState):
	clearTerminal()
	print('State time:    ', actPackState.timestamp)
	print('Accel X        ', actPackState.accelx)
	print('Accel Y:       ', actPackState.accely)
	print('Accel Z:       ', actPackState.accelz)
	print('Gyro X:        ', actPackState.gyrox)
	print('Gyro Y:        ', actPackState.gyroy)
	print('Gyro Z:        ', actPackState.gyroz)
	print('Motor angle:   ', actPackState.encoderAngle)
	print('Motor voltage: ', actPackState.motorVoltage)

def fxTwoPositionControl(port, baudRate, expTime = 10, time_step = 0.1, delta = 10000,
		transition_time = 1.5, resolution = 100):
	# Open device
	devId = fxOpen(port, baudRate, 0)
	fxStartStreaming(devId, resolution, shouldLog = False)
	sleep(0.1)

	# Setting initial angle and angle waypoints
	actPackState = fxReadDevice(devId)
	printDevice(actPackState)
	initialAngle = actPackState.encoderAngle

	# Setting angle waypoints
	positions = [initialAngle, initialAngle + delta]
	current_pos = 0
	num_pos = 2

	# Setting loop duration and transition rate
	num_time_steps = int(expTime/time_step)
	transition_steps = int(transition_time/time_step)

	# Setting gains (devId, kp, ki, kd, K, B)
	fxSetGains(devId, 150, 100, 0, 0, 0)

	# Setting position control at initial position
	fxSendMotorCommand(devId, FxPosition, initialAngle)

	# Matplotlib - initialize lists
	requests = []
	measurements = []
	times = []
	i = 0
	t0 = 0

	sleep(0.4)
	t0 = time()

	# Start two position control
	for i in range(num_time_steps):
		actPackState = fxReadDevice(devId)
		printDevice(actPackState)
		print('Holding position:', positions[current_pos], '\n')
		measuredPos = actPackState.encoderAngle

		if i % transition_steps == 0:
			current_pos = (current_pos + 1) % num_pos
			fxSendMotorCommand(devId, FxPosition, positions[current_pos])
		sleep(time_step)

		# Plotting
		times.append(time() - t0)
		requests.append(positions[current_pos])
		measurements.append(measuredPos)

	# Close device and do device cleanup
	close_check = fxClose(devId)

	# Plot before exit:
	title = "Two Position Control Demo"
	plt.plot(times, requests, color = 'b', label = 'Desired position')
	plt.plot(times, measurements, color = 'r', label = 'Measured position')
	plt.xlabel("Time (s)")
	plt.ylabel("Encoder position")
	plt.title(title)
	plt.legend(loc='upper right')
	if (os.name == 'nt'):
		print('\nIn Windows, press Ctrl+BREAK to exit. Ctrl+C may not work.')
	plt.show()

	return close_check

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxPositionControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
