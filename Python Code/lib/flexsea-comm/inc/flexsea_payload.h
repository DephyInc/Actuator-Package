/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-comm' Communication stack
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
	[This file] flexsea_payload: deals with the "intelligent" data packaged
	in a comm_str
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FX_PAYLOAD_H
#define INC_FX_PAYLOAD_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>
#include "flexsea_comm.h"

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern uint8_t payload_str[PAYLOAD_BUF_LEN];

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************
uint8_t payload_parse_str(PacketWrapper* foo);
uint8_t sent_from_a_slave(uint8_t *buf);
uint8_t packetType(uint8_t *buf);
void prepare_empty_payload(uint8_t from, uint8_t to, uint8_t *buf, uint32_t len);
void flexsea_payload_catchall(uint8_t *buf, uint8_t *info);
uint8_t tryUnpacking(CommPeriph *cp, PacketWrapper *pw);
uint8_t tryParseRx(CommPeriph *cp, PacketWrapper *pw);
void getSignatureOfLastPayloadParsed(uint8_t *cmd, uint8_t *type);

//****************************************************************************
// Definition(s):
//****************************************************************************

#ifdef __cplusplus
}
#endif

#endif
