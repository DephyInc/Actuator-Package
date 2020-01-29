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
def sinGenerator(amplitude, frequency, commandFreq):
	num_samples = commandFreq / frequency
	print("number of samples is: ", num_samples)
	in_array = np.linspace(-np.pi, np.pi, num_samples)
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals

# generate a line with specific amplitude
def lineGenerator(amplitude, commandFreq):
	num_samples = commandFreq
	line_vals = [ amplitude for i in range(num_samples) ]
	return line_vals

# Set the device(s) for current control
def setCurrentCtrl(devId0, devId1, secondDevice):
	fxSetGains(devId0, 300, 50, 0, 0, 0)
	if (secondDevice):
		fxSetGains(devId1, 300, 50, 0, 0, 0)

# Set the device(s) for position control
def setPositionCtrl(devId0, devId1, secondDevice):
	fxSetGains(devId0, 300, 50, 0, 0, 0)
	if (secondDevice):
		fxSetGains(devId1, 300, 50, 0, 0, 0)

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
# Request Jitter: Add jitter amount to every other sample sent to controller
# Jitter: Amount of jitter
def fxHighStressTest(port0, baudRate, port1 = "", controllerType = Controller.position, signalType = signal.sine, commandFreq = 1000, signalAmplitude = 10000, numberOfLoops = 5, signalFreq = 5, requestJitter = True, jitter = 500):

	########### One vs two devices ############
	secondDevice = False
	if (port1 != ""):
		secondDevice = True

	if (secondDevice):
		print("Running high stress test with two devices")
	else:
		print("Running high stress test with one device")

	########### Debug & Data Logging ############
	debugLoggingLevel = 0 # 6 is least verbose, 0 is most verbose
	dataLog = False # Data log logs device data

	delay_time = float(1/(float(commandFreq)))
	print(delay_time)

	########### Open the device(s) and start streaming ############
	devId0 = fxOpen(port0, baudRate, debugLoggingLevel) 
	fxStartStreaming(devId0, commandFreq, dataLog)
	print('Connected to device with ID ',devId0)

	devId1 = -1
	if (secondDevice):
		devId1 = fxOpen(port1, baudRate, debugLoggingLevel) 
		fxStartStreaming(devId1, commandFreq, dataLog)
		print('Connected to device with ID ',devId1)

	############# Main Code ############
	######## Make your changes here #########

	# Get initial position:
	print('Reading initial position...')
	
	# Give the device time to consume the startStreaming command and start streaming
	sleep(0.1)

	data = fxReadDevice(devId0)
	initialPos0 = data.encoderAngle

	initialPos1 = 0
	if (secondDevice):
		data = fxReadDevice(devId1)
		initialPos1 = data.encoderAngle
	
	# Generate a control profiles
	print('Command table #1 - Sine:')
	sineSamples = sinGenerator(signalAmplitude, signalFreq, commandFreq)
	print(np.int64(sineSamples))
	print('Command table #2 - Line:')
	lineSamples = lineGenerator(signalAmplitude, commandFreq)
	#print(np.int64(lineSamples))
	
	# Initialize lists
	currentRequests = []
	positionRequests = []
	currentMeasurements0 = []
	positionMeasurements0 = []
	currentMeasurements1 = []
	positionMeasurements1 = []
	times = []
	cycleStopTimes = []
	i = 0
	t0 = 0

	# Record start time of experiment
	t0 = time()
	for reps in range(0, numberOfLoops):
		
		print("Rep #",reps,"out of",numberOfLoops)
		print("------------")
		
		# Step 0: set position controller
		# -------------------------------
		print("Step 0: set position controller")
		setPositionCtrl(devId0, devId1, secondDevice)
		
		# Step 1: position sine wave
		# --------------------------
		print("Step 1: position sine wave")
		for sample in sineSamples:
			if (i % 2 == 0 and requestJitter):
				sample = sample + jitter

			sleep(delay_time)

			# set controller to the next sample
			# read ActPack data
			data0 = fxReadDevice(devId0)
			if (secondDevice):
				data1 = fxReadDevice(devId1)

			# Position setpoint:
			fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
			currentMeasurements0.append(data0.motorCurrent)
			positionMeasurements0.append(data0.encoderAngle - initialPos0)
			if (secondDevice):
				fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
				currentMeasurements1.append(data1.motorCurrent)
				positionMeasurements1.append(data1.encoderAngle - initialPos1)

			times.append(time() - t0)
			currentRequests.append(0)
			positionRequests.append(sample)
			i = i + 1

		# Step 2: set current controller
		# -------------------------------
		print("Step 2: set current controller")
		#setPositionCtrl(devId0, devId1, secondDevice)
		
		# Step 3: current setpoint
		# --------------------------
		print("Step 3: current line")
		for sample in lineSamples:
			if (i % 2 == 0 and requestJitter):
				sample = sample + jitter

			sleep(delay_time)

			# set controller to the next sample
			# read ActPack data
			data0 = fxReadDevice(devId0)
			if (secondDevice):
				data1 = fxReadDevice(devId1)

			# Position setpoint:
			fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
			currentMeasurements0.append(data0.motorCurrent)
			positionMeasurements0.append(data0.encoderAngle - initialPos0)
			if (secondDevice):
				fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
				currentMeasurements1.append(data1.motorCurrent)
				positionMeasurements1.append(data1.encoderAngle - initialPos1)

			times.append(time() - t0)
			currentRequests.append(0)
			positionRequests.append(sample)
			i = i + 1
			
		# We'll draw a line at the end of every period
		cycleStopTimes.append(time() - t0)
	elapsed_time = time() - t0

	fxClose(devId0)
	fxClose(devId1)

	######## End of Main Code #########

	######## Plotting Code, you can edit this ##################

	actual_period = cycleStopTimes[0]
	actual_frequency = 1 / actual_period
	command_frequency = i / elapsed_time
	print("i: " + str(i) + ", elapsed_time: " + str(elapsed_time))

	# Current Plot:
	plt.figure(1)
	title = "Motor Current (" + "{:.2f}".format(actual_frequency) + " Hz, " + \
		str(signalAmplitude) + " mA amplitude " + " and " + "{:.2f}".format(command_frequency) + " Hz commands )"
	plt.plot(times, currentRequests, color = 'b', label = 'desired current')
	plt.plot(times, currentMeasurements0, color = 'r', label = 'measured current')
	plt.xlabel("Time (s)")
	plt.ylabel("Motor current (mA)")
	plt.title(title)

	plt.legend(loc='upper right')

	# Draw a vertical line at the end of each cycle
	for endpoints in cycleStopTimes:
		plt.axvline(x=endpoints)

	# Position Plot:
	plt.figure(2)
	title = "Motor Position (" + "{:.2f}".format(actual_frequency) + " Hz, " + \
		str(signalAmplitude) + " ticks amplitude " + " and " + "{:.2f}".format(command_frequency) + " Hz commands)"
	plt.plot(times, positionRequests, color = 'b', label = 'desired position')
	plt.plot(times, positionMeasurements0, color = 'r', label = 'measured position')
	plt.xlabel("Time (s)")
	plt.ylabel("Encoder position")
	plt.title(title)

	plt.legend(loc='upper right')

	# Draw a vertical line at the end of each cycle
	for endpoints in cycleStopTimes:
		plt.axvline(x=endpoints)

	# if (secondDevice):
		# if (controllerType == Controller.current):
			# plt.figure(2)
			# title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				# str(signalAmplitude) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			# plt.plot(times, requests, color = 'b', label = 'desired current')
			# plt.plot(times, measurements1, color = 'r', label = 'measured current')
			# plt.xlabel("Time (s)")
			# plt.ylabel("Motor current (mA)")
			# plt.title(title)

			# plt.legend(loc='upper right')

			# # Draw a vertical line at the end of each cycle
			# for endpoints in cycleStopTimes:
				# plt.axvline(x=endpoints)

		# elif (controllerType == Controller.position):
			# plt.figure(2)
			# title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				# str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			# plt.plot(times, requests, color = 'b', label = 'desired position')
			# plt.plot(times, measurements1, color = 'r', label = 'measured position')
			# plt.xlabel("Time (s)")
			# plt.ylabel("Encoder position")
			# plt.title(title)

			# plt.legend(loc='upper right')

			# # Draw a vertical line at the end of each cycle
			# for endpoints in cycleStopTimes:
				# plt.axvline(x=endpoints)

	plt.show()

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxHighStressTest(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
