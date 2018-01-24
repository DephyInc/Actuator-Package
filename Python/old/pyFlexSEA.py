#Python wrapper for the FlexSEA stack

import ctypes
from ctypes import *
from ctypes import cdll
from ctypes import _SimpleCData
import serial
from time import sleep
from pyFlexSEA_def import *
import os

#Variables used to send packets:
nb = c_ushort(0)
packetIndex = c_ushort(0)
arrLen = c_ubyte(10)
commStr = (c_ubyte * COMM_STR_LEN)()
cBytes = (c_uint8 * COMM_STR_LEN)()
myRigid = rigid_s();

#ActPack variables:
controller = c_uint8(CTRL_NONE)
setpoint = c_int32(0)
setGains = c_uint8(0)
g0 = c_int16(0)
g1 = c_int16(0)
g2 = c_int16(0)
g3 = c_int16(0)
system = c_uint8(0)

#Stack init and support functions:
#=================================

def initPyFlexSEA():
	#Init code:
	print('[pySerial Module]\n')
	global flexsea
	flexsea = cdll.LoadLibrary('lib/FlexSEA-Stack-Plan.dll')
	#Init stack:
	flexsea.initFlexSEAStack_minimalist(FLEXSEA_PLAN_1);

#Get serial port handle from host
def setPyFlexSEASerialPort(s):
	global hser
	hser = s

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

#ActPack user functions:
#=======================

#Set Control Mode:
def setControlMode(ctrlMode):
	global controller
	controller = c_uint8(ctrlMode)

#Set Motor Voltage:
def setMotorVoltage(mV):
	global setpoint
	setpoint = c_int32(mV)

#ActPack is used to read sensor values, and write controller options & setpoint
#minOffs & maxOffs control what offsets are read (0: IMU, joint enc., etc., 
# 1: motor ang/vel/acc, board state, etc., 2: genVar (used for 6-ch Strain), ...)
#printDiv: values will be displayed on the terminal every printDiv samples
def readActPack(minOffs, maxOffs, printDiv):

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
			i = printActPack(printDiv)
			return i
		#else:
			#print('This is not a Rigid packet')
	#else:
		#print('Invalid packet')

#Send Read Request ActPack:
def requestReadActPack(offset):
	flexsea.ptx_cmd_actpack_rw(FLEXSEA_MANAGE_1, byref(nb), commStr, offset, controller, setpoint, setGains, g0, g1, g2, g3, system);
	hser.write(commStr)

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

#Print ActPack data (Rigid + controller info):
def printActPack(div):
	if(printDiv(div) == 0):
		global controller
		global setpoint
		global g0
		global g1
		global g2
		global g3
		os.system('cls') #Clear terminal
		printController(controller, setpoint, g0, g1, g2, g3)
		printRigid()
		return 0
	return 1

#Prints easy to read info about the controller
def printController(ctrl, sp, g0, g1, g2, g3):
	c = mapCtrlText[ctrl.value]
	s = sp.value
	print('\nController:', c, '|', 'Setpoint:', s)
	print('Gains: [', g0.value, ', ', g1.value, ', ', g2.value, ', ', g3.value, ']\n')

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

#Functions belowe this line are kept mostly for legacy reasons. Use with care.
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
