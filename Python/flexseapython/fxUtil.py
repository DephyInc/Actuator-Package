from flexseapython.pyFlexsea import *
from time import sleep
import os

#Clears the terminal - use before printing new values
def clearTerminal():
	isWin = os.name == 'nt'
	if isWin:
		os.system('cls')	#Clear terminal (Win)
	else:
		os.system('clear')	#Clear terminal (Unix)

def printDevice(actPackState: ActPackState):
	print('Actpack State time:   	', actPackState.timestamp)
	print('Accel X:              	', actPackState.accelx)
	print('Accel Y:              	', actPackState.accely)
	print('Accel Z:              	', actPackState.accelz)
	print('Gyro X:               	', actPackState.gyrox)
	print('Gyro Y:               	', actPackState.gyroy)
	print('Gyro Z:               	', actPackState.gyroz)
	print('Motor angle:          	', actPackState.encoderAngle)
	print('Motor voltage:        	', actPackState.motorVoltage)
	print('Battery Current (mA): 	', actPackState.batteryCurrent)
	print('Battery Voltage (mV): 	', actPackState.batteryVoltage)
	print('Battery Temp (C):     	', actPackState.batteryTemp)
	
def printExo(exoState: ExoState):
	print('Exo State time:          ', exoState.timestamp)
	print('Accel X:              	', exoState.accelx)
	print('Accel Y:              	', exoState.accely)
	print('Accel Z:              	', exoState.accelz)
	print('Gyro X:               	', exoState.gyrox)
	print('Gyro Y:               	', exoState.gyroy)
	print('Gyro Z:               	', exoState.gyroz)
	print('Motor angle:          	', exoState.encoderAngle)
	print('Motor voltage:        	', exoState.motorVoltage)
	print('Battery Current (mA): 	', exoState.batteryCurrent)
	print('Battery Voltage (mV): 	', exoState.batteryVoltage)
	print('Battery Temp (C):     	', exoState.batteryTemp)

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
