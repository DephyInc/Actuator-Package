/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User-specific code
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] cmd-CycleTester: Cycle Tester Commands
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-06-08 | jfduval | New code
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_CYCLE_TESTER_H
#define INC_FLEXSEA_CMD_CYCLE_TESTER_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>

//****************************************************************************
// Prototype(s):
//****************************************************************************

void rx_cmd_cycle_tester_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_cycle_tester_rr(uint8_t *buf, uint8_t *info);
void rx_cmd_cycle_tester_w(uint8_t *buf, uint8_t *info);

void tx_cmd_cycle_tester_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);

void tx_cmd_cycle_tester_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset, uint8_t action1, \
					uint8_t action2, uint8_t action3);

//****************************************************************************
// Definition(s):
//****************************************************************************

//Errors:
#define CT_ERR_MEM			2
#define CT_ERR_TEMP_WARN	4
#define CT_ERR_TEMP			8
#define CT_ERR_MOTION		16
#define CT_ERR_STUCK		32
#define CT_ERR_CORD			64

//Arrays:
#define CT_IDX_VALLEY		0
#define CT_IDX_PEAK			1

//****************************************************************************
// Structure(s):
//****************************************************************************

enum expCtrl
{
	CT_C_DEFAULT = 0,
	CT_C_INIT,
	CT_C_START,
	CT_C_PAUSE,
	CT_C_STOP
};

enum expStats
{
	CT_S_DEFAULT = 0,
	CT_S_READ,
	CT_S_START_STREAMING,
	CT_S_RESET,
	CT_S_CONFIRM_RESET
};

//****************************************************************************
// Shared variable(s)
//****************************************************************************

//Stats & display:
extern uint8_t ctStats_fsm1State, ctStats_pct, ctStats_errorMsg, ctStats_temp;
extern int8_t ctStats_mod1, ctStats_mod2;
extern uint32_t cyclesVolatile;
extern uint16_t cyclesNonVolatile;
extern uint16_t peakCurrent, valleyCurrent;
extern int32_t instantPower;
extern int16_t cyclePower;
extern int16_t peakPower;
extern uint16_t rms, i2r;

//Profiles:
extern uint16_t peakCurrentTarget;
extern uint16_t valleyCurrentTarget;
extern uint16_t ctNewProfileYT[2][5];
extern uint16_t ctNewProfileCurr[2];
extern uint16_t ctProfileInUseYT[2][5];
extern uint16_t ctProfileInUseCurr[2];

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_CYCLE_TESTER_H
