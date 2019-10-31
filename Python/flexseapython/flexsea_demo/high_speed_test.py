import os, sys, math
from time import sleep, time, strftime
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
#Next two lines are used to plot in a browser:
import matplotlib
matplotlib.use('WebAgg')

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(pardir)
sys.path.append(pardir)
from fxUtil import *

# Controller type to send to controller
class Controller(Enum):
	position = 1
	current = 2

# Signal type to send to controller
class signal(Enum):
	sine = 1
	line = 2

# Generate a sine wave of a specific amplitude and frequency
def sinGenerator(amplitude, frequency, offset, commandFreq):
	num_samples = commandFreq / frequency
	in_array = np.linspace(-np.pi, np.pi, num_samples)
	sin_vals = amplitude * np.sin(in_array) + offset
	return sin_vals

# generate a line with specific amplitude
def lineGenerator(amplitude, commandFreq):
	num_samples = commandFreq
	line_vals = [ amplitude for i in range(num_samples) ]
	return line_vals

# Port: port with outgoing serial connection to ActPack
# Baud Rate : baud rate of outgoing serial connection to ActPack
# Controller Type: Position controller or current controller
# Signal Type: Sine wave or line
# Command Freq: Desired frequency of issuing commands to controller, actual 
#	command frequency will be slower due to OS overhead.
# Signal Amplitude: Amplitude of signal to send to controller. Encoder position
#	if position controller, current in mA if current controller
# Number of Loops: Number of times to send desired signal to controller
# Signal Freq: Frequency of sine wave if using sine wave signal
# Cycle Delay: Delay between signals sent to controller, use with sine wave only
# Request Jitter: Add jitter amount to every other sample sent to controller
# Jitter: Amount of jitter
def fxHighSpeedTest(port, baudRate, controllerType = Controller.position, signalType = signal.sine, commandFreq = 1000, signalAmplitude = 10000, numberOfLoops = 10, signalFreq = 5, cycleDelay = .1, requestJitter = False, jitter = 20):
	
	debugLoggingLevel = 0 # 6 is least verbose, 0 is most verbose
	dataLog = False # Data log logs device data

	delay_time = float(1/(float(commandFreq)))
	print(delay_time)

	########### Open the device and start streaming ############
	devId = fxOpen(port, baudRate, commandFreq, debugLoggingLevel) 
	fxStartStreaming(devId, dataLog)
	print('Connected to device with ID ',devId)

	############# Main Code ############
	######## Make your changes here #########
	
	if(controllerType == Controller.position):
		#Get initial position:
		print('Reading initial position...')
		data = fxReadDevice(devId)
		initialPos = data._execute._motor_data._motor_angle
		timeout = 100
		timeoutCount = 0
		while(initialPos == None):
			print('Loop...')
			timeoutCount = timeoutCount + 1
			if(timeoutCount > timeout):
				print("Timed out waiting for valid encoder value...")
				sys.exit(1)
			else:
				sleep(delay_time)
				data = fxReadDevice(devId)
				initialPos = data._execute._motor_data._motor_angle
	else:
		initialPos = 0
	
	# Generate a control profile
	print('Command table:')
	if (signalType == signal.sine):
		samples = sinGenerator(signalAmplitude, signalFreq, initialPos, commandFreq)
		signalTypeStr = "sine wave"
	elif (signalType == signal.line):
		samples = lineGenerator(signalAmplitude, commandFreq)
		signalTypeStr = "line"
	else:
		assert 0
	print(np.int64(samples))

	# Initialize lists
	requests = []
	measurements = []
	times = []
	cycleStopTimes = []
	i = 0
	t0 = 0

	# Prepare controller:
	if (controllerType == Controller.current):
		print("Setting up current control demo")
		fxSetGains(devId, 300, 50, 0, 0, 0)
	elif (controllerType == Controller.position):
		print("Setting up position control demo")
		fxSetGains(devId, 300, 50, 0, 0, 0)
	else:
		assert 0
	
	# Record start time of experiment
	t0 = time()
	for reps in range(0, numberOfLoops):
		for sample in samples:
			if (i % 2 == 0 and requestJitter):
				sample = sample + jitter

			sleep(delay_time)

			# set controller to the next sample
			# read ActPack data
			data = fxReadDevice(devId)
			if (controllerType == Controller.current):
				fxSendMotorCommand(devId, FxCurrent, sample)
				measurements.append(data._execute._motor_data._motor_current)
			elif (controllerType == Controller.position):
				fxSendMotorCommand(devId, FxPosition, sample - initialPos)
				measurements.append(data._execute._motor_data._motor_angle)


			times.append(time() - t0)
			requests.append(sample)
			i = i + 1

		# Delay between cycles (sine wave only)
		if (signalType == signal.sine):
			for j in range(int(cycleDelay/delay_time)):

				sleep(delay_time)
				# Read data from ActPack
				data = fxReadDevice(devId)
				if (controllerType == Controller.current):
					measurements.append(data._execute._motor_data._motor_current)

				elif (controllerType == Controller.position):
					measurements.append(data._execute._motor_data._motor_angle)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

		# We'll draw a line at the end of every period
		cycleStopTimes.append(time() - t0)
	elapsed_time = time() - t0

	######## End of Main Code #########

	######## Plotting Code, you can edit this ##################

	actual_period = cycleStopTimes[0]
	actual_frequency = 1 / actual_period
	command_frequency = i / elapsed_time
	print("i: " + str(i) + ", elapsed_time: " + str(elapsed_time))

	if (controllerType == Controller.current):
		title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
			str(signalAmplitude) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
		plt.plot(times, requests, color = 'b', label = 'desired current')
		plt.plot(times, measurements, color = 'r', label = 'measured current')
		plt.xlabel("Time (s)")
		plt.ylabel("Motor current (mA)")

	elif (controllerType == Controller.position):
		title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
			str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
		plt.plot(times, requests, color = 'b', label = 'desired position')
		plt.plot(times, measurements, color = 'r', label = 'measured position')
		plt.xlabel("Time (s)")
		plt.ylabel("Encoder position")

	plt.title(title)

	plt.legend(loc='upper right')

	# Draw a vertical line at the end of each cycle
	for endpoints in cycleStopTimes:
		plt.axvline(x=endpoints)
	plt.show()

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxHighSpeedTest(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
