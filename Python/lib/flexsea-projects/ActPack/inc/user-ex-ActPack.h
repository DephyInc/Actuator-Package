/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'user/ActPack' Dephy's Actuator Package (ActPack)
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Luke Mooney, lmooney at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user-ex-ActPack: User code running on Ex
****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-09-27 | jfduval | Initial release
	*
****************************************************************************/

#ifdef INCLUDE_UPROJ_ACTPACK
#ifdef BOARD_TYPE_FLEXSEA_EXECUTE

#ifndef INC_ACTPACK_EX_H
#define INC_ACTPACK_EX_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void initActPack(void);
void ActPack_fsm(void);
void ActPack_refresh_values(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#endif	//INC_ACTPACK_EX_H

#endif //BOARD_TYPE_FLEXSEA_EXECUTE
#endif //INCLUDE_UPROJ_ACTPACK
