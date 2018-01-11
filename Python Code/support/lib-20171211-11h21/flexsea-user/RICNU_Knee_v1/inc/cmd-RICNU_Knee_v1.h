/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'user/RICNU_Knee_v1' RIC/NU Knee
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
	[This file] cmd-RICNU_Knee_v1: Custom commands for this project
****************************************************************************/

#ifdef INCLUDE_UPROJ_RICNU_KNEE_V1

#ifndef INC_FLEXSEA_CMD_RICNU_KNEE_1_H
#define INC_FLEXSEA_CMD_RICNU_KNEE_1_H

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

void rx_cmd_ricnu_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ricnu_w(uint8_t *buf, uint8_t *info);
void rx_cmd_ricnu_rr(uint8_t *buf, uint8_t *info);

void tx_cmd_ricnu_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset, uint8_t controller, \
					int32_t setpoint, uint8_t setGains, int16_t g0, int16_t g1,\
					int16_t g2, int16_t g3);
void tx_cmd_ricnu_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_ricnu_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);

//Decoding:
void rx_cmd_ricnu_Action1(uint8_t controller, int32_t setpoint, uint8_t setGains,
						int16_t g0,	int16_t g1,	int16_t g2, int16_t g3);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_RICNU_KNEE_1_H
#endif //INCLUDE_UPROJ_RICNU_KNEE_V1
