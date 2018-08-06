from flexseapython.pyFlexsea import *
from flexseapython.pyFlexsea_def import *
from time import sleep
import os

def loadAndGetDevice(filename, numDevices=None):
	loadSuccess = loadFlexsea()
	if(not loadSuccess):
		print("Library load failed... quitting")

        isUnix = os.name != 'nt'
        if(isUnix and os.geteuid() != 0):
            sys.exit('\nRoot privileges needed for running this script')

	if(numDevices != None):
		portList = []
		with open(filename, 'r') as f:
			portList = [ line.strip() for line in f if ( line.strip() != '' ) ]
	else:
		portList = filename
		numDevices = len(portList)

	n = len(portList)
	if(n > FX_NUM_PORTS):
		n = FX_NUM_PORTS

	for i in range(0, n):
		fxOpen(portList[i], i)
		sleep(0.2)
	
	waiting = True
	waited = 0
	while(waiting and waited < 5):
		sleep(0.2)
		waited = waited + 0.2

		waiting = False
		for i in range(0, n):
			if(not fxIsOpen(i)):
				print("Waiting for port {} to be open".format(i))
				waiting = True

	if(waiting):
		print("Couldn't connect...")
		sys.exit(1)
	
	devIds = fxGetDeviceIds()

	while(len(devIds) < numDevices):
		sleep(0.1)
		devIds = fxGetDeviceIds()
	
	return devIds

def printData(labels, values):
	if(len(values) != len(labels)):
		print("Error printing...")
	lens = [len(l) for l in labels]
	maxlen = max(lens)
	fstring = '{0:' + str(maxlen) + 's}: {1}\n'
	s = 'Flexsea Device Data:\n'
	for i in range(0, len(values)):
		s = s + fstring.format(labels[i], values[i])

	print(s)

#Clears the terminal - use before printing new values
def clearTerminal():
        isWin = os.name == 'nt'
        if isWin:
		os.system('cls') #Clear terminal (Win)
        else:
                os.system('clear') #Clear terminal (Unix)
