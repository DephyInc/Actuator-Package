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