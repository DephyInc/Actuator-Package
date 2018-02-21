/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Luke Mooney, lmooney at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors] Jean-Francois Duval, Elliott Rouse
*****************************************************************************
	[This file] user-mn-Rigid: FlexSEA-Rigid Manage user code
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-05-24 | jfduval | New file
	*
****************************************************************************/

#include "main.h"

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_USER_RIGID_H
#define INC_USER_RIGID_H

//****************************************************************************
// Include(s)
//****************************************************************************


//****************************************************************************
// Shared variable(s)
//****************************************************************************

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void rigid_fsm_1(void);
void rigid_fsm_2(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

#define RIGID_FSM2_POWER_ON_DELAY		5000

//****************************************************************************
// Structure(s)
//****************************************************************************

#endif	//INC_USER_RIGID_H

#endif //BOARD_TYPE_FLEXSEA_MANAGE
