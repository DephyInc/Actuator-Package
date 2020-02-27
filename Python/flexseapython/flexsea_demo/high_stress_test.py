import os
import sys
import math
from time import sleep, time
from datetime import datetime	# Create unique log filename
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
#Next two lines are used to plot in a browser:
import matplotlib
matplotlib.use('WebAgg')
from scipy import stats

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(pardir)
sys.path.append(pardir)
from fxUtil import *

######## These arrays are updated concurrently with every new timestamp ############
times                = []
currentRequests      = []
currentMeasurements0 = []	# For devId0
currentMeasurements1 = []	# For devId1
positionRequests     = []
positionMeasurements0= []	# For devId0
positionMeasurements1= []	# For devId1
readDeviceTimes      = []	# Timing data for fxReadDevice()
sendMotorTimes       = []	# Timing data for fxSendMotorCommand
setGainsTimes        = []	# Timing data for fxSetGains()
#####################################################################
cycleStopTimes = []		# Use to draw a line at end of every period
data0=0				# Contains state of ActPack0 
data1=0				# Contains state of ActPack1


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
	in_array = np.linspace(-np.pi, np.pi, num_samples)
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals

# Generate a line with specific amplitude
def lineGenerator(amplitude, length, commandFreq):
	num_samples = np.int32(length * commandFreq)
	line_vals = [ amplitude for i in range(num_samples) ]
	return line_vals

# Interpolates between two positions (A to B)
def linearInterp(a, b, points):
	lin_array = np.linspace(a, b, points)
	#print("Lin interp from",a,"to",b)
	return lin_array

"""
# Set the device(s) for position control
def setPositionCtrl(t0, devId0, devId1, secondDevice, position0, position1):
	global times
	global currentRequests
	global positionRequests
	global readDeviceTimes = []    # Timing data for fxReadDevice()
	global sendMotorTimes  = []    # Timing data for fxSendMotorCommand
	global setGainsTimes   = []    # Timing data for fxSetGains()

	tSetGainsTimes_beg = time()
	fxSetGains(devId0, 300, 50, 0, 0, 0)
	tSetGainsTimes_end = time()
	setGainsTimes.append(tSetGainsTimes_end - tSetGainsTimes_beg)

	tSendMotorTimes_beg = time()
	fxSendMotorCommand(devId0, FxPosition, position0)
	tSendMotorTimes_end = time()
	sendMotorTimes.append(tSendMotorTimes_end - tSendMotorTimes_beg)

	if (secondDevice):
		fxSetGains(devId1, 300, 50, 0, 0, 0)
		fxSendMotorCommand(devId1, FxPosition, position1)
	

	currentRequests.append(0)
	positionRequests.append(position0)
		

	currentMeasurements.append(data.motorCurrent)
	positionMeasurements.append(data.encoderAngle)

	times.append(time() - t0)
	
# Set the device(s) for current control
def setCurrentCtrl(t0, devId0, devId1, secondDevice, current0, current1):
	global times
	global currentRequests
	global positionRequests
	global readDeviceTimes = []    # Timing data for fxReadDevice()
	global sendMotorTimes  = []    # Timing data for fxSendMotorCommand
	global setGainsTimes   = []    # Timing data for fxSetGains()

	tstart = time()
	fxSetGains(devId0, 300, 50, 0, 0, 0)
	tstop  = time()
	setGainsTimes.append(tstop  - tstart)

	tSendMotorTimes_beg = time()
	fxSendMotorCommand(devId0, FxCurrent, current0)
	tSendMotorTimes_end = time()
	sendMotorTimes.append(tSendMotorTimes_end - tSendMotorTimes_beg)

	if (secondDevice):
		fxSetGains(devId1, 300, 50, 0, 0, 0)
		fxSendMotorCommand(devId1, FxCurrent, current1)

	times.append(time() - t0)
	currentRequests.append(current0)
	positionRequests.append(0)
"""

# Send fx commands and record their execution time.
# t0:	Timestamp for start of run. (Current time-t0) = Elapsed time
# initialPos0, initialPos1: Initial encoder angles for devId0, devId1. Used to provide offests
#	to encoder angle readings.
# current0, current1:	Desired currents  for devId0 and devId1
# position0, position1:	Desired positions for devId0 and devId1
# motorCmd:	An enum defined in flexseapython.py.
#	Allowed values:	FxPosition, FxVoltage, FxCurrent, FxImpedance
def sendAndTimeCmds(t0, devId0, devId1, device2: bool, initialPos0, initialPos1,
		current0, current1, motorCmd, position0, position1, posReq, setGains: bool):
	global times			# Elapsed time from start of run
	global currentRequests
	global currentMeasurements0	# For devId0
	global currentMeasurements1	# For devId1
	global positionRequests
	global positionMeasurements0	# For devId0
	global positionMeasurements1	# For devId1
	global readDeviceTimes		# Timing data for fxReadDevice()
	global sendMotorTimes		# Timing data for fxSendMotorCommand
	global setGainsTimes		# Timing data for fxSetGains()
	global data0			# Contains state of ActPack0 
	global data1 			# Contains state of ActPack1

	tstart = time()
	data0  = fxReadDevice(devId0)	# Get ActPackState
	readDeviceTimes.append(time() - tstart)
	if (device2):
		data1 = fxReadDevice(devId1)

	if setGains:
		tstart = time()
		for i in range(2):
			fxSetGains(devId0, 300, 50, 0, 0, 0)
		setGainsTimes.append(time() - tstart)
		if (device2):
			fxSetGains(devId1, 300, 50, 0, 0, 0)
	else:
		setGainsTimes.append(0)

	if motorCmd == FxCurrent:	# Set device(s) for current control
		tstart = time()
		fxSendMotorCommand(devId0, FxCurrent, current0)
		sendMotorTimes.append(time() - tstart)
		if (device2):
			fxSendMotorCommand(devId1, FxCurrent, current1)
			positionMeasurements1.append(data1.encoderAngle - initialPos1)
		positionMeasurements0.append(data0.encoderAngle)

	elif motorCmd == FxPosition:	# Set device(s) for position control
		tstart = time()
		fxSendMotorCommand(devId0, FxPosition, position0)
		sendMotorTimes.append(time() - tstart)
		if (device2):
			fxSendMotorCommand(devId1, FxPosition, position1)
			positionMeasurements1.append(data1.encoderAngle - initialPos1)
		positionMeasurements0.append(data0.encoderAngle - initialPos0)
	else:	# Defensive code.  It should not execute!
		assert 0, 'Unexpected motor command in record_timing()'

	currentRequests.append(current0)
	currentMeasurements0.append(data0.motorCurrent)
	if (device2):
		currentMeasurements1.append(data1.motorCurrent)
	positionRequests.append(position0)
	times.append(time() - t0)


# Port: port with outgoing serial connection to ActPack
# Baud Rate : baud rate of outgoing serial connection to ActPack
# Command Freq: Desired frequency of issuing commands to controller, actual 
#	command frequency will be slower due to OS overhead.
# positionAmplitude: amplitude (in ticks), position controller
# currentAmplitude: amplitude (in mA), current controller
# positionFreq: frequency (Hz) of the sine wave, position controller
# currentFreq: frequency (Hz) of the sine wave, current controller
# currentAsymmetricG: we use more current on the "way back" to come back closer to the staring
# point. Positive numbers only, 1-3 range.
# Number of Loops: Number of times to send desired signal to controller
def fxHighStressTest(port0, baudRate, port1 = "", commandFreq = 1000,
		positionAmplitude = 10000, currentAmplitude = 2500,
		positionFreq = 1, currentFreq = 5, currentAsymmetricG = 1.25,
		numberOfLoops = 720):
	global times		# Elapsed time since strart of run
	global currentRequests
	global positionRequests
	global readDeviceTimes	# Timing data for fxReadDevice()
	global sendMotorTimes	# Timing data for fxSendMotorCommand
	global setGainsTimes	# Timing data for fxSetGains()
	global cycleStopTimes
	global data0		# Contains state of ActPack0 
	global data1 		# Contains state of ActPack1

	########### One vs two devices ############
	secondDevice = False
	if (port1 != ""):
		secondDevice = True

	if (secondDevice):
		print("Running high stress test with two devices")
	else:
		print("Running high stress test with one device")

	########### Debug & Data Logging ############
	debugLoggingLevel = 6 # 6 is least verbose, 0 is most verbose
	dataLog = False # Data log logs device data

	delay_time = float(1/(float(commandFreq)))
	print('Delay time: ', delay_time)

	########### Open the device(s) and start streaming ############
	devId0 = fxOpen(port0, baudRate, debugLoggingLevel) 
	fxStartStreaming(devId0, commandFreq, dataLog)
	print('Connected to device with Id:', devId0)

	devId1 = -1
	if (secondDevice):
		print('Port: ', port1)
		print('BaudRate: ', baudRate)
		print('debugLoggingLevel: ', debugLoggingLevel)
		devId1 = fxOpen(port1, baudRate, debugLoggingLevel)
		fxStartStreaming(devId1, commandFreq, dataLog)
		print('Connected to device with Id:', devId1)

	############# Main Code ############
	######## Make your changes here #########

	# Get initial position:
	print('Reading initial position...')

	# Give the device time to consume the startStreaming command and start streaming
	sleep(0.1)

	data0 = fxReadDevice(devId0)
	initialPos0 = data0.encoderAngle	# May be used to offset subsequent readings
	print("Initial position 0:", initialPos0)

	initialPos1 = 0
	if (secondDevice):
		data1 = fxReadDevice(devId1)
		initialPos1 = data1.encoderAngle
		print("Initial position 1:", initialPos1)

	# Generate control profiles
	print('Command table #1 - Position Sine:')
	positionSamples = sinGenerator(positionAmplitude, positionFreq, commandFreq)
	print(np.int64(positionSamples))
	print('Command table #2 - Current Sine:')
	currentSamples = sinGenerator(currentAmplitude, currentFreq, commandFreq)
	print("number of samples is: ", len(currentSamples))
	print(np.int64(currentSamples))
	print('Command table #3 - Current Sine:')
	currentSamplesLine = lineGenerator(0, 0.15, commandFreq)
	#print(np.int64(currentSamplesLine))

	# Initialize lists
	# cycleStopTimes = []

	try:
		t0 = time()	# Record start time of experiment
		i = 0
		for reps in range(0, numberOfLoops):

			print("")
			print("Rep #", reps+1,"out of",numberOfLoops)
			print("-------------------")

			# Step 0: set position controller
			# -------------------------------
			print("Step 0: set position controller")

			sleep(delay_time)	# Important in loop 2+
			if (i):	# Second or later iterations in loop
				# setPositionCtrl(  devId0, devId1, secondDevice, data0.encoderAngle, initialPos1)
				sendAndTimeCmds(t0, devId0, devId1, secondDevice, initialPos0, initialPos1,
					current0=0, current1=0, motorCmd=FxPosition,
					position0=data0.encoderAngle, position1=initialPos1,
					posReq=0, setGains=True)
				# ToDo: data1.encoderAngle
			else:	# First loop iteration
				# setPositionCtrl(  devId0, devId1, secondDevice, initialPos0, initialPos1)
				sendAndTimeCmds(t0, devId0, devId1, secondDevice, initialPos0=0, initialPos1=0,
					current0=0, current1=0, motorCmd=FxPosition,
					position0=initialPos0, position1=initialPos1, posReq=0, setGains=True)

			# Step 1: go to initial position
			# -------------------------------
			if (i):	# Second or later iterations in loop
				print("Step 1: go to initial position")
				linSamples = linearInterp(data0.encoderAngle-initialPos0, 0, 100)
				#print(np.int64(linSamples))

				for sample in linSamples:

					sleep(delay_time)
					sendAndTimeCmds(t0, devId0, devId1, secondDevice, initialPos0, initialPos1,
						current0=0, current1=0, motorCmd=FxPosition,
						position0=sample+initialPos0, position1=sample+initialPos1,
						posReq=sample, setGains=False)
					"""
					# set controller to the next sample
					# read ActPack data
					tstart = time()
					data0  = fxReadDevice(devId0)
					tstop  = time()
					readDeviceTimes.append(tstop - tstart)
					if (secondDevice):
						data1 = fxReadDevice(devId1)

					# Position setpoint:
					tstart = time()
					fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
					tstop = time()
					sendMotorTimes.append(tstop - tstart)

					currentMeasurements0.append(data0.motorCurrent)
					positionMeasurements0.append(data0.encoderAngle - initialPos0)
					if (secondDevice):
						fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
						currentMeasurements1.append(data1.motorCurrent)
						positionMeasurements1.append(data1.encoderAngle-initialPos1)

					times.append(time() - t0)
					currentRequests.append(0)
					positionRequests.append(sample)	# BAB: sample+initialPos0 ???
					"""
					i = i + 1
			else:	# First time in loop
				print("Step 1: skipped, first round")

			# Step 2: position sine wave
			# --------------------------
			print("Step 2: track position sine wave")

			for sample in positionSamples:

				sleep(delay_time)
				sendAndTimeCmds(t0, devId0, devId1, secondDevice,initialPos0, initialPos1,
					current0=0, current1=0, motorCmd=FxPosition,
					position0=sample+initialPos0, position1=sample+initialPos1,
					posReq=0, setGains=False)

				"""
				# set controller to the next sample
				# read ActPack data
				tstart = time()
				data0 = fxReadDevice(devId0)
				tstop = time()
				readDeviceTimes.append(tstop - tstart)
				if (secondDevice):
					data1 = fxReadDevice(devId1)

				# Position setpoint:
				tstart = time()
				fxSendMotorCommand(devId0, FxPosition, sample + initialPos0)
				tstop = time()
				sendMotorTimes.append(tstop - tstart)

				currentMeasurements0.append(data0.motorCurrent)
				positionMeasurements0.append(data0.encoderAngle - initialPos0)
				if (secondDevice):
					fxSendMotorCommand(devId1, FxPosition, sample + initialPos1)
					currentMeasurements1.append(data1.motorCurrent)
					positionMeasurements1.append(data1.encoderAngle - initialPos1)

				times.append(time() - t0)
				currentRequests.append(0)
				positionRequests.append(sample)	# BAB: sample+initialPos0 ???
				"""
				i = i + 1

			# Step 3: set current controller
			# -------------------------------
			print("Step 3: set current controller")
			# setCurrentCtrl(   devId0, devId1, secondDevice, 0, 0)
			sendAndTimeCmds(t0, devId0, devId1, secondDevice, initialPos0, initialPos1,
				current0=0, current1=0, motorCmd=FxCurrent,
				position0=0, position1=0, posReq=0, setGains=True)


			# Step 4: current setpoint
			# --------------------------
			print("Step 4: track current sine wave")
			for sample in currentSamples:

				sleep(delay_time)
				# We use more current on the "way back" to come back closer to
				# the staring point
				if(sample <= 0):	#No change
					compensatedSample = sample
				else:			#Apply gain
					compensatedSample = np.int64(currentAsymmetricG * sample)

				sendAndTimeCmds(t0, devId0, devId1, secondDevice,initialPos0, initialPos1,
					current0=compensatedSample, current1=compensatedSample,
					motorCmd=FxCurrent, position0=0, position1=0, posReq=0, setGains=False)

				# set controller to the next sample
				# read ActPack data
				"""
				tstart = time()
				data0 = fxReadDevice(devId0)
				tstop = time()
				readDeviceTimes.append(tstop - tstart)
				if (secondDevice):
					data1 = fxReadDevice(devId1)

				# Position setpoint:
				tstart = time()
				fxSendMotorCommand(devId0, FxCurrent, compensatedSample)
				tstop = time()
				sendMotorTimes.append(tstop - tstart)

				currentMeasurements0.append(data0.motorCurrent)
				positionMeasurements0.append(data0.encoderAngle - initialPos0)
				if (secondDevice):
					fxSendMotorCommand(devId1, FxCurrent, compensatedSample)
					currentMeasurements1.append(data1.motorCurrent)
					positionMeasurements1.append(data1.encoderAngle - initialPos1)

				times.append(time() - t0)
				currentRequests.append(compensatedSample)
				positionRequests.append(0)
				"""
				i = i + 1
				
			# Step 5: short pause at 0 current to allow a slow-down
			# -----------------------------------------------------
			print("Step 5: motor slow-down, zero current")

			for sample in currentSamplesLine:

				sleep(delay_time)
				sendAndTimeCmds(t0, devId0, devId1, secondDevice,initialPos0, initialPos1,
				 	current0=sample, current1=sample, motorCmd=FxCurrent,
				 	position0=0, position1=0, posReq=0, setGains=False)

				"""
				# set controller to the next sample
				# read ActPack data
				tstart = time()
				data0 = fxReadDevice(devId0)
				tstop = time()
				readDeviceTimes.append(tstop - tstart)
				if (secondDevice):
					data1 = fxReadDevice(devId1)

				# Position setpoint:
				tstart = time()
				fxSendMotorCommand(devId0, FxCurrent, sample)
				tstop = time()
				sendMotorTimes.append(tstop - tstart)

				currentMeasurements0.append(data0.motorCurrent)
				positionMeasurements0.append(data0.encoderAngle - initialPos0)
				if (secondDevice):
					fxSendMotorCommand(devId1, FxCurrent, sample)
					currentMeasurements1.append(data1.motorCurrent)
					positionMeasurements1.append(data1.encoderAngle - initialPos1)

				times.append(time() - t0)
				currentRequests.append(sample)
				positionRequests.append(0)
				"""
				i = i + 1

			# We'll draw a line at the end of every period
			cycleStopTimes.append(time() - t0)
			elapsed_time = time() - t0
	except KeyboardInterrupt:
		print ('Keypress detected.  Exiting gracefully ...')

	fxClose(devId0)
	fxClose(devId1)

	######## Stats: #########
	print("")
	print("Final Stats:")
	print("------------")
	actual_period = cycleStopTimes[0]
	command_frequency = i / elapsed_time
	print("Number of commands sent: " + str(i))
	print("Total time (s): " + str(elapsed_time))
	print("Requested command frequency: "+"{:.2f}".format(commandFreq))
	print("Actual command frequency (Hz): "+"{:.2f}".format(command_frequency))
	print("")
	print('currentSamplesLine: ',		len(currentSamplesLine))
	print('size(times)',			len(times))
	print('size(currentRequests): ',	len(currentRequests))
	print('size(currentMeasurements0): ',	len(currentMeasurements0))
	print('size(setGainsTimes): ',		len(setGainsTimes))
	print('')

        ######## Summary stats about intividual arrays: #########
	print('\n\ntimes: ',			stats.describe(times))
	print('\n\ncurrentRequests: ',		stats.describe(currentRequests))
	print('\n\ncurrentMeasurements0: ',	stats.describe(currentMeasurements0))
	# print('\n\ncurrentMeasurements1: ',	stats.describe(currentMeasurements1))
	print('\n\npositionRequests: ',		stats.describe(positionRequests))
	print('\n\npositionMeasurements0: ',	stats.describe(positionMeasurements0))
	# print('\n\npositionMeasurements1: ',	stats.describe(positionMeasurements1))
	print('\n\nreadDeviceTimes: ',		stats.describe(readDeviceTimes))
	print('\n\nsendMotorTimes: ',		stats.describe(sendMotorTimes))
	print('\n\nseetGainsTimes: ',		stats.describe(setGainsTimes))


	######## End of Main Code #########

	######## Plotting Code, you can edit this ##################

	###### Begin Create unique data filename and save desired and measured values
	now = datetime.now().strftime("%Y-%m-%d_%H-%M")
	data_fn = 'log/' + now + '_Current.csv'
	print('Do create Current  data file ['+ data_fn + ']')
	# NON-PYTHONIC, but efficient write to file:
	# with open(data_fn, 'w') as df:
	# 	for i in range(len(currentRequests)):
	# 		df.write(str(times[i]) + ',' + str(currentRequests[i]) + ','
	# 			+ str(currentMeasurements0[i]) + '\n')

	data_fn = 'log/' + now + '_Position.csv'
	print('Do create Position data file ['+ data_fn + ']')
	# with open(data_fn, 'w') as df:
	# 	for i in range(len(positionRequests)):
	# 		df.write(str(times[i]) + ',' + str(positionRequests[i]) + ','
	# 			+ str(positionMeasurements0[i]) + '\n')
	###### End Create unique data filename and save desired and measured values

	# Current Plot:
	plt.figure(1)
	title = "Motor Current"
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
	title = "Motor Position"
	plt.plot(times, positionRequests, color = 'b', label = 'desired position')
	plt.plot(times, positionMeasurements0, color = 'r', label = 'measured position')
	plt.xlabel("Time (s)")
	plt.ylabel("Encoder position")
	plt.title(title)
	plt.legend(loc='upper right')

	# Draw a vertical line at the end of each cycle
	for endpoints in cycleStopTimes:
		plt.axvline(x=endpoints)

	plt.figure(3)
	# Convert command times into millisec
	sendMotorTimes = [i * 1000 for i in sendMotorTimes]
	plt.plot(times, sendMotorTimes, color='b', label='Send Motor Times')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")
	plt.title("Send Motor Times")
	plt.legend(loc='upper right')

	plt.figure(4)
	plt.yscale('log')
	plt.hist(sendMotorTimes, bins=100, label = 'Send Motor Times')
	plt.yscale('log')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")
	plt.title("Send Motor Commands")
	plt.legend(loc='upper right')

	plt.figure(5)
	# Convert command times into millisec
	readDeviceTimes = [i * 1000 for i in readDeviceTimes]
	plt.plot(times, readDeviceTimes, color='b', label='Read Device Times')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")
	plt.title("Read Device Commands")
	plt.legend(loc='upper right')

	plt.figure(6)
	plt.yscale('log')
	plt.hist(readDeviceTimes, bins=100, label = 'Read Device Times')
	plt.yscale('log')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")
	plt.title("Read Device Commands")
	plt.legend(loc='upper right')

	plt.figure(7)
	# Convert command times into millisec
	setGainsTimes = [i * 1000 for i in setGainsTimes]
	plt.plot(times, setGainsTimes, color='b', label='Set Gains Times')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")
	plt.title("Set Gains Commands")
	plt.legend(loc='upper right')

	plt.figure(8)
	plt.yscale('log')
	# Remove 0 values in histogram
	setGainsTimes = [i for i in setGainsTimes if i > 0]
	plt.hist(setGainsTimes, bins=100, label = 'Set Gains Times')
	plt.yscale('log')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")
	plt.title("Set Gains Commands")
	plt.legend(loc='upper right')


	# #######
	# *** ToDo: add plotting for 2nd device here ***
	# #######
	
	plt.show()

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxHighStressTest(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))

