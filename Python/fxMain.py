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

def fxFindPoles(devId):
	findPoles(devId, 2)

def main():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	devIds = loadAndGetDevice(fpath, 2)
	print('Got devices: ' + str(devIds))
#	devIds = loadAndGetDevice(['COM3', 'COM13'])
	try:
		expNumb = selectExperiment()
		if(expNumb < 5):
			experiments[expNumb][0](devIds[0])
		else:
			experiments[expNumb][0](devIds[0], devIds[1])
	except Exception as e:
		print("broke: " + str(e))
		pass

experiments = [ 							\
	(fxReadOnly, "Read Only"), 				\
	(fxOpenControl, "Open Control"),		\
	(fxCurrentControl, "Current Control"),	\
	(fxPositionControl, "Position Control"),\
	(fxFindPoles, "Find Poles"),			\
	(fxTwoDevicePositionControl, "Two Device Position Control"), \
	(fxLeaderFollower, "Two Device Leader Follower Control"),
]

def selectExperiment():
	expString = ''
	for i in range(0, len(experiments)):
		expString = expString + '[' + str(i) + '] ' + str(experiments[i][1]) + '\n'

	choice = input('Choose an experiment:\n' + expString )
	return int(choice)



main()
