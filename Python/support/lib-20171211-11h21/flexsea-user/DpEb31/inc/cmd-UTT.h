/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User functions
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] cmd-UTT: DpEb3.1 User Testing Tweaks
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-10-10 | jfduval | New code
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_UTT_H
#define INC_FLEXSEA_CMD_UTT_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>
#include "flexsea_user_structs.h"

//****************************************************************************
// Prototype(s):
//****************************************************************************

void init_utt(void);
uint32_t compTorqueX(struct dual_utt_s *wutt, uint8_t leg);
void decompTorqueX(struct dual_utt_s *wutt, uint8_t leg, uint32_t tp);

//****************************************************************************
// RX/TX Prototype(s):
//****************************************************************************

void rx_cmd_utt_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_utt_rr(uint8_t *buf, uint8_t *info);
void rx_cmd_utt_w(uint8_t *buf, uint8_t *info);

void tx_cmd_utt_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_utt_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset, struct dual_utt_s *wutt);

//****************************************************************************
// Definition(s):
//****************************************************************************

#define UTT_RIGHT	0
#define UTT_LEFT	1
#define UTT_DUAL	2

//****************************************************************************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern uint8_t sendTweaksToSlave;

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_UTT_H
