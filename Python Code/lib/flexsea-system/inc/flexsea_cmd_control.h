/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-system' System commands & functions
	Copyright (C) 2016 Dephy, Inc. <http://dephy.com/>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] flexsea_cmd_control: commands specific to the motor & control
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_CONTROL_H
#define INC_FLEXSEA_CMD_CONTROL_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>

//****************************************************************************
// Prototype(s):
//****************************************************************************

void init_flexsea_payload_ptr_control_1(void);
void init_flexsea_payload_ptr_control_2(void);

//Control mode:
void tx_cmd_ctrl_mode_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);
void tx_cmd_ctrl_mode_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t ctrlMode);
void rx_cmd_ctrl_mode_rr(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_mode_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_mode_w(uint8_t *buf, uint8_t *info);

//Current setpoint:
void tx_cmd_ctrl_i_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);
void tx_cmd_ctrl_i_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, int32_t currentSetpoint);
void rx_cmd_ctrl_i_rr(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_i_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_i_w(uint8_t *buf, uint8_t *info);

//Open setpoint:
void tx_cmd_ctrl_o_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);
void tx_cmd_ctrl_o_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, int32_t setpoint);
void rx_cmd_ctrl_o_rr(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_o_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_o_w(uint8_t *buf, uint8_t *info);

//Position setpoint:
void tx_cmd_ctrl_p_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, int32_t pos, int32_t posi, int32_t posf,\
						int32_t spdm, int32_t acc);
void tx_cmd_ctrl_p_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);
void rx_cmd_ctrl_p_w(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_p_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_p_rr(uint8_t *buf, uint8_t *info);

//Current gain:

void tx_cmd_ctrl_i_g_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, int16_t kp, int16_t ki, int16_t kd);
void tx_cmd_ctrl_i_g_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);

void rx_cmd_ctrl_i_g_w(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_i_g_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_i_g_rr(uint8_t *buf, uint8_t *info);

//Position gain:

void tx_cmd_ctrl_p_g_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, int16_t kp, int16_t ki, int16_t kd);
void tx_cmd_ctrl_p_g_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);
void rx_cmd_ctrl_p_g_w(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_p_g_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_p_g_rr(uint8_t *buf, uint8_t *info);

//Impedance gain:

void tx_cmd_ctrl_z_g_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, int16_t zk, int16_t zb, int16_t zi);
void tx_cmd_ctrl_z_g_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);
void rx_cmd_ctrl_z_g_w(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_z_g_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ctrl_z_g_rr(uint8_t *buf, uint8_t *info);

//****************************************************************************
// Prototype(s) - simplified functions (DLL):
//****************************************************************************

void ptx_cmd_ctrl_mode_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
							uint8_t ctrlMode);
void ptx_cmd_ctrl_o_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
						int32_t setpoint);
void ptx_cmd_ctrl_i_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
						int32_t currentSetpoint);
void ptx_cmd_ctrl_p_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
						int32_t pos, int32_t posi, int32_t posf,\
						int32_t spdm, int32_t acc);
void ptx_cmd_ctrl_i_g_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
							int16_t kp, int16_t ki, int16_t kd);
void ptx_cmd_ctrl_p_g_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
						int16_t kp, int16_t ki, int16_t kd);
void ptx_cmd_ctrl_z_g_w(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
						int16_t zk, int16_t zb, int16_t zi);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#endif	//INC_FLEXSEA_CMD_CONTROL_H
