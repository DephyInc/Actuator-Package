/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'user/DpEb31' Dephy's Exo
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Luke Mooney, lmooney at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user-mn-DpEb31: User code running on Mn
****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-06-19 | jfduval | Initial release
	*
****************************************************************************/

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_WALKING_CONTROLLER_H
#define INC_WALKING_CONTROLLER_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"
#include "exoDef.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void initWalkingController(void);
void walkingControllerFSM(void);
void refreshValues(void);

void rwTestFSM1(void);
void rwTestFSM2(void);

//****************************************************************************
// Accessor(s)
//****************************************************************************

int64_t get_st(void);
int32_t get_mot_ang(void);
int32_t get_mot_vel(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern int32_t ank_ang_comp;
extern int32_t mot_from_ank_ang;

#endif	//INC_WALKING_CONTROLLER_H

#endif //BOARD_TYPE_FLEXSEA_EXECUTE
