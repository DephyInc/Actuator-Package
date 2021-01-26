"""/*
 * NetMasterState.py
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

class NetMasterState(Structure):
	_pack_ = 1
	_fields_ = [
		("netmaster", c_int),
		("id", c_int),
		("state_time", c_int),
		("genvar_0", c_int),
		("genvar_1", c_int),
		("genvar_2", c_int),
		("genvar_3", c_int),
		("status", c_int),
		("a_accelx", c_int),
		("a_accely", c_int),
		("a_accelz", c_int),
		("a_gyrox", c_int),
		("a_gyroy", c_int),
		("a_gyroz", c_int),
		("a_pressure", c_int),
		("a_status", c_int),
		("b_accelx", c_int),
		("b_accely", c_int),
		("b_accelz", c_int),
		("b_gyrox", c_int),
		("b_gyroy", c_int),
		("b_gyroz", c_int),
		("b_pressure", c_int),
		("b_status", c_int),
		("c_accelx", c_int),
		("c_accely", c_int),
		("c_accelz", c_int),
		("c_gyrox", c_int),
		("c_gyroy", c_int),
		("c_gyroz", c_int),
		("c_pressure", c_int),
		("c_status", c_int),
		("d_accelx", c_int),
		("d_accely", c_int),
		("d_accelz", c_int),
		("d_gyrox", c_int),
		("d_gyroy", c_int),
		("d_gyroz", c_int),
		("d_pressure", c_int),
		("d_status", c_int),
		("e_accelx", c_int),
		("e_accely", c_int),
		("e_accelz", c_int),
		("e_gyrox", c_int),
		("e_gyroy", c_int),
		("e_gyroz", c_int),
		("e_pressure", c_int),
		("e_status", c_int),
		("f_accelx", c_int),
		("f_accely", c_int),
		("f_accelz", c_int),
		("f_gyrox", c_int),
		("f_gyroy", c_int),
		("f_gyroz", c_int),
		("f_pressure", c_int),
		("f_status", c_int),
		("g_accelx", c_int),
		("g_accely", c_int),
		("g_accelz", c_int),
		("g_gyrox", c_int),
		("g_gyroy", c_int),
		("g_gyroz", c_int),
		("g_pressure", c_int),
		("g_status", c_int),
		("h_accelx", c_int),
		("h_accely", c_int),
		("h_accelz", c_int),
		("h_gyrox", c_int),
		("h_gyroy", c_int),
		("h_gyroz", c_int),
		("h_pressure", c_int),
		("h_status", c_int),
		("SystemTime", c_int)]