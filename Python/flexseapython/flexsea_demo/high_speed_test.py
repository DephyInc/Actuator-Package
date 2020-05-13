from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import os
import sys
from time import sleep, time
from typing import Final, List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# matplotlib.use('WebAgg')

# from fxUtil import *
from flexseapython.pyFlexsea import fxReadDevice, ActPackState, fxOpen, fxStartStreaming, \
	fxSetGains, fxSendMotorCommand, FxCurrent, FxPosition, fxCloseAll, FxVoltage


# pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(pardir)
# sys.path.append(pardir)

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
	num_samples = int(round(commandFreq / frequency, 0))		# Default: 1000/5=200
	print("number of samples is: ", num_samples)
	in_array = np.linspace(-np.pi, np.pi, num_samples)
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals

# Generate a line with specific amplitude
def lineGenerator(amplitude, commandFreq):
	num_samples = commandFreq
	line_vals = [amplitude for i in range(num_samples)]
	return line_vals

# JFD: Dead code: fxHighSpeedTest2(): Remove eventually.
def fxHighSpeedTest2(port0, baudRate, port1="", controllerType=Controller.current,
					 signalType=signal.sine, commandFreq=1000, signalAmplitude=1000, numberOfLoops=30,
					 signalFreq=5, cycleDelay=0.1, requestJitter=False, jitter=20):
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
		print("Running high speed test with two devices")
	else:
		print("Running high speed test with one device")

	########### Debug & Data Logging ############
	debugLoggingLevel = 6	# 6 is least verbose, 0 is most verbose
	dataLog = False			# Data log logs device data

	delay_time = float(1 / (float(commandFreq)))
	print(delay_time)

	########### Open the device and start streaming ############
	devId0 = fxOpen(port0, baudRate, debugLoggingLevel)
	fxStartStreaming(devId0, commandFreq, dataLog)
	print('Connected to device with ID ', devId0)

	devId1 = -1
	if (secondDevice):
		devId1 = fxOpen(port1, baudRate, debugLoggingLevel)
		fxStartStreaming(devId1, commandFreq, dataLog)
		print('Connected to device with ID ', devId1)

	############# Main Code ############
	######## Make your changes here #########

	if (controllerType == Controller.position):
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

	# Prepare controller:
	if (controllerType == Controller.current):
		print("Setting up current control demo. Low current, high frequency: motor shouldn't move much if at all.")
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
	i = 0
	t0 = time()
	loopCtr = 0
	for reps in range(0, numberOfLoops):
		loopCtr += 1
		elapsed_time = time() - t0
		print('Loop:', loopCtr, 'of', numberOfLoops, '- Elapsed time:', int(elapsed_time + 0.5), 's', end='\r')
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
			for j in range(int(cycleDelay / delay_time)):

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
	# fxCloseAll()	#STACK-169

	# Disable the controller, send 0 PWM
	fxSendMotorCommand(devId0, FxVoltage, 0)
	fxSendMotorCommand(devId1, FxVoltage, 0)
	sleep(0.1)

	######## End of Main Code #########

	######## Plotting Code, you can edit this ##################

	try:  # Try to specify "WebAgg" as the backend for rendering and GUI integration.
		matplotlib.use('WebAgg')
	except ImportError:
		sys.exit('high_speed_test.py: use("WebAgg") unsuccessful:' + ImportError)

	elapsed_time = time() - t0
	print('Loop:', loopCtr, 'of', numberOfLoops, '- Elapsed time:', int(elapsed_time + 0.5), 's')
	actual_period = cycleStopTimes[0]
	actual_frequency = 1 / actual_period
	command_frequency = i / elapsed_time

	if (controllerType == Controller.current):
		plt.figure(1)
		title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(signalAmplitude) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(
			command_frequency) + " Hz commands"
		plt.plot(times, requests, color='b', label='desired current')
		plt.plot(times, measurements0, color='r', label='measured current')
		plt.xlabel("Time (s)")
		plt.ylabel("Motor current (mA)")
		plt.title(title)

		plt.legend(loc='upper right')

	# Draw a vertical line at the end of each cycle
	# for endpoints in cycleStopTimes:
	# 	plt.axvline(x=endpoints)

	elif (controllerType == Controller.position):
		plt.figure(1)
		title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(
			command_frequency) + " Hz commands"
		plt.plot(times, requests, color='b', label='desired position')
		plt.plot(times, measurements0, color='r', label='measured position')
		plt.xlabel("Time (s)")
		plt.ylabel("Encoder position")
		plt.title(title)

		plt.legend(loc='upper right')

		# Draw a vertical line at the end of each cycle
		for endpoints in cycleStopTimes:
			plt.axvline(x=endpoints)

	###### begin command times plotting ########################################33

	# Following 6 lines are legacy code. Remove eventually.
	# plt.figure(2)
	# title = "Current and stream command times (aggregate)"
	# plt.title(title)
	# plt.plot(currentCommandTimes,color='b', label='Current Command Times')
	# plt.plot(streamCommandTimes, color='r', label='Stream Command Times')
	# plt.legend(loc='upper right')

	plt.figure(2)
	# Convert command times into millisec
	currentCommandTimes = [i * 1000 for i in currentCommandTimes]
	# np.savetxt('JFD.txt', np.array(currentCommandTimes), fmt='%.10f')
	plt.plot(currentCommandTimes, color='b', label='Current Command Times')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	plt.figure(3)
	plt.yscale('log')
	plt.hist(currentCommandTimes, bins=100, label='Current Commands')
	plt.yscale('log')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	plt.figure(4)
	streamCommandTimes = [i * 1000 for i in streamCommandTimes]
	# Convert command times into milliseconds
	plt.plot(streamCommandTimes, color='b', label='Stream Command Times')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	plt.figure(5)
	plt.yscale('log')
	plt.hist(streamCommandTimes, bins=100, label='Stream Commands')
	plt.yscale('log')
	plt.title("Commands")
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	##### End command times plotting ########################################33

	if (secondDevice):
		if (controllerType == Controller.current):
			plt.figure(2)
			title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
					str(signalAmplitude) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(
				command_frequency) + " Hz commands"
			plt.plot(times, requests, color='b', label='desired current')
			plt.plot(times, measurements1, color='r', label='measured current')
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
					str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(
				command_frequency) + " Hz commands"
			plt.plot(times, requests, color='b', label='desired position')
			plt.plot(times, measurements1, color='r', label='measured position')
			plt.xlabel("Time (s)")
			plt.ylabel("Encoder position")
			plt.title(title)

			plt.legend(loc='upper right')

			# Draw a vertical line at the end of each cycle
			for endpoints in cycleStopTimes:
				plt.axvline(x=endpoints)

	if os.name == 'nt':
		print('\nIn Windows, press Ctrl-BREAK to exit.  Ctrl-C may not work.')
	plt.show()

	fxCloseAll()

####################################################################################################
##### New Implementation #####
####################################################################################################

@dataclass
class Device:
	""" Holds device state/measurements in one place """
	port: str = ''
	baudRate: int = 0
	controllerType: Controller = Controller.position
	signalType: signal = signal.sine
	commandFreq: int = 0
	signalAmplitude: int = 0
	numberOfLoops: int = 0
	signalFreq: int = 0
	cycleDelay: float = 0.0
	requestJitter: bool = False
	jitter: int = 0
	devId: int = 0
	initialPos: int = 0
	data: ActPackState = None
	measurements: List[float] = field(default_factory=list)

# Plot device data
def plot_device_data(devices: List[Device], t0: float, loopCtr: int, numberOfLoops: int,
		cmd_total: int, controllerType: Controller, signalAmplitude: int, signal_desc: str,
		currentCommandTimes: List[float], cycleStopTimes: List[float],
		requests: List[float], streamCommandTimes: List[float], times: List[float]) -> int:
	""" Plotting Code, you can edit this """

	# Specify "WebAgg" as the backend for rendering and GUI integration.
	# On show(), it will start a tornado server with an interactive figure.
	matplotlib.use('WebAgg')

	elapsed_time = time() - t0
	print('Loop:', loopCtr, 'of', numberOfLoops, '- Elapsed time:', round(elapsed_time, 1), 'sec.')
	actual_period = cycleStopTimes[0]
	actual_frequency = 1 / actual_period
	command_frequency = cmd_total / elapsed_time

	plt_ctr: int = 1
	for d in devices:
		plt.figure(plt_ctr)
		title: str = ''
		if controllerType == Controller.current:
			title = 'Curr ctrl: ' + str(round(actual_frequency, 2)) + ' Hz, Amp ' +\
					str(signalAmplitude) + ' mA,' + signal_desc + 'and' + \
					str(round(command_frequency, 1)) + 'Hz cmd'
			plt.plot(times, requests,       color='b', label='desired current')
			plt.plot(times, d.measurements, color='r', label='measured current')
			plt.ylabel("Motor current (mA)")
		else:
			title = 'Posn ctrl: ' + str(round(actual_frequency, 2)) + \
					'Hz, Ticks Amp' + str(signalAmplitude) + ' mA,' + signal_desc + 'and' + \
					str(round(command_frequency, 1)) + 'Hz cmd'
			plt.plot(times, requests,       color='b', label='desired position')
			plt.plot(times, d.measurements, color='r', label='measured position')
			plt.ylabel("Motor current (mA)")
			plt.ylabel("Encoder position")
		plt.xlabel("Time (s)")
		plt.title(title)
		# Draw a vertical line at the end of each cycle
		for endpoints in cycleStopTimes:
			plt.axvline(x=endpoints)
		plt_ctr += 1

	plt.figure(plt_ctr)
	plt.title("Current Command Times")
	# Convert command times from sec to millisec
	currentCommandTimes = [i * 1000 for i in currentCommandTimes]
	plt.plot(currentCommandTimes, color='b', label='Current Command Times')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	plt_ctr += 1
	plt.figure(plt_ctr)
	plt.title("Current Command Times Histogram")
	plt.hist(currentCommandTimes, bins=100,  label='Current Commands')
	plt.plot(currentCommandTimes, color='b', label='Current Command Times')
	plt.yscale('log')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	plt_ctr += 1
	plt.figure(plt_ctr)
	plt.title("Commands")
	streamCommandTimes = [i * 1000 for i in streamCommandTimes]		# Convert from sec to ms
	plt.plot(streamCommandTimes, color='b', label='Stream Command Times')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	plt_ctr += 1
	plt.figure(plt_ctr)
	plt.hist(streamCommandTimes, bins=100, label='Stream Commands')
	plt.yscale('log')
	plt.title("Commands")
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	if os.name == 'nt':
		print('\nIn Windows, press Ctrl-BREAK to exit.  Ctrl-C may not work.')
	plt.show()
	return 0

# port				Port with outgoing serial connection to ActPack
# baudRate			Baud rate of outgoing serial connection to ActPack
# controllerType	Position controller or current controller
# signalType		Sine wave or line
# commandFreq		Desired frequency of issuing commands to controller, actual
# 					command frequency will be slower due to OS overhead.
# signalAmplitude	Amplitude of signal to send to controller. Encoder position
# 					if position controller, current in mA if current controller
# numberOfLoops		Number of times to send desired signal to controller
# signalFreq		Frequency of sine wave if using sine wave signal
# cycleDelay		Delay between signals sent to controller, use with sine wave only
# requestJitter		Add jitter amount to every other sample sent to controller
# jitter			Amount of jitter
def fxHighSpeedTest(port0: str, baudRate: int, portList: List[str]=[],
		controllerType=Controller.current, signalType=signal.sine, commandFreq=1000,
		signalAmplitude=1000, numberOfLoops=15, signalFreq=5, cycleDelay=0.1, requestJitter=False,
		jitter=20) -> int:

	# *********** Initialize lists ***********
	currentCommandTimes: List[float] = []
	cycleStopTimes:		 List[float] = []		# Used to draw a line at the end of every period
	requests:			 List[float] = []
	streamCommandTimes:	 List[float] = []
	times:				 List[float] = []

	if not portList:		# Hack to handle only 1 connected device
		portList.append(port0)
	num_devices: int = len(portList)
	print('Running high speed test with', num_devices, 'device(s).')

	# Initialize one data class/connected device
	devices: List[Device] = []
	for i in range(num_devices):
		dev = Device(portList[i], baudRate, controllerType, signalType, commandFreq, signalAmplitude,
					numberOfLoops, signalFreq, cycleDelay, requestJitter, jitter)
		devices.append(dev)

	delay_time = 1 / commandFreq	# Default: 1 / 1000 == 0.001s == 1ms
	print('delay_time:', delay_time, 'sec')

	# *********** Open device(s) and start streaming  ***********
	debugLoggingLevel = 6			# 6 is least verbose, 0 is most verbose
	dataLog = False					# Turn-off device data logging to file
	for d in devices:
		d.devId = fxOpen(d.port, d.baudRate, debugLoggingLevel)
		fxStartStreaming(d.devId, d.commandFreq, dataLog)
		print('Connected to device with ID:', d.devId)

	# ********************************** Main Code **********************************

	# Give the device time to consume the startStreaming command and start streaming
	sleep(0.1)
	if controllerType == Controller.position:
		print('Reading initial position of connected devices ...')
		for d in devices:
			d.data = fxReadDevice(d.devId)
			d.initialPos = d.data.endocerAngle
	else:		# Default: controllerType==Controller.current
		pass	# No action required

	# Generate a control profile
	print('Command table:')
	signal_desc: str = ''
	if signalType == signal.sine:		# Default
		signal_desc = "sine"
		# Generate a sine wave with signalAmplitude: min==-1000, max==1000
		samples = sinGenerator(signalAmplitude, signalFreq, commandFreq)
	else:			# signalType == signal.line
		signal_desc = "line"
		samples = lineGenerator(signalAmplitude, commandFreq)
	print('Signal type:', signal_desc)
	print(np.int64(samples))

	if controllerType == Controller.current:
		print('Setting-up current control demo')
	else:
		print('Setting-up position control demo')
	# JFD: Prepare controller.  Use the exact same code for either control type
	for d in devices:
		fxSetGains(d.devId, 300, 50, 0, 0, 0)

	# *********** Main loop ***********
	t0: float = time()
	lag_time: Final = 0.1
	cmd_total: int = 0
	loopCtr: int = 0
	# JFD: Following loop takes about 5s/loop on Windows 10, about 2s on RPi4
	for _ in range(numberOfLoops):
		loopCtr += 1
		elapsed_time = round((time() - t0), 1)
		print('Loop', loopCtr, 'of', numberOfLoops, '/ Elapsed time', elapsed_time, 's',end='\r')
		for sample in samples:			# Default len(samples)==200
			if (cmd_total % 2 == 0) and requestJitter:
				sample += jitter
			sleep(delay_time)

			# set controller to the next sample
			# JFD: API also has function: fxReadDeviceAll(devId, dataQueueSize).  Function defined
			# TWICE, but code seems to be identical
			t1_start: float = time()
			for d in devices:			# read ActPack data
				d.data = fxReadDevice(d.devId)
			streamCommandTimes.append(time() - t1_start)

			if controllerType == Controller.current:	# Default
				t1_start = time()
				for d in devices:
					fxSendMotorCommand(d.devId, FxCurrent, sample)
					# sleep(lag_time)	# JFD: Experimental. Produces drastic change in device behavior
					d.measurements.append(d.data.motorCurrent)
				currentCommandTimes.append(time() - t1_start)
			else:						# controllerType == Controller.position
				for d in devices:
					fxSendMotorCommand(d.devId, FxPosition, sample + d.initialPos)
					d.measurements.append(d.data.encoderAngle - d.initialPos)
				currentCommandTimes.append(0.0)

			times.append(time() - t0)
			requests.append(sample)
			cmd_total += 1

		# JFD: Should this code be indented +1 so it executes once/sample instead of once/loop?
		# Currently, "sample" might be used before set.
		# Delay between cycles (sine wave only)
		if signalType == signal.sine:		# Default
			for _ in range(int(cycleDelay/delay_time)):		# Default: .1/.001 = 100
				sleep(delay_time)

				for d in devices:			# Read ActPack data
					d.data = fxReadDevice(d.devId)

				if controllerType == Controller.current:
					for d in devices:
						d.measurements.append(d.data.motorCurrent)
				else:						# controllerType == Controller.position
					for d in devices:
						d.measurements.append(d.data.encoderAngle - d.initialPos)
				times.append(time() - t0)
				requests.append(sample)		# JFD: Logical error: Use before set
				cmd_total += 1

		cycleStopTimes.append(time() - t0)	# To draw a line at the end of every period

	# fxCloseAll()							# STACK-169
	# Disable the controller, send 0 PWM
	for d in devices:
		fxSendMotorCommand(d.devId, FxVoltage, 0)
	sleep(0.1)
	plot_device_data(devices, t0, loopCtr, numberOfLoops, cmd_total, controllerType, signalAmplitude,
			signal_desc, currentCommandTimes, cycleStopTimes, requests, streamCommandTimes,times)
	fxCloseAll()
	return 0

if __name__ == '__main__':
	baud_rate = int(sys.argv[1])
	ports = sys.argv[2]
	try:
		fxHighSpeedTest(ports, baud_rate)
	except Exception as e:
		print("broke: " + str(e))
