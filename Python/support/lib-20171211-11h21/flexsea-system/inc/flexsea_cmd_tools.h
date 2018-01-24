/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-system' System commands & functions
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>

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
	[This file] flexsea_cmd_tools: Tools used to support FlexSEA's
	developpment and usage.
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-1-05 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_TOOLS_H
#define INC_FLEXSEA_CMD_TOOLS_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>

//****************************************************************************
// Prototype(s):
//****************************************************************************

void init_flexsea_payload_ptr_tools(void);

//Communication tests:
void tx_cmd_tools_comm_test_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t offset, uint8_t randomArrayLen, \
						uint8_t packetNum, uint8_t reply);
void tx_cmd_tools_comm_test_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t offset, uint8_t randomArrayLen, \
						uint8_t packetNum);
void rx_cmd_tools_comm_test_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_tools_comm_test_w(uint8_t *buf, uint8_t *info);
void rx_cmd_tools_comm_test_rr(uint8_t *buf, uint8_t *info);

//Simplified functions:
void ptx_cmd_tools_comm_test_w(	uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
								uint8_t offset, uint8_t randomArrayLen, \
								uint8_t packetNum, uint8_t reply);

//****************************************************************************
// Definition(s):
//****************************************************************************

#define MAX_PACKETS_BEHIND 		10

//****************************************************************************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern int32_t sentPackets, goodPackets, badPackets;
extern uint8_t lastTxPacketIndex, lastRxPacketIndex;
extern uint8_t packetOffset;

#endif	//INC_FLEXSEA_CMD_TOOLS_H
