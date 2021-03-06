"""/*
 * NetNodeState.py
 *
 * AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
 * CORE:ecdab88c05df58d9ba18cb5e4d6e41c2f32b3e85
 * BUILD:065ba7c027caf247c3a01011370de5bc31a467f7
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
