"""
///
/// @file MD12State.py
///
/// @brief AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
///
/// @core c4674f111fc72bad86b69ef5e7f862f75f59d86f
///
/// @build 6a54779ef7f5d112e58f4877e4667f33623592a3
///
/// @date 2023-02-23 14:31:03
///
/// @author Dephy, Inc.
"""
from ctypes import Structure, c_int

class MD12State(Structure):
    _pack_ = 1
    _fields_ = [
        ("device_family", c_int),
        ("variable_label", c_int),
        ("include files:", c_int),
        ("state_time", c_int),
        ("accelx", c_int),
        ("accely", c_int),
        ("accelz", c_int),
        ("gyrox", c_int),
        ("gyroy", c_int),
        ("gyroz", c_int),
        ("mot_ang", c_int),
        ("mot_vel", c_int),
        ("mot_acc", c_int),
        ("mot_cur", c_int),
        ("mot_volt", c_int),
        ("batt_volt", c_int),
        ("batt_curr", c_int),
        ("temperature", c_int),
        ("status_mn", c_int),
        ("status_ex", c_int),
        ("status_re", c_int),
        ("genvar_0", c_int),
        ("genvar_1", c_int),
        ("genvar_2", c_int),
        ("genvar_3", c_int),
        ("genvar_4", c_int),
        ("genvar_5", c_int),
        ("genvar_6", c_int),
        ("genvar_7", c_int),
        ("genvar_8", c_int),
        ("genvar_9", c_int),
        ("genvar_10", c_int),
        ("genvar_11", c_int),
        ("genvar_12", c_int),
        ("genvar_13", c_int),
        ("genvar_14", c_int),
        ("ank_ang", c_int),
        ("ank_vel", c_int),
        ("shank_ang", c_int),
        ("shank_vel", c_int),
        ("global_shank_ang", c_int),
        ("ank_pos_x", c_int),
        ("ank_pos_y", c_int),
        ("ank_pos_z", c_int),
        ("ank_linear_vel_x", c_int),
        ("ank_linear_vel_y", c_int),
        ("ank_linear_vel_z", c_int),
        ("mot_from_ank", c_int),
        ("ank_from_mot", c_int),
        ("trans_ratio", c_int),
        ("ank_torque", c_int),
        ("exo_step_power", c_int),
        ("step_count", c_int),
        ("step_time", c_int),
        ("gait_state", c_int),
        ("intermediate_state", c_int),
        ("movement", c_int),
        ("toe_whip", c_int),
        ("SystemTime", c_int)]
