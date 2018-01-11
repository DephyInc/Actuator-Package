/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'user/DpEb31' Dephy's Exo
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois Duval, jfduval at dephy dot com.
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

#ifndef INC_DPEB31_MN_H
#define INC_DPEB31_MN_H

//****************************************************************************
// Include(s)
//****************************************************************************

//#include "main.h"
#include "exoDef.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_DpEb31(void);
void DpEb31_fsm_1(void);
void DpEb31_fsm_2(void);
void init_current_controller(void);

void setMotorVoltage(int32_t v);
void setMotorCurrent(int32_t i);
void setControlMode(uint8_t m);
void setControlGains(int16_t g0, int16_t g1, int16_t g2);

//****************************************************************************
// Accessor(s)
//****************************************************************************


//****************************************************************************
// Definition(s):
//****************************************************************************

#define DP_FSM2_POWER_ON_DELAY		3500

//****************************************************************************
// Structure(s)
//****************************************************************************

typedef struct {
	uint8_t ctrl;
	int32_t setpoint;
	uint8_t setGains;
	uint8_t offset;
	int16_t g[4];
} writeEx_s;

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern struct ctrl_s ctrl;
extern struct rigid_s dpRigid;
extern int32_t dp_ank_ang_zero;
extern int32_t dp_mot_ang_zero;
extern int32_t mot_ang_offset;
extern int32_t ank_ang_offset;
extern writeEx_s writeEx;

#endif	//INC_DPEB31_MN_H

#endif //BOARD_TYPE_FLEXSEA_EXECUTE
