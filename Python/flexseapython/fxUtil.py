from flexseapython.pyFlexsea import *
from time import sleep
import numpy as np
import os

# Clears the terminal - use before printing new values
def clearTerminal():
	isWin = os.name == 'nt'
	if isWin:
		os.system('cls')	#Clear terminal (Win)
	else:
		os.system('clear')	#Clear terminal (Unix)

# Prints plot exit message
def printPlotExit():
	if (os.name == 'nt'):
		print('\nIn Windows, press Ctrl+BREAK to exit. Ctrl+C may not work.')

def printDevice(actPackState: ActPackState):
	print('[ Printing Actpack ]\n')
	print('State time:           ', actPackState.timestamp)
	print('Accel X:              ', actPackState.accelx)
	print('Accel Y:              ', actPackState.accely)
	print('Accel Z:              ', actPackState.accelz)
	print('Gyro X:               ', actPackState.gyrox)
	print('Gyro Y:               ', actPackState.gyroy)
	print('Gyro Z:               ', actPackState.gyroz)
	print('Motor angle:          ', actPackState.encoderAngle)
	print('Motor voltage (mV):   ', actPackState.motorVoltage)
	print('Battery Current (mA): ', actPackState.batteryCurrent)
	print('Battery Voltage (mV): ', actPackState.batteryVoltage)
	print('Battery Temp (C):     ', actPackState.batteryTemp)

def printExo(exoState: ExoState):
	print('[ Printing Exo/ActPack Plus ]\n')
	print('State time:           ', exoState.timestamp)
	print('Accel X:              ', exoState.accelx)
	print('Accel Y:              ', exoState.accely)
	print('Accel Z:              ', exoState.accelz)
	print('Gyro X:               ', exoState.gyrox)
	print('Gyro Y:               ', exoState.gyroy)
	print('Gyro Z:               ', exoState.gyroz)
	print('Motor angle:          ', exoState.encoderAngle)
	print('Motor voltage (mV):   ', exoState.motorVoltage)
	print('Motor current (mA):   ', exoState.motorCurrent)
	print('Battery Current (mA): ', exoState.batteryCurrent)
	print('Battery Voltage (mV): ', exoState.batteryVoltage)
	print('Battery Temp (C):     ', exoState.batteryTemp)
	print('genVar[0]:            ', exoState.genVar[0])
	print('genVar[1]:            ', exoState.genVar[1])
	print('genVar[2]:            ', exoState.genVar[2])
	print('genVar[3]:            ', exoState.genVar[3])
	print('genVar[4]:            ', exoState.genVar[4])
	print('genVar[5]:            ', exoState.genVar[5])
	print('genVar[6]:            ', exoState.genVar[6])
	print('genVar[7]:            ', exoState.genVar[7])
	print('genVar[8]:            ', exoState.genVar[8])
	print('genVar[9]:            ', exoState.genVar[9])
	print('Ankle angle:          ', exoState.ankleAngle)
	print('Ankle velocity:       ', exoState.ankleVelocity)

def printNetMaster(netMasterState: NetMasterState):
	print('[ Printing NetMaster ]\n')
	print('State time:        ', netMasterState.timestamp)
	print('genVar[0]:         ', netMasterState.genVar[0])
	print('genVar[1]:         ', netMasterState.genVar[1])
	print('genVar[2]:         ', netMasterState.genVar[2])
	print('genVar[3]:         ', netMasterState.genVar[3])
	print('Status:            ', netMasterState.status)
	print('NetNode0 - accelx: ', netMasterState.netNode[0].accelx, ', accely: ', netMasterState.netNode[0].accely, ' accelz: ', netMasterState.netNode[0].accelz)
	print('NetNode0 - gyrox:  ', netMasterState.netNode[0].gyrox,  ', gyroy:  ', netMasterState.netNode[0].gyroy,  ' gyroz:  ', netMasterState.netNode[0].gyroz)
	print('NetNode1 - accelx: ', netMasterState.netNode[1].accelx, ', accely: ', netMasterState.netNode[1].accely, ' accelz: ', netMasterState.netNode[1].accelz)
	print('NetNode1 - gyrox:  ', netMasterState.netNode[1].gyrox,  ', gyroy:  ', netMasterState.netNode[1].gyroy,  ' gyroz:  ', netMasterState.netNode[1].gyroz)
	print('NetNode2 - accelx: ', netMasterState.netNode[2].accelx, ', accely: ', netMasterState.netNode[2].accely, ' accelz: ', netMasterState.netNode[2].accelz)
	print('NetNode2 - gyrox:  ', netMasterState.netNode[2].gyrox,  ', gyroy:  ', netMasterState.netNode[2].gyroy,  ' gyroz:  ', netMasterState.netNode[2].gyroz)
	print('NetNode3 - accelx: ', netMasterState.netNode[3].accelx, ', accely: ', netMasterState.netNode[3].accely, ' accelz: ', netMasterState.netNode[3].accelz)
	print('NetNode3 - gyrox:  ', netMasterState.netNode[3].gyrox,  ', gyroy:  ', netMasterState.netNode[3].gyroy,  ' gyroz:  ', netMasterState.netNode[3].gyroz)
	print('NetNode4 - accelx: ', netMasterState.netNode[4].accelx, ', accely: ', netMasterState.netNode[4].accely, ' accelz: ', netMasterState.netNode[4].accelz)
	print('NetNode4 - gyrox:  ', netMasterState.netNode[4].gyrox,  ', gyroy:  ', netMasterState.netNode[4].gyroy,  ' gyroz:  ', netMasterState.netNode[4].gyroz)
	print('NetNode5 - accelx: ', netMasterState.netNode[5].accelx, ', accely: ', netMasterState.netNode[5].accely, ' accelz: ', netMasterState.netNode[5].accelz)
	print('NetNode5 - gyrox:  ', netMasterState.netNode[5].gyrox,  ', gyroy:  ', netMasterState.netNode[5].gyroy,  ' gyroz:  ', netMasterState.netNode[5].gyroz)
	print('NetNode6 - accelx: ', netMasterState.netNode[6].accelx, ', accely: ', netMasterState.netNode[6].accely, ' accelz: ', netMasterState.netNode[6].accelz)
	print('NetNode6 - gyrox:  ', netMasterState.netNode[6].gyrox,  ', gyroy:  ', netMasterState.netNode[6].gyroy,  ' gyroz:  ', netMasterState.netNode[6].gyroz)
	print('NetNode7 - accelx: ', netMasterState.netNode[7].accelx, ', accely: ', netMasterState.netNode[7].accely, ' accelz: ', netMasterState.netNode[7].accelz)
	print('NetNode7 - gyrox:  ', netMasterState.netNode[7].gyrox,  ', gyroy:  ', netMasterState.netNode[7].gyroy,  ' gyroz:  ', netMasterState.netNode[7].gyroz)

# Most scripts will print a loop count:
def printLoopCount(i, total):
	print('\nLoop', i + 1, 'of', total)

# And some will include the elapsed time
def printLoopCountAndTime(i, total, elapsed_time):
	print('\nLoop', i + 1, 'of', total, '- Elapsed time:', int(elapsed_time+0.5), 's', end='\r')

# Generate a sine wave of a specific amplitude and frequency
def sinGenerator(amplitude, frequency, commandFreq):
	num_samples = commandFreq / frequency
	print("number of samples is: ", int(num_samples))
	in_array = np.linspace(-np.pi, np.pi, int(num_samples))
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals

# Generate a line with specific amplitude
def lineGenerator(amplitude, length, commandFreq):
	num_samples = np.int32(length * commandFreq)
	line_vals = [ amplitude for i in range(num_samples) ]
	return line_vals

# Interpolates between two positions (A to B)
def linearInterp(a, b, points):
	lin_array = np.linspace(a, b, points)
	return lin_array

# By default takes just one device from your com.txt file
# If two arguments are passed, one is the path of the COM.txt file
# the other is the number of devices expected
def loadPortsFromFile(filename):
	loadSuccess = loadFlexsea()
	if(not loadSuccess):
		raise Exception('Could not load FlexSEA libraries.')

	# this now looks for the baud rate in the first line of com.txt and the com
	# ports on all following lines. Copy com_template.txt to com.txt and fill
	# in the correct baud rate and serial ports for your device
	portList = []
	try:
		with open(filename, 'r') as f:
			lines = f.readlines()
			gotBaudRate=False

			for lineNum in lines:
				#check if it's a comment
				notAComment=not("#" in lineNum)
				notABlankLine= len(lineNum.strip())>0

				#if it's not a comment check it.  if not, we don't care.
				if(notAComment and notABlankLine):
					if(gotBaudRate):
						portList.append(lineNum.strip())
					else:
						baudRate = int(lineNum.strip())
						gotBaudRate = True;
			#baudRate = lines[0].strip()
			#for line in lines[1:]:
				#portList.append(line.strip())
	except IOError:
		print("\n\nNo com.txt found in the flexseapython directory..."\
				"\nPlease copy the com_template.txt found there to a file named com.txt"\
				"\nBe sure to use the same format of baud rate on the first line,"\
				"\nand com ports on preceding lines\n\n")
		raise
	return portList, baudRate
