/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-system' System commands & functions
	Copyright (C) 2016 Dephy, Inc. <http://dephy.com/>

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
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] flexsea_system: configuration and functions for this
	particular system
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_SYSTEM_H
#define INC_FLEXSEA_SYSTEM_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <flexsea_comm_def.h>
#include "flexsea_sys_def.h"
//Include the core flexsea-system files:
#include "flexsea_global_structs.h"
#include "flexsea_cmd_stream.h"
#include "flexsea_cmd_control.h"
#include "flexsea_cmd_sensors.h"
#include "flexsea_cmd_external.h"
#include "flexsea_cmd_data.h"
#include "flexsea_cmd_tools.h"
#include "flexsea_cmd_in_control.h"
//Include the user files:
#include "flexsea_cmd_user.h"

//****************************************************************************
// Prototype(s):
//****************************************************************************

void init_flexsea_payload_ptr(void);
uint16_t tx_cmd(uint8_t *payloadData, uint8_t cmdCode, uint8_t cmd_type, \
				uint32_t len, uint8_t receiver, uint8_t *buf);
void pack(uint8_t *shBuf, uint8_t cmd, uint8_t cmdType, uint16_t len, \
			uint8_t rid, uint8_t *info, uint16_t *numBytes, uint8_t *commStr);
void packAndSend(uint8_t *shBuf, uint8_t cmd, uint8_t cmdType, uint16_t len, \
				 uint8_t rid, uint8_t *info, uint8_t ms);
void executePtrXid(struct execute_s **myPtr, uint8_t p_xid);
void managePtrXid(struct manage_s **myPtr, uint8_t p_xid);
void gossipPtrXid(struct gossip_s **myPtr, uint8_t p_xid);
void strainPtrXid(struct strain_s **myPtr, uint8_t p_xid);
void flexsea_payload_catchall(uint8_t *buf, uint8_t *info);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Macro(s):
//****************************************************************************

//To simplify user's life, here are two macros:
#define TX_N_DEFAULT		tmpPayload,&cmdCode,&cmdType,&cmdLen
#define P_AND_S_DEFAULT		tmpPayload,cmdCode,cmdType,cmdLen

//****************************************************************************
// Shared variable(s)
//****************************************************************************

//We use this buffer to exchange information between tx_N() and tx_cmd():
extern uint8_t tmpPayload[PAYLOAD_BUF_LEN];	//tx_N() => tx_cmd()
//Similarly, we exchange command code, type and length:
extern uint8_t cmdCode, cmdType;
extern uint16_t cmdLen;

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_SYSTEM_H
