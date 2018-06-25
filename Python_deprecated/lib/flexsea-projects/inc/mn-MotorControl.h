/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-manage' Mid-level computing, and networking
	Copyright (C) 2018 Dephy, Inc. <http://dephy.com/>

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
	[This file] mn-MotorControl: Wrappers for motor control functions on Mn
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2018-05-22 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_MN_MOTOR_CONTROL_H
#define INC_MN_MOTOR_CONTROL_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"
#include "flexsea_board.h"
#include "flexsea_sys_def.h"
#include "flexsea_global_structs.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void initWriteEx(uint8_t ch);
void init_current_controller(uint8_t ch);
void init_position_controller(uint8_t ch);
void setMotorVoltage(int32_t v, uint8_t ch);
void setMotorCurrent(int32_t i, uint8_t ch);
void setControlMode(uint8_t m, uint8_t ch);
void setControlGains(int16_t g0, int16_t g1, int16_t g2, int16_t g3, uint8_t ch);
void setMotorPosition(int32_t i, uint8_t ch);

//****************************************************************************
// Definition(s):
//****************************************************************************

//Default:
#define CTRL_I_KP					100
#define CTRL_I_KI					20
#define CTRL_P_KP					200

//****************************************************************************
// Structure(s)
//****************************************************************************

typedef struct {
	uint8_t ctrl;
	int32_t setpoint;
	uint8_t setGains;
	uint8_t offset;
	int16_t g[4];
} writeEx_s;

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern struct ctrl_s ctrl[];
extern writeEx_s writeEx[];

#endif	//INC_MN_MOTOR_CONTROL_H

#endif //BOARD_TYPE_FLEXSEA_MANAGE
