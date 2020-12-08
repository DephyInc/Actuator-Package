"""/*
 * NetNodeState.py
 *
 * AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
 * CORE:228bd6fc3380919b08a364fd9f852465520f7ad9
 * BUILD:94bbfbbd2d74bba2633ab1956cd8c3135ba1d5b6
 *
 *
 * Specification File Created on: 2020-06-22 14:42:45
 * Author: Dephy, Inc.
 *
 */
"""
from ctypes import Structure, c_int

class NetNodeState(Structure):
	_pack_ = 1
	_fields_ = [
		("netnode", c_int),
		("id", c_int),
		("state_time", c_int),
		("genvar_0", c_int),
		("genvar_1", c_int),
		("genvar_2", c_int),
		("genvar_3", c_int),
		("status", c_int),
		("SystemTime", c_int)]