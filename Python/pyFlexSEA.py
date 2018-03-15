#Python wrapper for the FlexSEA stack

import ctypes
from ctypes import *
from ctypes import cdll
from ctypes import _SimpleCData
import serial
from time import sleep
from pyFlexSEA_def import *
import os
import sys

#Variables used to send packets:
nb = c_ushort(0)
packetIndex = c_ushort(0)
arrLen = c_ubyte(10)
commStr = (c_ubyte * COMM_STR_LEN)()
cBytes = (c_uint8 * COMM_STR_LEN)()
myRigid = rigid_s();
myPocket = pocket_s();

#Control variables:
controlChannels = 2
pCtrl = (c_uint8 * controlChannels)()
pSetpoint = (c_int32 * controlChannels)()
pSetGains = (c_uint8 * controlChannels)()
pG0 = (c_int16 * controlChannels)()
pG1 = (c_int16 * controlChannels)()
pG2 = (c_int16 * controlChannels)()
pG3 = (c_int16 * controlChannels)()
pSystem = c_uint8(0)

#Stack init and support functions:
#=================================

def initPyFlexSEA():
	#Init code:
	print('[pySerial Module]\n')
	global flexsea
	libraries = ['lib/FlexSEA-Stack-Plan', # Windows
				'lib/libFlexSEA-Stack-Plan.so', # Linux
				'lib/rpiFlexSEA-Stack-Plan.so'] # Raspbian
	
	for lib in libraries:
		try:
			flexsea = cdll.LoadLibrary(lib)
			break
		except:
			pass

	#Init stack:
	flexsea.initFlexSEAStack_minimalist(FLEXSEA_PLAN_1);
	#Initialize control variables:
	initControlVariables()

def initControlVariables():
	for i in range(0, controlChannels):
		pCtrl[i] = c_uint8(CTRL_NONE)
		pG0[i] = c_int16(0)
		pG1[i] = c_int16(0)
		pG2[i] = c_int16(0)
		pG3[i] = c_int16(0)
		pSetpoint[i] = c_int32(0)
		pSetGains[i] = c_uint8(KEEP)

#Get serial port handle from host
def setPyFlexSEASerialPort(s):
	global hser
	hser = s

#Read serial port from com.txt file
def comPortFromFile():
	file = open("com.txt", "r")
	s = file.read()
	#print(s)
	return s
	
#Did we receive new serial bytes?
def serialBytesReady(timeout, b):
	i = 0
	while hser.in_waiting < b:
		i = i + 1
		if i > timeout:
			break
	return hser.in_waiting

#Next communication offset
ri_offs = 0
def offs(min, max):
	global ri_offs
	ri_offs += 1
	if ri_offs > max:
		ri_offs = min
	return ri_offs

#Clears the terminal - use before printing new values
def clearTerminal():
	if sys.platform.lower().startswith('win'):
		os.system('cls') #Clear terminal (Win)
	elif sys.platform.lower().startswith('linux'):
		os.system('clear') #Clear terminal (Unix)

#ActPack user functions:
#=======================

#ActPack is used to read sensor values, and write controller options & setpoint
#minOffs & maxOffs control what offsets are read (0: IMU, joint enc., etc., 
# 1: motor ang/vel/acc, board state, etc., 2: genVar (used for 6-ch Strain), ...)
#printDiv: values will be displayed on the terminal every printDiv samples
def readActPack(minOffs, maxOffs, printDiv, displayFlexSEA=True):

	requestReadActPack(offs(minOffs, maxOffs))
	bytes = serialBytesReady(100, COMM_STR_LEN)
	
	#s = hser.read(bytes)
	s = hser.read(COMM_STR_LEN) #Reading a fixed length for now
	for i in range(0,bytes-1):
		#print(s[i], end=' ')
		cBytes[i] = s[i]
	#print(']')
	
	ppFlag = c_uint8(0)
	ppFlag = flexsea.receiveFlexSEABytes(byref(cBytes), bytes, 1);
	if(ppFlag):
		#print('We parsed a packet: ', end='')
		cmd = c_uint8(0)
		type = c_uint8(0)
		flexsea.getSignatureOfLastPayloadParsed(byref(cmd), byref(type));
		#print('cmd:', cmd, 'type:', type)
		
		newActPackPacket = c_uint8(0)
		newActPackPacket = flexsea.newActPackRRpacketAvailable();
		
		if(newActPackPacket):
			#print('New Rigid packet(s) available\n')
			flexsea.getLastRigidData(byref(myRigid));
			
			if displayFlexSEA:
				i = printActPack(printDiv)
				return i
		#else:
			#print('This is not a Rigid packet')
	#else:
		#print('Invalid packet')

#Send Read Request ActPack:
def requestReadActPack(offset):
	global pSetGains
	flexsea.ptx_cmd_actpack_rw(FLEXSEA_MANAGE_1, byref(nb), commStr, offset, pCtrl[0], pSetpoint[0], pSetGains[0], pG0[0], pG1[0], pG2[0], pG3[0], pSystem);
	hser.write(commStr)
	if(offset == 0 and pSetGains[0] == CHANGE):
		pSetGains[0] = c_uint8(KEEP)

#Use this function to enable or disable FSM2. Controller will be reset.
def actPackFSM2(on):
	global pSystem
	global pCtrl
	pCtrl[0] = c_uint8(CTRL_NONE)	#Disable controller
	if on:
		pSystem = c_uint8(SYS_NORMAL)
	else:
		pSystem = c_uint8(SYS_DISABLE_FSM2)

	flexsea.ptx_cmd_actpack_rw(FLEXSEA_MANAGE_1, byref(nb), commStr, c_uint8(0), pCtrl[0], pSetpoint[0], pG0[0], pG1[0], pG2[0], pG3[0], pSetGains[0], pSystem);
	hser.write(commStr)

#Sends a request to Execute. Make sure to disable FSM2 first.
def findPoles(block):
	flexsea.ptx_cmd_calibration_mode_rw(FLEXSEA_EXECUTE_1, byref(nb), commStr, c_uint8(CALIBRATION_FIND_POLES))
	hser.write(commStr)
	if not block:
		return
	else:
		for s in range(60,0, -1):
			print(s,'seconds...')
			sleep(1)
		print('Ready!')

#Pocket functions:
#================

#Pocket is used to read sensor values, and write controller options & setpoint (FlexSEA-Pocket only)
#minOffs & maxOffs control what offsets are read 
# 0: IMU, voltages and other Mn + Re variables 
# 1: Right motor
# 2: Left motor
# 3: genVars
#printDiv: values will be displayed on the terminal every printDiv samples
def readPocket(minOffs, maxOffs, printDiv, displayFlexSEA=True):

	requestReadPocket(offs(minOffs, maxOffs))
	bytes = serialBytesReady(100, COMM_STR_LEN)
	
	#s = hser.read(bytes)
	s = hser.read(COMM_STR_LEN) #Reading a fixed length for now
	for i in range(0,bytes-1):
		#print(s[i], end=' ')
		cBytes[i] = s[i]
	#print(']')
	
	ppFlag = c_uint8(0)
	#print("Bytes:", bytes)
	ppFlag = flexsea.receiveFlexSEABytes(byref(cBytes), bytes, 1);
	if(ppFlag):
		#print('We parsed a packet: ', end='')
		cmd = c_uint8(0)
		type = c_uint8(0)
		flexsea.getSignatureOfLastPayloadParsed(byref(cmd), byref(type));
		#print('cmd:', cmd, 'type:', type)
		
		newPocketPacket = c_uint8(0)
		newPocketPacket = flexsea.newPocketRRpacketAvailable();
		
		if(newPocketPacket):
			#print('New Rigid packet(s) available\n')
			flexsea.getLastPocketData(byref(myPocket));
			
			if displayFlexSEA:
				i = printPocket(printDiv)
				return i
		#else:
			#print('This is not a Rigid packet')
	#else:
		#print('Invalid packet')

#Send Read Request ActPack:
def requestReadPocket(offset):
	global pSetGains
	flexsea.ptx_cmd_pocket_rw(FLEXSEA_MANAGE_1, byref(nb), commStr, offset, pCtrl[0], pSetpoint[0], pSetGains[0], pG0[0], pG1[0], pG2[0], pG3[0], pCtrl[1], pSetpoint[1], pSetGains[1], pG0[1], pG1[1], pG2[1], pG3[1], pSystem);
	hser.write(commStr)
	if(pSetGains[0] == CHANGE):
		pSetGains[0] = c_uint8(KEEP)
	if(pSetGains[1] == CHANGE):
		pSetGains[1] = c_uint8(KEEP)

#Set Control Mode:
def setControlMode(ctrlMode, ch=0):
	global pCtrl
	pCtrl[ch] = c_uint8(ctrlMode)

#Set Motor Voltage:
def setMotorVoltage(mV, ch=0):
	global pSetpoint
	pSetpoint[ch] = c_int32(mV)

#Set Motor Current:
def setMotorCurrent(cur, ch=0):
	global pSetpoint
	pSetpoint[ch] = c_int32(cur)

#Set Position Setpoint (Position & Impedance controllers):
def setPosition(p, ch=0):
	global pSetpoint
	pSetpoint[ch] = c_int32(p)

#Set Impedance controller gains.
#z_k & z_b: Impedance K & B
#i_kp & i_ki: Current Proportional & Integral
def setZGains(z_k, z_b, i_kp, i_ki, ch=0):
	global pG0, pG1, pG2, pG3
	global pSetGains
	pG0[ch] = c_int16(z_k)
	pG1[ch] = c_int16(z_b)
	pG2[ch] = c_int16(i_kp)
	pG3[ch] = c_int16(i_ki)
	pSetGains[ch] = c_uint8(CHANGE)

#Display functions:
#==================

#Print Rigid data:
def printRigid():
	print('Gyro X:          ', myRigid.mn.gyro.x)
	print('Gyro Y:          ', myRigid.mn.gyro.y)
	print('Gyro Z:          ', myRigid.mn.gyro.z)
	print('Accel X:         ', myRigid.mn.accel.x)
	print('Accel Y:         ', myRigid.mn.accel.y)
	print('Accel Z:         ', myRigid.mn.accel.z)
	print('Motor angle:     ', myRigid.ex.enc_ang[0])
	print('Motor velocity:  ', myRigid.ex.enc_ang_vel[0])
	print('Motor current:   ', myRigid.ex.mot_current)
	print('Joint angle:     ', myRigid.ex.joint_ang[0])
	print('Joint velocity:  ', myRigid.ex.joint_ang_vel[0])
	print('Joint Ang-Mot:   ', myRigid.ex.joint_ang_from_mot[0])
	print('+VB:             ', myRigid.re.vb)
	print('Battery current: ', myRigid.re.current)
	print('Temperature:     ', myRigid.re.temp)
	print('6-ch strain #0:  ', myRigid.mn.genVar[0])
	print('...              ')

#Print Pocket data:
def printPocket_s():
	print('Gyro X:          ', myPocket.mn.gyro.x)
	print('Gyro Y:          ', myPocket.mn.gyro.y)
	print('Gyro Z:          ', myPocket.mn.gyro.z)
	print('Accel X:         ', myPocket.mn.accel.x)
	print('Accel Y:         ', myPocket.mn.accel.y)
	print('Accel Z:         ', myPocket.mn.accel.z)
	print('Analog[0]:       ', myPocket.mn.analog[0])
	print('Analog[0]:       ', myPocket.mn.analog[1])
	
	print('M1 Angle:        ', myPocket.ex[0].enc_ang[0])
	print('M1 Velocity:     ', myPocket.ex[0].enc_ang_vel[0])
	print('M1 Current:      ', myPocket.ex[0].mot_current)
	print('M1 Voltage:      ', myPocket.ex[0].mot_volt)
	print('M1 Strain:       ', myPocket.ex[0].strain)
	
	print('M2 Angle:        ', myPocket.ex[1].enc_ang[0])
	print('M2 Velocity:     ', myPocket.ex[1].enc_ang_vel[0])
	print('M2 Current:      ', myPocket.ex[1].mot_current)
	print('M2 Voltage:      ', myPocket.ex[1].mot_volt)
	print('M2 Strain:       ', myPocket.ex[1].strain)
	
	print('+VB:             ', myPocket.re.vb)
	print('Battery current: ', myPocket.re.current)
	print('Temperature:     ', myPocket.re.temp)
	print('Status:          ', myPocket.re.status)
	
	print('genVar[0]:       ', myPocket.mn.genVar[0])
	print('genVar[1]:       ', myPocket.mn.genVar[1])
	print('genVar[2]:       ', myPocket.mn.genVar[2])
	print('genVar[3]:       ', myPocket.mn.genVar[3])
	print('...              ')

#Print ActPack data (Rigid + controller info):
def printActPack(div):
	if(printDiv(div) == 0):
		clearTerminal()
		printController(pCtrl[0], pSetpoint[0], pG0[0], pG1[0], pG2[0], pG3[0], pSetGains[0])
		printRigid()
		return 0
	return 1

#Print Pocket data (pocket_s + controller info):
def printPocket(div):
	if(printDiv(div) == 0):
		clearTerminal()
		printController(pCtrl[0], pSetpoint[0], pG0[0], pG1[0], pG2[0], pG3[0], pSetGains[0])
		printController(pCtrl[1], pSetpoint[1], pG0[1], pG1[1], pG2[1], pG3[1], pSetGains[1])
		printPocket_s()
		return 0
	return 1

#Prints easy to read info about the controller
def printController(ctrl, sp, g0, g1, g2, g3, sg):
	c = mapCtrlText[ctrl]
	s = sp
	print('\nController:', c, '|', 'Setpoint:', s)
	print('Gains: [', g0, ', ', g1, ', ', g2, ', ', g3, '] (', sg, ')\n')

#Controller index to string mapping
mapCtrlText = { 0 : 'CTRL_NONE',
				1 : 'CTRL_OPEN',
				2 : 'CTRL_POSITION',
				3 : 'CTRL_CURRENT',
				4 : 'CTRL_IMPEDANCE',
				5 : 'CTRL_CUSTOM',
				6 : 'CTRL_MEASRES',}
#Timing dividers:
printDivider = 0
def printDiv(div):
	global printDivider
	printDivider += 1
	if printDivider > div:
		printDivider = 0
	return printDivider

#Functions below this line are kept mostly for legacy reasons. Use with care.
#=============================================================================

#Send Read Request Rigid:
def requestReadRigid(offset):
	flexsea.ptx_cmd_rigid_r(FLEXSEA_MANAGE_1, byref(nb), commStr, offset);
	hser.write(commStr)

#Set Control Mode:
def setControlMode_manual(ctrlMode):
	flexsea.ptx_cmd_ctrl_mode_w(FLEXSEA_EXECUTE_1, byref(nb), commStr, ctrlMode);
	hser.write(commStr)

#Set Motor Voltage:
def setMotorVoltage_manual(mV):
	flexsea.ptx_cmd_ctrl_o_w(FLEXSEA_EXECUTE_1, byref(nb), commStr, mV);
	hser.write(commStr)
	
def readRigid():

	requestReadRigid(offs())
	bytes = serialBytesReady(100, COMM_STR_LEN)
	
	#s = hser.read(bytes)
	s = hser.read(COMM_STR_LEN) #Reading a fixed length for now
	for i in range(0,bytes-1):
		#print(s[i], end=' ')
		cBytes[i] = s[i]
	#print(']')

	ppFlag = c_uint8(0)
	ppFlag = flexsea.receiveFlexSEABytes(byref(cBytes), bytes, 1);
	if(ppFlag):
		#print('We parsed a packet: ', end='')
		cmd = c_uint8(0)
		type = c_uint8(0)
		flexsea.getSignatureOfLastPayloadParsed(byref(cmd), byref(type));
		#print('cmd:', cmd, 'type:', type)
		
		newRigidPacket = c_uint8(0)
		newRigidPacket = flexsea.newRigidRRpacketAvailable();
		
		if(newRigidPacket):
			#print('New Rigid packet(s) available\n')
			flexsea.getLastRigidData(byref(myRigid));
			printRigid()
		#else:
			#print('This is not a Rigid packet')
	#else:
		#print('Invalid packet')
