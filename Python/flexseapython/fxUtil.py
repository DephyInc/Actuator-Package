from flexseapython.pyFlexsea import *
from time import sleep
import os

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
	# ports on all following lines. Copy com_template.txt to com.txt and fill
	# in the correct baud rate and serial ports for your device
	try:
		with open(filename, 'r') as f:
			lines = f.readlines()
			baudRate = lines[0].strip()
			for line in lines[1:]:
				portList.append(line.strip())
	except IOError:
		print("\n\nNo com.txt found in the flexseapython directory..."\
				"\nPlease copy the com_template.txt found there to a file named com.txt"\
				"\nBe sure to use the same format of baud rate on the first line,"\
				"\nand com ports on preceding lines\n\n")
		raise
	return portList, baudRate
