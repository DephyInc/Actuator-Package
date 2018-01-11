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
	[This file] user-ex-DpEb31: User code running on Ex
****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-06-19 | jfduval | Initial release
	*
****************************************************************************/

#ifdef BOARD_TYPE_FLEXSEA_EXECUTE

#ifndef INC_DPEB31_EX_H
#define INC_DPEB31_EX_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void initDpEb31(void);
void DpEb31_fsm(void);
void DpEb31_refresh_values(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#endif	//INC_DPEB31_EX_H

#endif //BOARD_TYPE_FLEXSEA_EXECUTE
