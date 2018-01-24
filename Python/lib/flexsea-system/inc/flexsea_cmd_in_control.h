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
	[This file] flexsea_cmd_in_control: commands specific to the in control module
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	* 2017-02-09 | dudds4 | Extracted in control commands to separate file
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_IN_CONTROL_TOLSH
#define INC_FLEXSEA_CMD_IN_CONTROL_TOLSH

#ifdef __cplusplus
extern "C" {
#endif
//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>

//****************************************************************************
// Prototype(s):
//****************************************************************************

void init_flexsea_payload_ptr_in_control(void);

//In Control Tool:

void tx_cmd_in_control_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t select_w);
void tx_cmd_in_control_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);

void rx_cmd_in_control_w(uint8_t *buf, uint8_t *info);
void rx_cmd_in_control_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_in_control_rr(uint8_t *buf, uint8_t *info);

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_IN_CONTROL_H
