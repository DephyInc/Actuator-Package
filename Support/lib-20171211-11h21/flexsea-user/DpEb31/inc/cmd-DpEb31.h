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
	[This file] cmd-DpEb31: Custom commands for the Exo v3.1
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_DPEB31_H
#define INC_FLEXSEA_CMD_DPEB31_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include "flexsea_system.h"

//****************************************************************************
// Prototype(s):
//****************************************************************************

void tx_cmd_dpeb31_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
							uint16_t *len, uint8_t offset, uint8_t controller, \
					int32_t setpoint, uint8_t setGains, int16_t g0, int16_t g1,\
					int16_t g2, int16_t g3, uint8_t system);
void tx_cmd_dpeb31_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_dpeb31_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
							uint16_t *len, uint8_t offset);

void rx_cmd_dpeb31_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_dpeb31_rr(uint8_t *buf, uint8_t *info);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_DPEB31_H
