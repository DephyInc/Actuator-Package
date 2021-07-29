"""
///
/// @file CellScreenerState.py
///
/// @brief AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
///
/// @core c5e60a9b936218bf28732038398d20790a7e43c4
///
/// @build 6fe6c6d940447fd3d97f371713be0ccbc5a692c8
///
/// @date 2020-10-14 16:43:39
///
/// @author Dephy, Inc.
"""
from ctypes import Structure, c_int

class CellScreenerState(Structure):
	_pack_ = 1
	_fields_ = [
		("cellscreener", c_int),
		("id", c_int),
		("state_time", c_int),
		("current", c_int),
		("voltage", c_int),
		("fsm_state", c_int),
		("button", c_int),
		("leds", c_int),
		("genvar_0", c_int),
		("genvar_1", c_int),
		("genvar_2", c_int),
		("genvar_3", c_int),
		("status", c_int),
		("p_timestamp", c_int),
		("p_current", c_int),
		("p_open_voltage", c_int),
		("p_voltage", c_int),
		("p_dv", c_int),
		("p_esr", c_int),
		("p_bin", c_int),
		("SystemTime", c_int)]
