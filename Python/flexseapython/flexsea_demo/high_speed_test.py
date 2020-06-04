import os, sys, math
from time import sleep, time, strftime
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from flexseapython.fxUtil import *
from flexseapython.fxPlotting import *
matplotlib.use('WebAgg')

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(pardir)
sys.path.append(pardir)

# # Controller type to send to controller
# # ToDo: this was in High Speed Test. Is that needed? Duplicated?
# class Controller(Enum):
#  position = 1
#  current = 2
#
# Signal type to send to controller
class signal(Enum):
 sine = 1
 line = 2

# Generate a sine wave of a specific amplitude and frequency
def sinGenerator(amplitude, frequency, commandFreq):
	num_samples = commandFreq / frequency
	print("number of samples is: ", int(num_samples))
	in_array = np.linspace(-np.pi, np.pi, int(num_samples))
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals

# Generate a line with specific amplitude
def lineGenerator(amplitude, commandFreq):
	num_samples = commandFreq
	line_vals = [ amplitude for i in range(num_samples) ]
	return line_vals

def fxHighSpeedTest(port0, baudRate, port1 = "", controllerType = hssCurrent,
	signalType = signal.sine, commandFreq = 1000, signalAmplitude = 1000, numberOfLoops = 30,
	signalFreq = 5, cycleDelay = 0.1, requestJitter = False, jitter = 20):
	"""
	baudRate		Baud rate of outgoing serial connection to ActPack
	port			Port with outgoing serial connection to ActPack
	controllerType	Position controller or current controller
	signalType		Sine wave or line
	commandFreq		Desired frequency of issuing commands to controller, actual 
					command frequency will be slower due to OS overhead.
	signalAmplitude	Amplitude of signal to send to controller. Encoder position
					if position controller, current in mA if current controller
	nmberOfLoops	Number of times to send desired signal to controller
	signalFreq		Frequency of sine wave if using sine wave signal
	cycleDelay		Delay between signals sent to controller, use with sine wave only
	requestJitter	Add jitter amount to every other sample sent to controller
	jitter			Amount of jitter
	"""
	secondDevice = False
	if(port1 != ""):
		secondDevice = True

	if(secondDevice):
		print("Running High Speed Test with two devices")
	else:
		print("Running High Speed Test with one device")

	# Debug & Data Logging
	debugLoggingLevel = 6 	# 6 is least verbose, 0 is most verbose
	dataLog = False 		# Data log logs device data

	delay_time = float(1 / (float(commandFreq)))
	print(delay_time)

	# Open the device and start streaming
	devId0 = fxOpen(port0, baudRate, debugLoggingLevel) 
	fxStartStreaming(devId0, commandFreq, dataLog)
	print('Connected to device 0 with ID', devId0)

	devId1 = -1
	if(secondDevice):
		devId1 = fxOpen(port1, baudRate, debugLoggingLevel) 
		fxStartStreaming(devId1, commandFreq, dataLog)
		print('Connected to device 1 with ID', devId1)

	# Get initial position:
	if(controllerType == hssPosition):#Controller.position):
		#Get initial position:
		print('Reading initial position...')		
		# Give the device time to consume the startStreaming command and start streaming
		sleep(0.1)
		data = fxReadDevice(devId0)
		initialPos0 = data.encoderAngle

		initialPos1 = 0
		if(secondDevice):
			data = fxReadDevice(devId1)
			initialPos1 = data.encoderAngle
	else:
		initialPos0 = 0
		initialPos1 = 0
	
	# Generate a control profile
	print('Command table:')
	if(signalType == signal.sine):
		samples = sinGenerator(signalAmplitude, signalFreq, commandFreq)
		signalTypeStr = "sine wave"
	elif(signalType == signal.line):
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

	# Prepare controller:
	if(controllerType == hssCurrent):	#Controller.current):
		print("Setting up current control demo. Low current, high frequency")
		fxSetGains(devId0, 300, 50, 0, 0, 0)
		if(secondDevice):
			fxSetGains(devId1, 300, 50, 0, 0, 0)

	elif(controllerType == hssPosition ):#Controller.position):
		print("Setting up position control demo")
		fxSetGains(devId0, 300, 50, 0, 0, 0)
		if(secondDevice):
			fxSetGains(devId1, 300, 50, 0, 0, 0)
	else:
		assert 0, 'Invalid controllerType'

	# Record start time of experiment
	i = 0
	t0 = time()
	loopCtr = 0
	for reps in range(0, numberOfLoops):
		loopCtr += 1
		elapsedTime = time() - t0
		printLoopCountAndTime(loopCtr, numberOfLoops, elapsedTime)
		for sample in samples:
			if(i % 2 == 0 and requestJitter):
				sample = sample + jitter

			sleep(delay_time)

			# set controller to the next sample
			# read ActPack data
			tReadTime0 = time()
			data0 = fxReadDevice(devId0)
			tReadTime1 = time()
			if(secondDevice):
				data1 = fxReadDevice(devId1)

			if(controllerType == hssCurrent):	#Controller.current):
				tCommandTime0 = time()
				fxSendMotorCommand(devId0, FxCurrent, sample)
				tCommandTime1 = time()
				measurements0.append(data0.motorCurrent)
				if(secondDevice):
					fxSendMotorCommand(devId1, FxCurrent, sample)
					measurements1.append(data1.motorCurrent)

			elif(controllerType == hssPosition):	#Controller.position):
				fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
				measurements0.append(data0.encoderAngle - initialPos0)
				if(secondDevice):
					fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
					measurements1.append(data1.encoderAngle - initialPos1)

			streamCommandTimes.append(tReadTime1 - tReadTime0)
			currentCommandTimes.append(tCommandTime1 - tCommandTime0)
			times.append(time() - t0)
			requests.append(sample)
			i = i + 1

		# Delay between cycles (sine wave only)
		if(signalType == signal.sine):
			for j in range(int(cycleDelay/delay_time)):

				sleep(delay_time)
				# Read data from ActPack
				data0 = fxReadDevice(devId0)
				if(secondDevice):
					data1 = fxReadDevice(devId1)

				if(controllerType == hssCurrent):	#Controller.current):
					measurements0.append(data0.motorCurrent)
					if(secondDevice):
						measurements1.append(data1.motorCurrent)

				elif(controllerType == hssPosition):	#.position):
					measurements0.append(data0.encoderAngle - initialPos0)
					if(secondDevice):
						measurements1.append(data1.encoderAngle - initialPos1)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

		# We'll draw a line at the end of every period
		cycleStopTimes.append(time() - t0)

	# Disable the controller, send 0 PWM
	fxSendMotorCommand(devId0, FxNone, 0)
	fxSendMotorCommand(devId1, FxNone, 0)
	sleep(0.1)
	# End of Main Code
	
	# Plotting Code begins here

	elapsedTime = time() - t0
	actualPeriod = cycleStopTimes[0]
	actualFrequency = 1 / actualPeriod
	commandFrequency = i / elapsedTime

	# Figure: setpoint, desired vs measured (1st device)
	fig = 1	# First time, functions will increment
	fig = plotSetpointVsDesired(devId0, fig, controllerType, actualFrequency, signalAmplitude, signalTypeStr, commandFrequency, times,
						requests, measurements0, cycleStopTimes)

	fig = plotExpStats(devId0, fig, currentCommandTimes, streamCommandTimes)

	# Figure: setpoint, desired vs measured (2nd device)
	if(secondDevice):
		plotSetpointVsDesired(devId1, fig, controllerType, actualFrequency, signalAmplitude, signalTypeStr, commandFrequency,
						times, requests, measurements1, cycleStopTimes)

	if(os.name == 'nt'):
		print('\nIn Windows, press Ctrl+BREAK to exit. Ctrl+C may not work.')
	plt.show()
	
	fxCloseAll()

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxHighSpeedTest(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
