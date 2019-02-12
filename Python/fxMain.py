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
from flexseapython.flexsea_demo.two_devices_positioncontrol import fxTwoDevicePositionControl
from flexseapython.flexsea_demo.two_devices_leaderfollower import fxLeaderFollower
from flexseapython.flexsea_demo.twopositioncontrol import fxTwoPositionControl
#Specify the number of devices - this has to be consistent with com.txt
FLEXSEA_DEVICES = 1

def fxFindPoles(devId):
	findPoles(devId, FLEXSEA_DEVICES)

def main():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	devIds = loadAndGetDevice(fpath, FLEXSEA_DEVICES)
	print('Got devices: ' + str(devIds))
#	devIds = loadAndGetDevice(['COM3', 'COM13'])
	try:
		expNumb = selectExperiment()
		if(expNumb < 6):
			experiments[expNumb][0](devIds[0])
		else:
			experiments[expNumb][0](devIds[0], devIds[1])
	except Exception as e:
		print("broke: " + str(e))
		pass

experiments = [ 									\
		(fxReadOnly,		"Read Only"),	 		\
		(fxOpenControl,	 "Open Control"),		\
		(fxCurrentControl,  "Current Control"),		\
		(fxPositionControl, "Position Control"),	\
		(fxFindPoles,	   "Find Poles"),			\
		(fxTwoPositionControl, "Two position control"), \
		(fxTwoDevicePositionControl,	"Two Device Position Control"),	 \
		(fxLeaderFollower,			  "Two Device Leader Follower Control"),
]

def selectExperiment():
	expString = ''
	for i in range(0, len(experiments)):
		expString = expString + '[' + str(i) + '] ' + str(experiments[i][1]) + '\n'

	choice = input('Choose an experiment:\n' + expString )
	return int(choice)



main()
