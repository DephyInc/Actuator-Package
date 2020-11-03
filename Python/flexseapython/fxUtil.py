from .pyFlexsea import *
from time import sleep
import numpy as np
import os

from .dev_spec import AllDevices

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

def printDevice(device, appType):
	if (appType == FxActPack):
		printActPack(device)
	elif (appType == FxNetMaster):
		printNetmaster(device)
	elif (appType == FxBMS):
		printBMS(device)
	elif (appType == FxExo):
		printExo(device)
	else:
		raise RuntimeError('Unsupported application type: ', appType)

def printExo(exoState: AllDevices.ExoState):
	print('[ Printing Exo/ActPack Plus ]\n')
	print('State time:           ', exoState.state_time)
	print('Accel X:              ', exoState.accelx)
	print('Accel Y:              ', exoState.accely)
	print('Accel Z:              ', exoState.accelz)
	print('Gyro X:               ', exoState.gyrox)
	print('Gyro Y:               ', exoState.gyroy)
	print('Gyro Z:               ', exoState.gyroz)
	print('Motor angle:          ', exoState.mot_ang)
	print('Motor voltage (mV):   ', exoState.mot_volt)
	print('Motor current (mA):   ', exoState.mot_cur)
	print('Battery Current (mA): ', exoState.batt_volt)
	print('Battery Voltage (mV): ', exoState.batt_curr)
	print('Battery Temp (C):     ', exoState.temperature)
	print('genVar[0]:            ', exoState.genvar_0)
	print('genVar[1]:            ', exoState.genvar_1)
	print('genVar[2]:            ', exoState.genvar_2)
	print('genVar[3]:            ', exoState.genvar_3)
	print('genVar[4]:            ', exoState.genvar_4)
	print('genVar[5]:            ', exoState.genvar_5)
	print('genVar[6]:            ', exoState.genvar_6)
	print('genVar[7]:            ', exoState.genvar_7)
	print('genVar[8]:            ', exoState.genvar_8)
	print('genVar[9]:            ', exoState.genvar_9)
	print('Ankle angle:          ', exoState.ank_ang)
	print('Ankle velocity:       ', exoState.ank_vel)

def printActPack(actPackState: AllDevices.ActPackState):
	print('[ Printing Actpack ]\n')
	print('State time:           ', actPackState.state_time)
	print('Accel X:              ', actPackState.accelx)
	print('Accel Y:              ', actPackState.accely)
	print('Accel Z:              ', actPackState.accelz)
	print('Gyro X:               ', actPackState.gyrox)
	print('Gyro Y:               ', actPackState.gyroy)
	print('Gyro Z:               ', actPackState.gyroz)
	print('Motor angle:          ', actPackState.mot_ang)
	print('Motor voltage (mV):   ', actPackState.mot_volt)
	print('Battery Current (mA): ', actPackState.batt_curr)
	print('Battery Voltage (mV): ', actPackState.batt_volt)
	print('Battery Temp (C):     ', actPackState.temperature)

def printNetMaster(netMasterState: AllDevices.NetMasterState):
	print('[ Printing NetMaster ]\n')
	print('State time:        ', netMasterState.state_time)
	print('genVar[0]:         ', netMasterState.genVar_0)
	print('genVar[1]:         ', netMasterState.genVar_1)
	print('genVar[2]:         ', netMasterState.genVar_2)
	print('genVar[3]:         ', netMasterState.genVar_3)
	print('Status:            ', netMasterState.status)
	print('NetNode0 - accelx: ', netMasterState.A_accelx, ', accely: ', netMasterState.A_accely, ' accelz: ', netMasterState.A_accelz)
	print('NetNode0 - gyrox:  ', netMasterState.A_gyrox,  ', gyroy:  ', netMasterState.A_gyroy,  ' gyroz:  ', netMasterState.A_gyroz)
	print('NetNode1 - accelx: ', netMasterState.B_accelx, ', accely: ', netMasterState.B_accely, ' accelz: ', netMasterState.B_accelz)
	print('NetNode1 - gyrox:  ', netMasterState.B_gyrox,  ', gyroy:  ', netMasterState.B_gyroy,  ' gyroz:  ', netMasterState.B_gyroz)
	print('NetNode2 - accelx: ', netMasterState.C_accelx, ', accely: ', netMasterState.C_accely, ' accelz: ', netMasterState.C_accelz)
	print('NetNode2 - gyrox:  ', netMasterState.C_gyrox,  ', gyroy:  ', netMasterState.C_gyroy,  ' gyroz:  ', netMasterState.C_gyroz)
	print('NetNode3 - accelx: ', netMasterState.D_accelx, ', accely: ', netMasterState.D_accely, ' accelz: ', netMasterState.D_accelz)
	print('NetNode3 - gyrox:  ', netMasterState.D_gyrox,  ', gyroy:  ', netMasterState.D_gyroy,  ' gyroz:  ', netMasterState.D_gyroz)
	print('NetNode4 - accelx: ', netMasterState.E_accelx, ', accely: ', netMasterState.E_accely, ' accelz: ', netMasterState.E_accelz)
	print('NetNode4 - gyrox:  ', netMasterState.E_gyrox,  ', gyroy:  ', netMasterState.E_gyroy,  ' gyroz:  ', netMasterState.E_gyroz)
	print('NetNode5 - accelx: ', netMasterState.F_accelx, ', accely: ', netMasterState.F_accely, ' accelz: ', netMasterState.F_accelz)
	print('NetNode5 - gyrox:  ', netMasterState.F_gyrox,  ', gyroy:  ', netMasterState.F_gyroy,  ' gyroz:  ', netMasterState.F_gyroz)
	print('NetNode6 - accelx: ', netMasterState.G_accelx, ', accely: ', netMasterState.G_accely, ' accelz: ', netMasterState.G_accelz)
	print('NetNode6 - gyrox:  ', netMasterState.G_gyrox,  ', gyroy:  ', netMasterState.G_gyroy,  ' gyroz:  ', netMasterState.G_gyroz)
	print('NetNode7 - accelx: ', netMasterState.H_accelx, ', accely: ', netMasterState.H_accely, ' accelz: ', netMasterState.H_accelz)
	print('NetNode7 - gyrox:  ', netMasterState.H_gyrox,  ', gyroy:  ', netMasterState.H_gyroy,  ' gyroz:  ', netMasterState.H_gyroz)

# Most scripts will print a loop count:
def printLoopCount(i, total):
	print('\nLoop', i + 1, 'of', total)

# And some will include the elapsed time
def printLoopCountAndTime(i, total, elapsed_time):
	print('\nLoop {} of {} - Elapsed time: {}s'.format(
		i + 1, total, round(elapsed_time)))

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
