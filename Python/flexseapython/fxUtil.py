from flexseapython.pyFlexsea import *
from flexseapython.pyFlexsea_def import *
from time import sleep
import os

def printData(labels, values):
	if(len(values) != len(labels)):
		print("Error printing...") # add error handling
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

# By default takes just one device from your com.txt file
# If two arguments are passed, one is the path of the COM.txt file
# the other is the number of devices expected
def loadPortsFromFile(filename, numDevices = 1):
	loadSuccess = loadFlexsea()
	if(not loadSuccess):
		raise Exception('load FlexSEA failed')
	
	# We should avoid OS or using ROOT (if this fails put it back)
	"""
	isUnix = os.name != 'nt'
	if(isUnix and os.geteuid() != 0):
		sys.exit('\nRoot privileges needed for running this script') # why??
	"""

	portList = []
	with open(filename, 'r') as f:
		portList = [ line.strip() for line in f if ( line.strip() != '' ) ]

	return portList