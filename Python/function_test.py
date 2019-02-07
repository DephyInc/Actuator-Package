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
	for expNumb, experiment in enumerate(experiments):
		try:
			dummy_var = raw_input("The " + experiments[expNumb][1] +  " test is about to start. Ready?")
			if(expNumb < 6):
				experiments[expNumb][0](devIds[0])
			elif len(devIds) >= 2 and expNumb >= 6:
				experiments[expNumb][0](devIds[0], devIds[1])
			else:
				print("Skipping experiment")
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

main()
