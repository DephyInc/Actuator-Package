import os, sys, math
from time import sleep, time, strftime
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
#Next two lines are used to plot in a browser:
import matplotlib
matplotlib.use('WebAgg')


# Toggle profiling to identify any performance bottlenecks
doProfile=False
if (doProfile):
	import cProfile
	pr = cProfile.Profile()
	# Surround problematic code with following 2 lines:
	# pr.enable()
	# pr.disable()
	# Make following the last line in your code:
	# pr.print_stats(sort='time')

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
	in_array = np.linspace(-np.pi, np.pi, int(num_samples))
	sin_vals = amplitude * np.sin(in_array)
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
def fxHighSpeedTest(port0, baudRate, port1="", controllerType=Controller.current,
	signalType=signal.sine, commandFreq=1000, signalAmplitude=1000, numberOfLoops=40,
	signalFreq=5, cycleDelay=.1, requestJitter=False, jitter=20):

	secondDevice = False
	if (port1 != ""):
		secondDevice = True

	if (secondDevice):
		print("Running high speed test with two devices")
	else:
		print("Running high speed test with one device")

	########### Debug & Data Logging ############
	debugLoggingLevel = 6 # 6 is least verbose, 0 is most verbose
	dataLog = False # Data log logs device data

	delay_time = float(1/(float(commandFreq)))
	print(delay_time)

	########### Open the device and start streaming ############
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

	if(controllerType == Controller.position):
		#Get initial position:
		print('Reading initial position...')
		
		# Give the device time to consume the startStreaming command and start streaming
		sleep(0.1)

		data = fxReadDevice(devId0)
		initialPos0 = data.encoderAngle

		initialPos1 = 0		
		if (secondDevice):
			data = fxReadDevice(devId1)
			initialPos1 = data.encoderAngle
	else:
		initialPos0 = 0
		initialPos1 = 0
	
	# Generate a control profile
	print('Command table:')
	if (signalType == signal.sine):
		samples = sinGenerator(signalAmplitude, signalFreq, commandFreq)
		signalTypeStr = "sine wave"
	elif (signalType == signal.line):
		samples = lineGenerator(signalAmplitude, commandFreq)
		signalTypeStr = "line"
	else:
		assert 0
	print(np.int64(samples))

	# Initialize lists
	requests = []
	measurements0 = []
	measurements1 = []
	times = []
	cycleStopTimes = []
	currentCommandTimes = []
	streamCommandTimes = []
	i = 0
	t0 = 0

	# Prepare controller:
	if (controllerType == Controller.current):
		print("Setting up current control demo")
		fxSetGains(devId0, 300, 50, 0, 0, 0)
		if (secondDevice):
			fxSetGains(devId1, 300, 50, 0, 0, 0)

	elif (controllerType == Controller.position):
		print("Setting up position control demo")
		fxSetGains(devId0, 300, 50, 0, 0, 0)
		if (secondDevice):
			fxSetGains(devId1, 300, 50, 0, 0, 0)
	else:
		assert 0, 'Invalid controllerType'
	
	# Record start time of experiment
	t0 = time()
	for reps in range(0, numberOfLoops):
		for sample in samples:
			if (i % 2 == 0 and requestJitter):
				sample = sample + jitter

			sleep(delay_time)

			# set controller to the next sample
			# read ActPack data
			tReadTime0 = time()
			data0 = fxReadDevice(devId0)
			tReadTime1 = time()
			if (secondDevice):
				data1 = fxReadDevice(devId1)

			if (controllerType == Controller.current):
				tCommandTime0 = time()
				fxSendMotorCommand(devId0, FxCurrent, sample)
				tCommandTime1 = time()
				measurements0.append(data0.motorCurrent)
				if (secondDevice):
					fxSendMotorCommand(devId1, FxCurrent, sample)
					measurements1.append(data1.motorCurrent)

			elif (controllerType == Controller.position):
				fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
				measurements0.append(data0.encoderAngle - initialPos0)
				if (secondDevice):
					fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
					measurements1.append(data1.encoderAngle - initialPos1)

			streamCommandTimes.append(tReadTime1 - tReadTime0)
			currentCommandTimes.append(tCommandTime1 - tCommandTime0)
			times.append(time() - t0)
			requests.append(sample)
			i = i + 1

		# Delay between cycles (sine wave only)
		if (signalType == signal.sine):
			for j in range(int(cycleDelay/delay_time)):

				sleep(delay_time)
				# Read data from ActPack
				data0 = fxReadDevice(devId0)
				if (secondDevice):
					data1 = fxReadDevice(devId1)

				if (controllerType == Controller.current):
					measurements0.append(data0.motorCurrent)
					if (secondDevice):
						measurements1.append(data1.motorCurrent)

				elif (controllerType == Controller.position):
					measurements0.append(data0.encoderAngle - initialPos0)
					if (secondDevice):
						measurements1.append(data1.encoderAngle - initialPos1)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

		# We'll draw a line at the end of every period
		cycleStopTimes.append(time() - t0)
	elapsed_time = time() - t0

	fxCloseAll()

	######## End of Main Code #########

	######## Plotting Code, you can edit this ##################

	actual_period = cycleStopTimes[0]
	actual_frequency = 1 / actual_period
	command_frequency = i / elapsed_time
	print("i: " + str(i) + ", elapsed_time: " + str(elapsed_time))

	if (controllerType == Controller.current):
		plt.figure(1)
		title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
			str(signalAmplitude) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
		plt.plot(times, requests, color = 'b', label = 'desired current')
		plt.plot(times, measurements0, color = 'r', label = 'measured current')
		plt.xlabel("Time (s)")
		plt.ylabel("Motor current (mA)")
		plt.title(title)

		plt.legend(loc='upper right')

		# Draw a vertical line at the end of each cycle
#		for endpoints in cycleStopTimes:
#			plt.axvline(x=endpoints)

	elif (controllerType == Controller.position):
		plt.figure(1)
		title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
			str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
		plt.plot(times, requests, color = 'b', label = 'desired position')
		plt.plot(times, measurements0, color = 'r', label = 'measured position')
		plt.xlabel("Time (s)")
		plt.ylabel("Encoder position")
		plt.title(title)

		plt.legend(loc='upper right')

		# Draw a vertical line at the end of each cycle
		for endpoints in cycleStopTimes:
			plt.axvline(x=endpoints)

	###### begin command times plotting ########################################33

	# Babar: Following 6 lines are legacy code. Remove eventually.
	#plt.figure(2)
	#title = "Current and stream command times (aggregate)"
	#plt.title(title)
	#plt.plot(currentCommandTimes,color='b', label='Current Command Times')
	#plt.plot(streamCommandTimes, color='r', label='Stream Command Times')
	#plt.legend(loc='upper right')


	plt.figure(2)
	# Convert command times into millisec
	currentCommandTimes = [i * 1000 for i in currentCommandTimes]
	#np.savetxt('JFD.txt', np.array(currentCommandTimes), fmt='%.10f')
	plt.plot(currentCommandTimes, color='b', label='Current Command Times')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	plt.figure(3)
	plt.yscale('log')
	plt.hist(currentCommandTimes, bins=100, label = 'Current Commands')
	plt.yscale('log')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	plt.figure(4)
	streamCommandTimes = [i * 1000 for i in streamCommandTimes]
	# Convert command times into millisec
	plt.plot(streamCommandTimes, color='b', label='Stream Command Times')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	plt.figure(5)
	plt.yscale('log')
	plt.hist(streamCommandTimes, bins=100, label = 'Stream Commands')
	plt.yscale('log')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")


	##### end command times plotting ########################################33

	if (secondDevice):
		if (controllerType == Controller.current):
			plt.figure(2)
			title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(signalAmplitude) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			plt.plot(times, requests, color = 'b', label = 'desired current')
			plt.plot(times, measurements1, color = 'r', label = 'measured current')
			plt.xlabel("Time (s)")
			plt.ylabel("Motor current (mA)")
			plt.title(title)

			plt.legend(loc='upper right')

			# Draw a vertical line at the end of each cycle
			for endpoints in cycleStopTimes:
				plt.axvline(x=endpoints)

		elif (controllerType == Controller.position):
			plt.figure(2)
			title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			plt.plot(times, requests, color = 'b', label = 'desired position')
			plt.plot(times, measurements1, color = 'r', label = 'measured position')
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
