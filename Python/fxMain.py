import os, sys
thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(thisdir)

from flexseapython.pyFlexsea import *
from flexseapython.pyFlexsea_def import *
from flexseapython.fxUtil import *
from flexseapython.flexsea_demo.readonly import fxReadOnly
from flexseapython.flexsea_demo.opencontrol import fxOpenControl
from flexseapython.flexsea_demo.currentcontrol import fxCurrentControl
from flexseapython.flexsea_demo.positioncontrol import fxPositionControl
from flexseapython.flexsea_demo.high_speed_test import fxHighSpeedTest
from flexseapython.flexsea_demo.two_devices_positioncontrol import fxTwoDevicePositionControl
from flexseapython.flexsea_demo.impedancecontrol import fxImpedanceControl
from flexseapython.flexsea_demo.two_devices_leaderfollower import fxLeaderFollower
from flexseapython.flexsea_demo.twopositioncontrol import fxTwoPositionControl
from flexseapython.flexsea_demo.userRW import fxUserRW
from flexseapython.flexsea_demo.streamManager import Stream

def fxFindPoles(port):
	stream = Stream(port, baudRate, printingRate = 2, labels=[], varsToStream=[])
	findPoles(stream.devId, 1)
	del stream

def main():
	print('')
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports, baudRate = loadPortsFromFile(fpath)
	print('Loaded ports: ' + str(ports))
	print('Using baud rate: ' + str(baudRate))

	try:
		expNumb = selectExperiment()
		if(expNumb < len(experiments) - 2 ):
			experiments[expNumb][0](ports[0],int(baudRate))
		else:
			print(experiments[expNumb][0])
			experiments[expNumb][0](ports[0],ports[1],int(baudRate))

	except Exception as e:
		print("broke: " + str(e))
	cleanupPlanStack()

experiments =  [									\
		(fxReadOnly,		"Read Only"),			\
		(fxOpenControl, "Open Control"),		\
		(fxCurrentControl, "Current Control"),	\
		(fxPositionControl, "Position Control"),	\
		(fxTwoPositionControl, "Two Positions Control"), \
		(fxImpedanceControl, "Impedance Control"), \
		(fxHighSpeedTest, "High Speed Test"),	\
		(fxFindPoles,	"Find Poles"),			\
		(fxUserRW, "User RW"), \
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
