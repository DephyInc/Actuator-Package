/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Luke Mooney, lmooney at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab 
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] exo-angles: motor & ankle angle
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-06-22 | jfduval | New release
****************************************************************************/

#ifndef INC_EXO_ANGLES_H
#define INC_EXO_ANGLES_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void initAnk2MotArrays(void);
int mot_ank_ang_cal_fsm(void);
int get_mot_from_ank(int32_t);
int get_ank_from_mot(int32_t);

//****************************************************************************
// Definition(s):
//****************************************************************************


//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************



#endif //INC_EXO_ANGLES_H
