import os, sys
thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(thisdir)

import traceback

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
#from flexseapython.flexsea_demo.twopositioncontrol import fxTwoPositionControl

def fxRunFindPoles(port, baudRate):
	devId = fxOpen(port, baudRate, 0)
	if (fxFindPoles(devId) == FxInvalidDevice):
		raise ValueError('fxFindPoles: invalid device ID')

def main():
	print('')
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports, baudRate = loadPortsFromFile(fpath)
	print('Loaded ports: ' + str(ports))
	print('Using baud rate: ' + str(baudRate))

	try:
		expNumb = selectExperiment()
		
		if (expNumb == 5 or expNumb == 6): # High speed/stress tests
			numDevices = input('\nHow many devices to use for high speed test (1 or 2)?\n')
			if (int(numDevices) == 1):
				experiments[expNumb][0](ports[0],int(baudRate))
			elif (int(numDevices) == 2):
				experiments[expNumb][0](ports[0],int(baudRate),ports[1])
			else:
				print('Invalid number of devices to use for high speed test. Exiting...')
				exit()

		elif(expNumb < len(experiments) - 2):
			experiments[expNumb][0](ports[0],int(baudRate))
		else:
			experiments[expNumb][0](ports[0],ports[1],int(baudRate))

	except Exception as e:
		print(traceback.format_exc())
	print('Exiting fxMain()')

experiments =  [									\
	(fxReadOnly,		"Read Only"),			\
	(fxOpenControl, "Open Control"),		\
	(fxCurrentControl, "Current Control"),	\
	(fxPositionControl, "Position Control"),	\
	(fxImpedanceControl, "Impedance Control"), \
	(fxHighSpeedTest, "High Speed Test"),	\
	(fxHighStressTest, "High Stress Test"),	\
#	(fxUserRW, "User RW"), \
	(fxRunFindPoles,	"Find Poles"),			\
#	(fxTwoPositionControl, "Two Positions Control"), \
	(fxTwoDevicePositionControl,	"Two Devices Position Control"),	 \
	(fxLeaderFollower,	"Two Devices Leader Follower Control"),
]

def selectExperiment():
	expString = ''
	for i in range(0, len(experiments)):
		expString = expString + '[' + str(i) + '] ' + str(experiments[i][1]) + '\n'

	choice = input('\nChoose an experiment:\n' + expString )
	return int(choice)

main()
