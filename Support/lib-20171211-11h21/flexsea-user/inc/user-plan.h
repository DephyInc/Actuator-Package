/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-plan' GUI
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user: User Projects & Functions
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-07-07 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifdef BOARD_TYPE_FLEXSEA_PLAN

#ifndef INC_USER_PLAN_H
#define INC_USER_PLAN_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "flexsea_board.h"
#include "flexsea_sys_def.h"
#include "flexsea_global_structs.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

//****************************************************************************
// Definition(s):
//****************************************************************************

//List of projects - All 0 for Plan
#define PROJECT_BAREBONE		0	//Barebone Manage, default option.
#define PROJECT_ANKLE_2DOF		0	//Biomechatronics 2-DOF Ankle
#define PROJECT_RICNU_KNEE		0	//RIC/NU Knee
#define PROJECT_MOTORTB			0
#define PROJECT_DEV				0	//Experimental code - use with care
#define PROJECT_CYCLE_TESTER	0	//Automatic Cycle Tester
#define PROJECT_DPEB			0	//DpEb2.1 and below
#define PROJECT_DPEB31			0	//DpEb3.1 Exo
#define PROJECT_ACTPACK			0	//Dephy's Actuator Package

//List of sub-projects:
#define SUBPROJECT_NONE			0
#define SUBPROJECT_A			1
#define SUBPROJECT_B			2
//(ex.: the 2-DoF ankle has 2 Execute. They both use PROJECT_2DOF_ANKLE, and each
// 		of them has a sub-project for specific configs)

//Step 1) Select active project (from list):
//==========================================

#define ACTIVE_PROJECT			0	//Plan has all of them
//#define ACTIVE_PROJECT		PROJECT_DPEB31
#define ACTIVE_SUBPROJECT		SUBPROJECT_A


//****************************************************************************
// Structure(s)
//****************************************************************************


//****************************************************************************
// Shared variable(s)
//****************************************************************************


#endif	//INC_USER_PLAN_H

#endif //BOARD_TYPE_FLEXSEA_PLAN
