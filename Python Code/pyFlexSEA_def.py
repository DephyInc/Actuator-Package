#FlexSEA Stack structures and essential constant definitions

import ctypes
from ctypes import *
from ctypes import cdll
from ctypes import _SimpleCData

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
					("ank_ang_from_mot", POINTER(c_int16)),
					("contra_hs", c_int16),
					("step_energy", c_int16)]

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

#Constants:
FLEXSEA_PLAN_1 = 10
FLEXSEA_MANAGE_1 = 20
FLEXSEA_EXECUTE_1 = 40
COMM_STR_LEN = 48
CTRL_NONE = 0
CTRL_OPEN = 1
CTRL_POSITION = 2
CTRL_CURRENT = 3
CTRL_IMPEDANCE = 4
CTRL_CUSTOM = 5
CTRL_MEASRES = 6
KEEP = 0
CHANGE = 1
