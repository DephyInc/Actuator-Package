"""/*
 * CellScreenerState.py
 *
 * AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
 * CORE:228bd6fc3380919b08a364fd9f852465520f7ad9
 * BUILD:94bbfbbd2d74bba2633ab1956cd8c3135ba1d5b6
 *
 *
 * Specification File Created on: 2020-10-14 16:43:39
 * Author: Dephy, Inc.
 *
 */
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