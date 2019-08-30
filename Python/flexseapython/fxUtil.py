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
def loadPortsFromFile(filename):
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
	baudRate = []
	# this now looks for the baud rate in the first line of com.txt and the com
	# ports on all following lines. I'm also adding a com_template.txt and
	# gitignoring com.txt so if you change the value it does not make your repo
	# dirty
	# TODO: need to check if com.txt exists and if it does not let the user know
	# they should copy com_template.txt to com.txt
	with open(filename, 'r') as f:
		lines = f.readlines()
		baudRate = lines[0].strip()
		for line in lines[1:]:
			portList.append(line.strip())
	return portList, baudRate