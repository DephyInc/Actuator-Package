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

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_USER_CYCLE_TESTER_H
#define INC_USER_CYCLE_TESTER_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_cycle_tester(void);
void cycle_tester_fsm_1(void);
void cycle_tester_fsm_2(void);
void cycle_tester_setAction(uint8_t act1, uint8_t act2, uint8_t act3);

//****************************************************************************
// Definition(s):
//****************************************************************************

#define CT_FSM2_POWER_ON_DELAY		5000

//Position:
#define CT_P_KP						250
#define CT_P_KI						25
#define CT_P_KD						0

enum fsm1State
{
	CT_FSM1_BOOT = 0,
	CT_FSM1_INIT_CTRL0,
	CT_FSM1_INIT_CTRL1,
	CT_FSM1_INIT_ERROR,
	CT_FSM1_INIT_CTRL2,
	CT_FSM1_CYCLE,
	CT_FSM1_PAUSE,
	CT_FSM1_STOP,
	CT_FSM1_ERROR
};

//Experimental settings:
#define CT_POS_CNT					5
#define CT_MAX_Y					3000	//Starting point - will get modified
#define CT_MIN_Y					0		//Starting point - will get modified
#define CT_PRO_T0					0
#define CT_PRO_Y0					CT_MIN_Y
#define CT_PRO_T1					400
#define CT_PRO_Y1					CT_MIN_Y
#define CT_PRO_T2					650
#define CT_PRO_Y2					CT_MAX_Y
#define CT_PRO_T3					725
#define CT_PRO_Y3					CT_MAX_Y
#define CT_PRO_T4					1100
#define CT_PRO_Y4					CT_MIN_Y
#define PLATEAU_LEN					(CT_PRO_T3-CT_PRO_T2)
#define PEAK_CURRENT_TARGET			10000
#define VALLEY_CURRENT_TARGET		1000

//We increment the count by 1 every EEPROM_CYCLE_DIV cycles
#define EEPROM_CYCLE_DIV			1000

#define OPEN_REEL					500				//Motor voltage, mV
#define MOD_STEP					45				//Encoder ticks
#define POS_CALIB_SPAN				7500			//Encoder ticks
#define CURR_ARRAY_LEN				16

//Safety limits:
#define CT_LIM_DELTA_POS_POS		30000			//Maximum positive travel
#define CT_LIM_DELTA_POS_NEG		5000			//Maximum negative travel
#define CT_LIM_MIN_MOTION			100				//Minimum amount of motion required
#define CT_LIM_TEMP_WARN			55
#define CT_LIM_TEMP_ERROR			70
#define CT_LIM_MIN_CURRENT			1000
#define CT_LIM_CTRL1_TIME			20000

//Calibration: map control space.
#define MAP_OPEN_CTRL_G				2				//V/s (later div by 2)
#define MAP_HOLD_DELAY				200				//ms
#define MAP_CURRENT_DIFF_MIN		2000			//mA
#define MAP_CURRENT_DIFF_MAX		5000			//mA
#define MAP_MAX_OPEN				35000			//mV

#define MOTOR_RESISTANCE 			0.186

//****************************************************************************
// Structure(s)
//****************************************************************************

struct pt_s
{
	uint32_t t;
	int32_t y;
};

struct profile_s
{
	int32_t floor;
	int32_t ceiling;
	struct pt_s pro[CT_POS_CNT];
	struct pt_s pt[CT_POS_CNT];
	int32_t length[CT_POS_CNT-1];
	int32_t height[CT_POS_CNT-1];
};

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern struct profile_s ctProfile;

#endif	//INC_USER_CYCLE_TESTER_H

#endif //BOARD_TYPE_FLEXSEA_MANAGE
