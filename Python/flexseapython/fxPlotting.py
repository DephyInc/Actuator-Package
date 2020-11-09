from flexseapython.pyFlexsea import *
from flexseapython.fxUtil import isPi
import matplotlib
import matplotlib.pyplot as plt

# Figure: setpoint, desired vs measured
def plotSetpointVsDesired(devId, fig, controllerType, signalFrequency, signalAmplitude, signalTypeStr, commandFrequency, times, requests, measurements, cycleStopTimes):

	plt.figure(fig)
	fig += 1

	# Specific to the current controller:
	if(controllerType == hssCurrent):	#Controller.current):
		title = "Current control with {:.0f} Hz, {:.1f} mA {} and {:.0f} Hz commands (ID: {})".format(
			signalFrequency, signalAmplitude, signalTypeStr, commandFrequency, devId)
		plt.ylabel("Motor current (mA)")

	# Specific to the position controller:
	elif(controllerType == hssPosition):#Controller.position):

		title = "Position control with {:.0f} Hz, {:.0f} tick{} {} and {:.0f} Hz commands (ID: {})".format(
			signalFrequency, signalAmplitude, ("s" if signalAmplitude > 1 else ""),
			signalTypeStr, commandFrequency, devId)
		plt.ylabel("Encoder position")

	# Common info:
	plt.plot(times, requests, color='b', label='Desired')
	plt.plot(times, measurements, color='r', label='Measured')
	plt.xlabel("Time (s)")
	plt.title(title, wrap=True)
	plt.legend(loc='upper right')
	# Style parameters and webb server address for external clients
	matplotlib.rcParams.update({'figure.constrained_layout.use': True,
								'figure.constrained_layout.h_pad': 0.5})
	if isPi():
		matplotlib.rcParams.update({'webagg.address': '0.0.0.0'})

	# Draw a vertical line at the end of each cycle
	for endpoints in cycleStopTimes:
		plt.axvline(x=endpoints, color='xkcd:light grey', linestyle='--')

	return fig

# Multiple figures: command and stream times in linear and occurrence log
# Supports two types at once
def plotExpStats(devId, fig, writeCommandTimes, readCommandTimes):
	fig = plotExpStatsOneType(devId, fig, writeCommandTimes, "Write")
	fig = plotExpStatsOneType(devId, fig, readCommandTimes, "Read")
	return fig

# Two figures: command and stream times in linear and occurrence log
def plotExpStatsOneType(devId, fig, actionTimes, title):

	# Figure: command time vs time, linear scale
	plt.figure(fig)
	fig += 1
	actionTimes = [i * 1000 for i in actionTimes]
	# Convert command times into ms
	plt.plot(actionTimes, color='b', label='Times')
	plt.title(title + " Time vs Time" ' (ID:' + str(devId) + ')')
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	# Figure: time occurrences, log
	plt.figure(fig)
	fig += 1
	plt.yscale('log')
	plt.hist(actionTimes, bins=100, label = 'Setpoints')
	plt.yscale('log')
	plt.title(title + " Time Occurrence" + ' (ID:' + str(devId) + ')')
	plt.legend(loc='upper right')
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	return fig
