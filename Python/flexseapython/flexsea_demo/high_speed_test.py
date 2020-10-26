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

# Signal type to send to controller
class signal(Enum):
	sine = 1
	line = 2

def fxHighSpeedTest(port0, baudRate, port1 = "", controllerType = hssCurrent,
	signalType = signal.sine, commandFreq = 1000, signalAmplitude = 1000, numberOfLoops = 4,
	signalFreq = 5, cycleDelay = 0.1, requestJitter = False, jitter = 20):
	"""
	baudRate		Baud rate of outgoing serial connection to ActPack
	portX			Port with outgoing serial connection to ActPack
	controllerType	Position controller or current controller
	signalType		Sine wave or line
	commandFreq		Desired frequency of issuing commands to controller, actual 
					command frequency will be slower due to OS overhead.
	signalAmplitude	Amplitude of signal to send to controller. Encoder position
					if position controller, current in mA if current controller
	numberOfLoops	Number of times to send desired signal to controller
	signalFreq		Frequency of sine wave if using sine wave signal
	cycleDelay		Delay between signals sent to controller, use with sine wave only
	requestJitter	Add jitter amount to every other sample sent to controller
	jitter			Amount of jitter
	"""

	# One vs two devices
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
	if(controllerType == hssPosition):
		#Get initial position:
		print('Reading initial position...')
		# Give the device time to consume the startStreaming command and start streaming
		sleep(0.1)
		data = fxReadDevice(devId0)
		initialPos0 = data.mot_ang

		initialPos1 = 0
		if(secondDevice):
			data = fxReadDevice(devId1)
			initialPos1 = data.mot_ang
	else:
		initialPos0 = 0
		initialPos1 = 0
	
	# Generate a control profile
	print('Command table:')
	if(signalType == signal.sine):
		samples = sinGenerator(signalAmplitude, signalFreq, commandFreq)
		signalTypeStr = "sine wave"
	elif(signalType == signal.line):
		samples = lineGenerator(signalAmplitude, 1, commandFreq)
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
	dev0WriteCommandTimes = []
	dev1WriteCommandTimes = []
	dev0ReadCommandTimes = []
	dev1ReadCommandTimes = []

	# Prepare controller:
	if(controllerType == hssCurrent):
		print("Setting up current control demo. Low current, high frequency")
		fxSetGains(devId0, 300, 50, 0, 0, 0, 0)
		if(secondDevice):
			fxSetGains(devId1, 300, 50, 0, 0, 0, 0)

	elif(controllerType == hssPosition):
		print("Setting up position control demo")
		fxSetGains(devId0, 300, 50, 0, 0, 0, 0)
		if(secondDevice):
			fxSetGains(devId1, 300, 50, 0, 0, 0, 0)
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

			# Read ActPack data
			dev0ReadTimeBefore = time()
			data0 = fxReadDevice(devId0)
			dev0ReadTimeAfter = time()
			if(secondDevice):
				dev1ReadTimeBefore = time()
				data1 = fxReadDevice(devId1)
				dev1ReadTimeAfter = time()

			# Write setpoint
			if(controllerType == hssCurrent):
				dev0WriteTimeBefore = time()
				fxSendMotorCommand(devId0, FxCurrent, sample)
				dev0WriteTimeAfter = time()
				measurements0.append(data0.mot_cur)
				if(secondDevice):
					dev1WriteTimeBefore = time()
					fxSendMotorCommand(devId1, FxCurrent, sample)
					dev1WriteTimeAfter = time()
					measurements1.append(data1.mot_cur)

			elif(controllerType == hssPosition):
				dev0WriteTimeBefore = time()
				fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
				dev0WriteTimeAfter = time()
				measurements0.append(data0.mot_ang - initialPos0)
				if(secondDevice):
					dev1WriteTimeBefore = time()
					fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
					dev1WriteTimeAfter = time()
					measurements1.append(data1.mot_ang - initialPos1)

			dev0ReadCommandTimes.append(dev0ReadTimeAfter - dev0ReadTimeBefore)
			dev0WriteCommandTimes.append(dev0WriteTimeAfter - dev0WriteTimeBefore)
			if secondDevice:
				dev1ReadCommandTimes.append(dev1ReadTimeAfter - dev1ReadTimeBefore)
				dev1WriteCommandTimes.append(dev1WriteTimeAfter - dev1WriteTimeBefore)
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

				if(controllerType == hssCurrent):
					measurements0.append(data0.mot_cur)
					if(secondDevice):
						measurements1.append(data1.mot_cur)

				elif(controllerType == hssPosition):
					measurements0.append(data0.mot_ang - initialPos0)
					if(secondDevice):
						measurements1.append(data1.mot_ang - initialPos1)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

		# We'll draw a line at the end of every period
		cycleStopTimes.append(time() - t0)
	# Disable the controller, send 0 PWM
	fxSendMotorCommand(devId0, FxNone, 0)
	fxSendMotorCommand(devId1, FxNone, 0)
	sleep(0.1)

	# End of Main Code - Start of plotting code

	elapsedTime = time() - t0
	actualPeriod = cycleStopTimes[0]
	actualFrequency = 1 / actualPeriod
	commandFrequency = i / elapsedTime

	# Figure: setpoint, desired vs measured (1st device)
	figureCounter = 1	# First time, functions will increment
	figureCounter = plotSetpointVsDesired(devId0, figureCounter, controllerType, actualFrequency, signalAmplitude, signalTypeStr, commandFrequency, times,
						requests, measurements0, cycleStopTimes)
	figureCounter = plotExpStats(devId0, figureCounter, dev0WriteCommandTimes, dev0ReadCommandTimes)

	# Figure: setpoint, desired vs measured (2nd device)
	if(secondDevice):
		figureCounter = plotSetpointVsDesired(devId1, figureCounter, controllerType, actualFrequency, signalAmplitude, signalTypeStr, commandFrequency,
						times, requests, measurements1, cycleStopTimes)
		figureCounter = plotExpStats(devId1, figureCounter, dev1WriteCommandTimes, dev1ReadCommandTimes)

	printPlotExit()
	plt.show()
	fxCloseAll()

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxHighSpeedTest(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
