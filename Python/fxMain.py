from signal import signal, SIGINT
import os
import sys
import traceback

if sys.platform == 'win32':		# For Python 3.8 compatibility:
	import asyncio
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(thisdir)

from flexseapython.pyFlexsea import *
from flexseapython.fxUtil import *
from flexseapython.flexsea_demo.readonly import fxReadOnly
from flexseapython.flexsea_demo.opencontrol import fxOpenControl
from flexseapython.flexsea_demo.currentcontrol import fxCurrentControl
from flexseapython.flexsea_demo.positioncontrol import fxPositionControl
from flexseapython.flexsea_demo.high_speed_test import fxHighSpeedTest
from flexseapython.flexsea_demo.high_stress_test import fxHighStressTest
from flexseapython.flexsea_demo.two_devices_positioncontrol import fxTwoDevicePositionControl
from flexseapython.flexsea_demo.impedancecontrol import fxImpedanceControl
from flexseapython.flexsea_demo.two_devices_leaderfollower import fxLeaderFollower
from flexseapython.flexsea_demo.twopositioncontrol import fxTwoPositionControl

def handler(signal_received, frame):
	sys.exit('SIGINT or CTRL-C detected\nExiting gracefully ...')

def fxRunFindPoles(port, baudRate):
	devId = fxOpen(port, baudRate, 0)
	if (fxFindPoles(devId) == FxInvalidDevice):
		raise ValueError('fxFindPoles: invalid device ID')

def main(argv):
	numDevices = 0
	if len(argv) > 1:		# We have command-line arguments
		numDevices_str = argv[1]
		if numDevices_str.isdecimal():
			numDevices = int(numDevices_str)
		else:				# Invalid number of devices
			sys.exit('\nUsage: python fxMain.py [number_of_devices]')

	# Tell Python to run the handler() function when SIGINT is recieved
	signal(SIGINT, handler)
	print('')
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports, baudRate = loadPortsFromFile(fpath)
	print('Loaded ports: ' + str(ports))
	print('Using baud rate: ' + str(baudRate))

	expNumb = selectExperiment()
	if expNumb == -1:
		sys.exit('Quitting')
	try:
		if (expNumb == 5 or expNumb == 6): # High speed/stress tests
			if numDevices < 1:		# User didn't specify this on command line
				numDevices_str = input('\nNumber of devices?\t')
				if numDevices_str.isdecimal():
					numDevices = int(numDevices_str)
				else:
					error_msg = 'Invalid number of devices [' + numDevices_str + ']. Exiting...'
					sys.exit(error_msg)
			if (int(numDevices) == 1):
				experiments[expNumb][0](ports[0],int(baudRate))
			elif (int(numDevices) == 2):
				experiments[expNumb][0](ports[0],int(baudRate),ports[1])
			else:
				sys.exit('Not implemented: Handling >2 attached devices.')

		elif(expNumb < len(experiments) - 2):
			experiments[expNumb][0](ports[0],int(baudRate))
		else:
			experiments[expNumb][0](ports[0],ports[1],int(baudRate))

	except Exception as e:
		print(traceback.format_exc(e))
	print('\nExiting fxMain()')

experiments =  [									\
	(fxReadOnly,					"Read Only"),			\
	(fxOpenControl, 				"Open Control"),		\
	(fxCurrentControl, 				"Current Control"),	\
	(fxPositionControl,				"Position Control"),	\
	(fxImpedanceControl, 			"Impedance Control"), \
	(fxHighSpeedTest, 				"High Speed Test"),	\
	(fxHighStressTest, 				"High Stress Test"),	\
	#(fxUserRW, 					"User RW"), \
	(fxRunFindPoles,				"Find Poles"),			\
	(fxTwoPositionControl, 			"Two Positions Control"), \
	(fxTwoDevicePositionControl,	"Two Devices Position Control"),	 \
	(fxLeaderFollower,				"Two Devices Leader Follower Control"),
]

def selectExperiment():
	expString = ''
	for i in range(0, len(experiments)):
		expString = expString + '[' + str(i) + '] ' + str(experiments[i][1]) + '\n'

	choice = input('\nChoose an experiment [q to quit]:\n' + expString)
	if choice == 'q':
		return -1
	return int(choice)

if __name__ == '__main__':
	main(sys.argv)
