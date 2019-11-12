import os, sys
import glob
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.fxUtil import *

def fxCommunicationTester(port, baudRate, test_duration_seconds = 3, streaming_frequency = 100):
	# Connect to the Device Under Test (DUT)
	devId = fxOpen(port, baudRate, streaming_frequency)
	# Print out the device ID
	print("Device ID: ", devId)
	# Command the device to start streaming data
	fxStartStreaming(devId, True)
	# Allow the device class to handle processing the streaming data in the background
	sleep(test_duration_seconds)
	# All test data is currently stored in the data logger csv file so can now be used for
	# communication quality analysis
	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxCommunicationTester(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
