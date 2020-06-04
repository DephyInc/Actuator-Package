from flexseapython.pyFlexsea import *
import matplotlib.pyplot as plt
import matplotlib

# Figure: setpoint, desired vs measured
def plotSetpointVsDesired(devId, fig, controllerType, signalFrequency, signalAmplitude, signalTypeStr, commandFrequency, times, requests, measurements, cycleStopTimes):

	plt.figure(fig)
	fig += 1

	# Specific to the current controller:
	if(controllerType == hssCurrent):	#Controller.current):

		title = "Current control with " + "{:.2f}".format(signalFrequency) + " Hz, " + \
			str(signalAmplitude) + " mA " + signalTypeStr + " and " + \
				"{:.2f}".format(commandFrequency) + " Hz commands" + ' (ID:' + str(devId) + ')'
		plt.ylabel("Motor current (mA)")

	# Specific to the position controller:
	elif(controllerType == hssPosition):#Controller.position):
		plt.figure(fig)
		title = "Position control with " + "{:.2f}".format(signalFrequency) + " Hz, " + \
			str(signalAmplitude) + " ticks " + signalTypeStr + " and " + \
				"{:.2f}".format(commandFrequency) + " Hz commands" + ' (ID:' + str(devId) + ')'
		plt.ylabel("Encoder position")

	# Common info:
	plt.plot(times, requests, color='b', label='Desired')
	plt.plot(times, measurements, color='r', label='Measured')
	plt.xlabel("Time (s)")
	plt.title(title)
	plt.legend(loc='upper right')

	# Draw a vertical line at the end of each cycle
	for endpoints in cycleStopTimes:
		plt.axvline(x=endpoints, color='xkcd:light grey')

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
