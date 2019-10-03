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
from .streamManager import Stream

# Select which variables you want to read:

labels = ["State time", \
"Motor angle", "Motor current", \
"Battery voltage", "Battery current" \
]

varsToStream = [ \
	FX_STATETIME, \
	FX_ENC_ANG, \
	FX_MOT_CURR, \
	FX_BATT_VOLT, 
	FX_BATT_CURR \
]

# Controller type
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
#               command frequency will be slower due to OS overhead.
# Signal Amplitude: Amplitude of signal to send to controller. Encoder position
#                   if position controller, current in mA if current controller
# Number of Loops: Number of times to send desired signal to controller
# Signal Freq: Frequency of sine wave if using sine wave signal
# Cycle Delay: Delay between signals sent to controller, use with sine wave only
# Request Jitter: Add jitter amount to every other sample sent to controller
# Jitter: Amount of jitter
def fxHighSpeedTest(port, baudRate, controllerType = Controller.position, signalType = signal.sine, commandFreq = 1000, signalAmplitude = 10000, numberOfLoops = 10, signalFreq = 1, cycleDelay = .1, requestJitter = False, jitter = 200):
	
	streamFreq = 1000
	shouldLog = True
	shouldAutostream = 1 # ActPack will send data to the script automatically (more efficient)

	delay_time = float(1/(float(commandFreq)))
	print(delay_time)

	try:
		# Must be called before reading any device data
		stream = Stream(port, baudRate, varsToStream, 2, labels, streamFreq, shouldLog, shouldAutostream)
		sleep(0.4)

		############# Main Code ############
		######## Make your changes here #########

		# Generate a control profile
		if (signalType == signal.sine):
			samples = sinGenerator(signalAmplitude, signalFreq, commandFreq)
			signalTypeStr = "sine wave"
		elif (signalType == signal.line):
			samples = lineGenerator(signalAmplitude, commandFreq)
			signalTypeStr = "line"
		else:
			assert 0
		print(samples)

		# Initialize lists
		requests = []
		measurements = []
		times = []

		cycleStopTimes = []
		i = 0
		t0 = 0

		if (controllerType == Controller.current):
			setControlMode(stream.devId, CTRL_CURRENT)
			print("Setting up current control demo")
		elif (controllerType == Controller.position):
			setControlMode(stream.devId, CTRL_POSITION)
			print("Setting up position control demo")
			initial_pos = stream([FX_ENC_ANG])

		else:
			assert 0
					
		setGains(stream.devId, 300, 50, 0, 0)
		
		# Record start time of experiment
		t0 = time()
		for reps in range(0, numberOfLoops):
			for sample in samples:
				if (i % 2 == 0 and requestJitter):
					sample = sample + jitter

				sleep(delay_time)

				# set controller to the next sample
				# read ActPack data
				if (controllerType == Controller.current):
					setMotorCurrent(stream.devId, sample)
					data = stream([FX_MOT_CURR])

				elif (controllerType == Controller.position):
					setPosition(stream.devId, sample) 
					data = stream([FX_ENC_ANG])

				measurements.append(data)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

			# Delay between cycles (sine wave only)
			if (signalType == signal.sine):
				for j in range(int(cycleDelay/delay_time)):
	
					sleep(delay_time)
					# Read data from ActPack
					if (controllerType == Controller.current):
						data = stream([FX_MOT_CURR])
	
					elif (controllerType == Controller.position):
						data = stream([FX_ENC_ANG])
	
					measurements.append(data)
	
					times.append(time() - t0)
					requests.append(sample)
					i = i + 1

			# We'll draw a line at the end of every period
			cycleStopTimes.append(time() - t0)
		elapsed_time = time() - t0

		######## End of Main Code #########
		######## Do not delete the cleanup functions below! #########

		setControlMode(stream.devId, CTRL_NONE)
	
		del stream

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
			plt.xlabel("time (s)")
			plt.ylabel("motor current (mA)")

		elif (controllerType == Controller.position):
			title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(signalAmplitude) + " ticks amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			plt.plot(times, requests, color = 'b', label = 'desired position')
			plt.plot(times, measurements, color = 'r', label = 'measured position')
			plt.xlabel("time (s)")
			plt.ylabel("Encoder position")

		plt.title(title)

		plt.legend(loc='upper right')

		# Draw a vertical line at the end of each cycle
		for endpoints in cycleStopTimes:
			plt.axvline(x=endpoints)
		plt.show()


	except:
		# Run the cleanup no matter how you exit
		setControlMode(stream.devId, CTRL_NONE)
	
		del stream

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxHighSpeedTest(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))