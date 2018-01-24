import ctypes
from ctypes import *
from ctypes import cdll
from ctypes import _SimpleCData
import serial
from time import sleep

#Constants:
FLEXSEA_PLAN_1 = 10
FLEXSEA_MANAGE_1 = 20
FLEXSEA_EXECUTE_1 = 40
COMMSTR_LEN = 48
CTRL_NONE = 0
CTRL_OPEN = 1

#Variables used to send packets:
nb = c_ushort(0)
packetIndex = c_ushort(0)
arrLen = c_ubyte(10)
commStr = (c_ubyte * COMMSTR_LEN)()

#Send Read Request Rigid:
def requestReadRigid(offset):
	flexsea.ptx_cmd_rigid_r(FLEXSEA_MANAGE_1, byref(nb), commStr, offset);
	ser.write(commStr)

#Print Rigid data:
def printRigid():
	print('Gyro X:', myRigid.mn.gyro.x)
	print('Gyro Y:', myRigid.mn.gyro.y)
	print('Gyro Z:', myRigid.mn.gyro.z)
	print('Accel X:', myRigid.mn.accel.x)
	print('Accel Y:', myRigid.mn.accel.y)
	print('Accel Z:', myRigid.mn.accel.z)

class xyz_s(Structure):
		_fields_ = [("x", c_int16),
					("y", c_int16),
					("z", c_int16)]

class gain_s(Structure):
		_fields_ = [("g0", c_uint16),
					("g1", c_uint16),
					("g2", c_uint16),
					("g3", c_uint16),
					("g4", c_uint16),
					("g5", c_uint16)]

class diffarr_s(Structure):
		_fields_ = [("vals", c_int32 * 50),
					("curval", c_int32),
					("indx", c_int32),
					("curdif", c_int32),
					("avg", c_int32)]

class gen_ctrl_s(Structure):
		_fields_ = [("gain", gain_s),
					("actual_val", c_int32),
					("setpoint_val", c_int32),
					("actual_vel", c_int32),
					("actual_vals", diffarr_s),
					("error", c_int32),
					("error_prev", c_int32),
					("error_sum", c_int32),
					("error_dif", c_int32),
					("trap_t", c_int64)]

class pos_ctrl_s(Structure):
		_fields_ = [("gain", gain_s),
					("pos", c_int32),
					("setp", c_int32),
					("posi", c_int32),
					("posf", c_int32),
					("spdm", c_int32),
					("acc", c_int32),
					("error", c_int32),
					("error_prev", c_int32),
					("error_sum", c_int32),
					("error_dif", c_int32),
					("trap_t", c_int64)]

class ctrl_s(Structure):
		_fields_ = [("active_ctrl", c_uint8),
					("pwm", c_int32),
					("generic", gen_ctrl_s),
					("current", gen_ctrl_s),
					("position", pos_ctrl_s),
					("impedance", gen_ctrl_s)]

class decoded_xyz_s(Structure):
		_fields_ = [("x", c_int32),
					("y", c_int32),
					("z", c_int32)]

class decoded_fx_rigid_mn_s(Structure):
		_fields_ = [("gyro", decoded_xyz_s),
					("accel", decoded_xyz_s),
					("magneto", decoded_xyz_s)]

class fx_rigid_re_s(Structure):
		_fields_ = [("vb", c_uint16),
					("vg", c_uint16),
					("v5", c_uint16),
					("current", c_int16),
					("temp", c_int8),
					("button", c_uint8),
					("state", c_uint8),
					("status", c_uint16)]

class fx_rigid_mn_s(Structure):
		_fields_ = [("gyro", xyz_s),
					("accel", xyz_s),
					("magneto", xyz_s),
					("analog", c_uint16 * 4),
					("status", c_uint16),
					("genVar", c_int16 * 10),
					("decoded", decoded_fx_rigid_mn_s)]

class fx_rigid_ctrl_s(Structure):
		_fields_ = [("timestamp", c_uint32),
					("walkingState", c_int8),
					("gaitState", c_int8),
					("ank_ang_deg", POINTER(c_int16)),
					("ank_vel", POINTER(c_int16)),
					("ank_ang_from_mot", POINTER(c_int16))]

class fx_rigid_ex_s(Structure):
		_fields_ = [("strain", c_uint16),
					("mot_current", c_int32),
					("mot_volt", c_int32),
					("enc_ang", POINTER(c_int32)),
					("enc_ang_vel", POINTER(c_int32)),
					("joint_ang", POINTER(c_int16)),
					("joint_ang_vel", POINTER(c_int16)),
					("joint_ang_from_mot", POINTER(c_int16)),
					("mot_acc", c_int32),
					("status", c_uint16),
					("ctrl", ctrl_s)]

class rigid_s(Structure):
		_fields_ = [("re", fx_rigid_re_s),
		("mn", fx_rigid_mn_s),
		("ex", fx_rigid_ex_s),
		("ctrl", fx_rigid_ctrl_s),
		("lastOffsetDecoded", c_uint8)]

#"Main":
print('\nDemo code #2 - Python project with FlexSEA-Stack DLL')
print('====================================================\n')
flexsea = cdll.LoadLibrary('lib/FlexSEA-Stack-Plan.dll')

#Init stack:
flexsea.initFlexSEAStack_minimalist(FLEXSEA_PLAN_1);

#Open serial port:
ser = serial.Serial('COM5')
print('Opened', ser.portstr)

#Demo code - Single Read, Rigid:
#===============================

requestReadRigid(0);
sleep(0.1)
bytes = ser.in_waiting
cBytes = (c_uint8 * COMMSTR_LEN)()
print('Bytes received:', bytes, '[ ', end='')
s = ser.read(bytes)
for i in range(0,bytes-1):
	print(s[i], end=' ')
	cBytes[i] = s[i]
print(']')
#Feed bytes to stack:
ppFlag = c_uint8(0)
ppFlag = flexsea.receiveFlexSEABytes(byref(cBytes), bytes, 1);
if(ppFlag):
	print('We parsed a packet: ', end='')
	cmd = c_uint8(0)
	type = c_uint8(0)
	flexsea.getSignatureOfLastPayloadParsed(byref(cmd), byref(type));
	print('cmd:', cmd, 'type:', type)
	
	newRigidPacket = c_uint8(0)
	newRigidPacket = flexsea.newRigidRRpacketAvailable();
	
	if(newRigidPacket):
		print('New Rigid packet(s) available\n')
		myRigid = rigid_s();
		flexsea.getLastRigidData(byref(myRigid));
		printRigid()
	else:
		print('This is not a Rigid packet')
else:
	print('Invalid packet')

#Closing:
sleep(0.1)
print('\nDone.\n')
ser.close
