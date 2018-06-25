/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'user/MIT_2DoF_Ankle' MIT Biomechatronics 2-dof Ankle
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
	[This file] cmd-MIT_2DoF_Ankle: Custom commands for this project
****************************************************************************/

#ifdef INCLUDE_UPROJ_MIT_A2DOF

#ifndef INC_FLEXSEA_CMD_MITA2DOF_H
#define INC_FLEXSEA_CMD_MITA2DOF_H

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

void tx_cmd_ankle2dof_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
							uint16_t *len, uint8_t slave);
void tx_cmd_ankle2dof_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
							uint16_t *len, uint8_t slave, uint8_t controller, \
							int16_t ctrl_i, int16_t ctrl_o);
void rx_cmd_ankle2dof_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_ankle2dof_rr(uint8_t *buf, uint8_t *info);

/*
uint32_t tx_cmd_ctrl_special_5(uint8_t receiver, uint8_t cmd_type, uint8_t *buf, uint32_t len, \
								uint8_t slave, uint8_t controller, int16_t ctrl_i, int16_t ctrl_o);
void rx_cmd_special_5(uint8_t *buf);
*/

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

#endif	//INC_FLEXSEA_CMD_MITA2DOF_H
#endif //INCLUDE_UPROJ_MIT_A2DOF
