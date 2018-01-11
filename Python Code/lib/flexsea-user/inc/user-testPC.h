//Use this file to test on a PC, outside of the Plan project. It's currently only
//used by DephyInc/commTest.

#ifdef TEST_PC

#ifndef INC_USER_TEST_PC_H
#define INC_USER_TEST_PC_H

//****************************************************************************
// Include(s)
//****************************************************************************

//#include "main.h"
#include "flexsea_board.h"
#include "flexsea_sys_def.h"
#include "flexsea_global_structs.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

/*
void init_user(void);
void user_fsm_1(void);
void user_fsm_2(void);
*/

//****************************************************************************
// Definition(s):
//****************************************************************************

/*
//List of projects - All 0 for Plan
#define PROJECT_BAREBONE		0	//Barebone Manage, default option.
#define PROJECT_ANKLE_2DOF		0	//Biomechatronics 2-DOF Ankle
#define PROJECT_RICNU_KNEE		0	//RIC/NU Knee
#define PROJECT_MOTORTB			0
#define PROJECT_DEV				0	//Experimental code - use with care
#define PROJECT_CYCLE_TESTER	0	//Automatic Cycle Tester
#define PROJECT_DPEB			0	//DpEb2.1 and below
#define PROJECT_DPEB31			0	//DpEb3.1 Exo
*/

//List of sub-projects:
#define SUBPROJECT_NONE			0
#define SUBPROJECT_A			1
#define SUBPROJECT_B			2
//(ex.: the 2-DoF ankle has 2 Execute. They both use PROJECT_2DOF_ANKLE, and each
// 		of them has a sub-project for specific configs)

//Step 1) Select active project (from list):
//==========================================

#define ACTIVE_PROJECT			99
#define ACTIVE_SUBPROJECT		SUBPROJECT_NONE


//****************************************************************************
// Structure(s)
//****************************************************************************


//****************************************************************************
// Shared variable(s)
//****************************************************************************


#endif	//INC_USER_TEST_PC_H

#endif //TEST_PC
