/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'plan-gui' Graphical User Interface
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] cmd_rigid: Rigid Commands
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-04-18 | jfduval | New code
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_RIGID_H
#define INC_FLEXSEA_CMD_RIGID_H

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

void rx_cmd_rigid_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_rigid_rr(uint8_t *buf, uint8_t *info);

void tx_cmd_rigid_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_rigid_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);

//****************************************************************************
// Prototype(s) - simplified functions (DLL):
//****************************************************************************

void ptx_cmd_rigid_r(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
							uint8_t offset);

uint8_t newRigidRRpacketAvailable(void);
void getLastRigidData(struct rigid_s *r);
void init_rigid(void);

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

#endif	//INC_FLEXSEA_CMD_RIGID_H
