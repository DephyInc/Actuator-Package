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
	[This file] user-mn-MIT-DLeg: Demo state machine for DLeg
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2018-02-24 | jfduval | New release
****************************************************************************/

#ifdef INCLUDE_UPROJ_MIT_DLEG

#include "main.h"

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_MIT_DLEG_H
#define INC_MIT_DLEG_H

//****************************************************************************
// Include(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************



//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_MIT_DLeg(void);
void MIT_DLeg_fsm_1(void);
void MIT_DLeg_fsm_2(void);

//****************************************************************************
// Definition(s):
//****************************************************************************



//****************************************************************************
// Structure(s)
//****************************************************************************

#endif	//INC_MIT_DLEG_H

#endif 	//BOARD_TYPE_FLEXSEA_MANAGE
#endif //INCLUDE_UPROJ_MIT_DLEG
