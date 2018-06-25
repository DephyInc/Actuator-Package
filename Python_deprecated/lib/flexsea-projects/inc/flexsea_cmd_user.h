/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' System commands & functions specific to
	user projects
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
	[This file] flexsea_cmd_user: Interface to the user functions
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_USER_H
#define INC_FLEXSEA_CMD_USER_H

#ifdef __cplusplus
extern "C" {
#endif


//****************************************************************************
// Include(s)
//****************************************************************************

//****************************************************************************
// Prototype(s):
//****************************************************************************

void init_flexsea_payload_ptr_user(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//Give nickname to function codes here. Always remember that they have to be
//in the 100-127 range!

#define CMD_A2DOF					100
#define CMD_RICNU					101
#define CMD_MOTORTB					103
#define CMD_ANGLE_TORQUE_PROFILE	104
#define CMD_CYCLE_TESTER			105
#define CMD_DPEB31					106
#define CMD_DPEB42					CMD_DPEB31
#define CMD_UTT						107
#define CMD_GAITSTATS				108

#define CMD_READ_ALL_POCKET			119
#define CMD_READ_ALL_RIGID			120
#define CMD_ACTPACK					121
#define CMD_BILATERAL				125
#define CMD_USER_DYNAMIC 			126

//***************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_USER_H
