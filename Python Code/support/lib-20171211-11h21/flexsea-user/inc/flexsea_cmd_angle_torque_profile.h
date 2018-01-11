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
	[This file] flexsea_cmd_angle_torque_profile: commands specific to the angle-torque profile that exo tries to achieve
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-04-04 | dweisdorf | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_ANKLE_TORQUE_H
#define INC_FLEXSEA_CMD_ANKLE_TORQUE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Module variables
extern const int ANKLE_TORQUE_MODULE_NUM_POINTS;
extern int16_t *atProfile_torques;
extern int16_t *atProfile_angles;
extern int16_t *torqueBuf;
extern int16_t *angleBuf;
extern int indexOfLastBuffered;

extern uint8_t atProfile_newProfileFlag;
extern uint8_t atProfile_newDataFlag;

void init_flexsea_payload_ptr_ankleTorqueProfile(void);

void tx_cmd_ankleTorqueProfile_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, uint16_t *len, uint8_t requestProfile);
void tx_cmd_ankleTorqueProfile_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, uint16_t *len);

void rx_cmd_ankleTorqueProfile_rr(uint8_t *buf, uint8_t *info);
void rx_cmd_ankleTorqueProfile_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ankleTorqueProfile_r(uint8_t *buf, uint8_t *info);

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_ANKLE_TORQUE_H


