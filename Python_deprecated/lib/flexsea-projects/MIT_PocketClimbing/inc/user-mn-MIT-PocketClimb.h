/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-projects' User projects
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
	[Lead developer] Jean-Francois Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user-mn-MIT-PocketClimb: Demo state machine for Pocket 2x DC
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2018-03-02 | jfduval | New release
****************************************************************************/

#ifdef INCLUDE_UPROJ_MIT_POCKET_CLIMB

#include "main.h"

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_MIT_POCKET_CLIMB_H
#define INC_MIT_POCKET_CLIMB_H

//****************************************************************************
// Include(s)
//****************************************************************************


//****************************************************************************
// Shared variable(s)
//****************************************************************************



//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_MIT_PocketClimb(void);
void MIT_PocketClimb_fsm_1(void);
void MIT_PocketClimb_fsm_2(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

#define LEFT_MOTOR				0
#define RIGHT_MOTOR				1
#define OPEN_PWM_DEMO_HIGH		200	//Range: -500 to +500 (PWM duty cycle)
#define FORCE_GAIN				10	//pwm = ticks / gain => 5000 = max PWM

//****************************************************************************
// Structure(s)
//****************************************************************************

#endif	//INC_MIT_POCKET_CLIMB_H

#endif 	//BOARD_TYPE_FLEXSEA_MANAGE
#endif //INCLUDE_UPROJ_MIT_POCKET_CLIMB
