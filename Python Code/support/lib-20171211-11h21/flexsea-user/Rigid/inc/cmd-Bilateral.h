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
	[This file] cmd-Bilateral: Communication between 2 Rigid
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-10-06 | jfduval | New code
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_BILATERAL_H
#define INC_FLEXSEA_CMD_BILATERAL_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>
#include "flexsea_user_structs.h"

//****************************************************************************
// RX/TX Prototype(s):
//****************************************************************************

void rx_cmd_bilateral_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_bilateral_rr(uint8_t *buf, uint8_t *info);

void tx_cmd_bilateral_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_bilateral_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);

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

#endif	//INC_FLEXSEA_CMD_BILATERAL_H
