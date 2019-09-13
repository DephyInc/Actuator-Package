import os, sys, math
from time import sleep, time, strftime
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(pardir)
sys.path.append(pardir)
from fxUtil import *
from .streamManager import Stream

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

class Controller(Enum):
	position = 1
	current = 2

class FuncType(Enum):
	sine = 1
	line = 2

################## Tune the experimental parameters here #########################

# Adjust this to change the desired motor command frequency in Hz
# Actual motor command frequency will be slower because of running on an OS
# This can be over 1000Hz but after 2000Hz it will be capped by a constant in fx_plan_stack

COMMAND_FREQUENCY = 1000

# amplitude of signal
AMPLITUDE = 3500

# frequency of sine wave in Hz
FREQUENCY = 2.5 

# number of times to run the signal
NUMBER_OF_LOOPS = 10

# delay between signal cycles (s)
CYCLE_DELAY = 0

CONTROLLER_TYPE = Controller.position
SIGNAL_TYPE = FuncType.sine

REQUEST_JITTER = False
JITTER = 200


# generate a sine wave of a specific amplitude and frequency
def sinGenerator(amplitude, frequency):
	num_samples = COMMAND_FREQUENCY / frequency
	in_array = np.linspace(-np.pi, np.pi, num_samples)
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals

# generate a line with specific amplitude
def lineGenerator(amplitude):
	num_samples = COMMAND_FREQUENCY
	line_vals = [ amplitude for i in range(num_samples) ]
	return line_vals


def fxHighSpeedTest(port, baudRate):
	
	streamFreq = 1000
	shouldLog = True
	shouldAutostream = 1 # This makes the loop run slightly faster

	delay_time = float(1/(float(COMMAND_FREQUENCY)))
	print(delay_time)

	try:
		# Must be called before reading any device data
		stream = Stream(port, baudRate, varsToStream, 2, labels, streamFreq, shouldLog, shouldAutostream)
		sleep(0.4)

		############# Main Code ############
		######## Make your changes here #########

		# generate a control profile
		if (SIGNAL_TYPE == FuncType.sine):
			samples = sinGenerator(AMPLITUDE, FREQUENCY)
			signalTypeStr = "sine wave"
		elif (SIGNAL_TYPE == FuncType.line):
			samples = lineGenerator(AMPLITUDE)
			signalTypeStr = "line"
		else:
			assert 0		
		print(samples)

		# initialize lists
		requests = []
		measurements = []
		times = []

		cycleStopTimes = []
		i = 0
		t0 = 0

		if (CONTROLLER_TYPE == Controller.current):
			setControlMode(stream.devId, CTRL_CURRENT)
			print("Setting up current control demo")
		elif (CONTROLLER_TYPE == Controller.position):
			setControlMode(stream.devId, CTRL_POSITION)
			print("Setting up position control demo")
			initial_pos = stream([FX_ENC_ANG])

		else:
			assert 0	
					
		setGains(stream.devId, 300, 50, 0, 0)
		
		# record start time of experiment
		t0 = time()
		for reps in range(0, NUMBER_OF_LOOPS):
			for sample in samples:
				if (i % 2 == 0 and REQUEST_JITTER):
					sample = sample + JITTER

				sleep(delay_time)

				# set controller to the next sample
				# read ActPack data
				if (CONTROLLER_TYPE == Controller.current):
					setMotorCurrent(stream.devId, sample)
					data = stream([FX_MOT_CURR])

				elif (CONTROLLER_TYPE == Controller.position):
					setPosition(stream.devId, sample) 
					data = stream([FX_ENC_ANG])

				measurements.append(data)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

			# Delay between cycles
			for j in range(int(CYCLE_DELAY/delay_time)):

				sleep(delay_time)
				# read data from ActPack
				if (CONTROLLER_TYPE == Controller.current):
					data = stream([FX_MOT_CURR])

				elif (CONTROLLER_TYPE == Controller.position):
					data = stream([FX_ENC_ANG])

				measurements.append(data)

				times.append(time() - t0)
				requests.append(sample)
				i = i + 1

			# we'll draw a line at the end of every period
			cycleStopTimes.append(time() - t0)
		elapsed_time = time() - t0

		######## End of Main Code #########
		######## Do not delete the cleanup functions below #########

		setControlMode(stream.devId, CTRL_NONE)
	
		del stream

		######## Plotting Code, you can edit this ##################

		actual_period = cycleStopTimes[0]
		actual_frequency = 1 / actual_period
		command_frequency = i / elapsed_time
		print("i: " + str(i) + ", elapsed_time: " + str(elapsed_time))

		if (CONTROLLER_TYPE == Controller.current):
			title = "Current control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(AMPLITUDE) + " mA amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			plt.plot(times, requests, color = 'b', label = 'desired current')
			plt.plot(times, measurements, color = 'r', label = 'measured current')
			plt.xlabel("time (s)")
			plt.ylabel("motor current (mA)")

		elif (CONTROLLER_TYPE == Controller.position):
			title = "Position control with " + "{:.2f}".format(actual_frequency) + " Hz, " + \
				str(AMPLITUDE) + " amplitude " + signalTypeStr + " and " + "{:.2f}".format(command_frequency) + " Hz commands"
			plt.plot(times, requests, color = 'b', label = 'desired position')
			plt.plot(times, measurements, color = 'r', label = 'measured position')
			plt.xlabel("time (s)")
			plt.ylabel("Encoder position")

		plt.title(title)

		plt.legend(loc='upper right')

		# draw a vertical line at the end of each cycle
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