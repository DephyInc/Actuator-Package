import os, sys
thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(thisdir)
from time import sleep

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
	return True

def main():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports = loadPortsFromFile(fpath, FLEXSEA_DEVICES)
	print('Loaded ports: ' + str(ports))
	test_results = []
	
	for test_num, test_case in enumerate(test_cases):
		clearTerminal()
		print(""" **** Commencing test number """, test_num, """ of """,len(test_cases))
		sleep(1)
		try:
			test_results.append(test_case[0](ports,**test_case[2]))
		except Exception as e:
			print("broke: " + str(e))
	if all(test_results):
		print("All tests passed")
	else:
		failedTests = [idx for idx,test in enumerate(test_results) if not test]
		print("The following tests failed:")
		failedTestNames = [test_cases[idx][1] for idx in failedTests]
		print(failedTestNames)

# The test case in a tuple containing the function to be tested, its name and the
# parameters used to test it. ** unpacks the parameter dict into named keywords
test_cases = [ 									\
		#(fxFindPoles, "Find Poles", dict()),			\
		(fxReadOnly, "Read Only", {"time": 1}), \
		(fxPositionControl, "Position Control", {"time":1,'resolution':150}),	\
		(fxOpenControl, "Open Control", {}),		\
		(fxCurrentControl, "Current Control", {'holdCurrent':[200,300,400]}),		\
		(fxTwoPositionControl, "Two position control", {'time' : 4, 'time_step': 0.1, 'transition_time':2 ,'resolution': 500})]


main()
