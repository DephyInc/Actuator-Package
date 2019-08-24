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
from flexseapython.flexsea_demo.twopositioncontrol import fxTwoPositionControl
from flexseapython.flexsea_demo.streamManager import Stream

def fxFindPoles(port):
	stream = Stream(port, printingRate =2, labels=[], varsToStream=[])
	findPoles(stream.devId, 1)
	del stream

def main():
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports = loadPortsFromFile(fpath)
	print('Loaded ports: ' + str(ports))
	testResults = []
	for device in ports:
		for expNumb in range(len(test_cases)):
			try:
				testResults.append((test_cases[expNumb][0](device,**test_cases[expNumb][2]), device))
				sleep(1)
			except Exception as e:
				print("broke: " + str(e))
	if all([test[0] for test in testResults]):
		print("All tests passed")
	else:
		failedTests = [(idx,device) for idx,(test,device) in enumerate(testResults) if not test]
		print("The following tests failed:")
		failedTestNames = [test_cases[idx%len(test_cases)][1] + " for " + device for idx,device in failedTests]
		print(failedTestNames)
			
	cleanupPlanStack()
# The test case in a tuple containing the function to be tested, its name and the
# parameters used to test it. ** unpacks the parameter dict into named keywords
test_cases = [ 									\
		#(fxFindPoles, "Find Poles", dict()),			\
		(fxPositionControl, "Position Control", {"time":1,'resolution':150}),	\
		(fxReadOnly, "Read Only", {"time": 1}),	\
		(fxOpenControl, "Open Control", {}),		\
		(fxCurrentControl, "Current Control", {'holdCurrent':[200,300,400]}),		\
		(fxTwoPositionControl, "Two position control", {'time' : 4, 'time_step': 0.1, 'transition_time':2 ,'resolution': 1000})]


main()
