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
	[This file] flexsea: Master file for the FlexSEA stack.
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_COMM_DEF_H_
#define INC_FLEXSEA_COMM_DEF_H_

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Core features:
//****************************************************************************

//Framing:
#define HEADER  						0xED	//237d
#define FOOTER  						0xEE	//238d
#define ESCAPE  						0xE9	//233d

//Return codes:
#define UNPACK_ERR_HEADER				-1
#define UNPACK_ERR_FOOTER				-2
#define UNPACK_ERR_LEN					-3
#define UNPACK_ERR_CHECKSUM				-4

//Buffers and packets:
#define RX_BUF_LEN						150		//Reception buffer (flexsea_comm)
#define PAYLOAD_BUF_LEN					36		//Number of bytes in a payload string
#define PAYLOAD_BYTES					(PAYLOAD_BUF_LEN - 4)
#define COMM_STR_BUF_LEN				48		//Number of bytes in a comm. string
#define PACKAGED_PAYLOAD_LEN			48		//Temporary
#define PAYLOAD_BUFFERS					4		//Max # of payload strings we expect to find
#define MAX_CMD_CODE					127
#define PACKET_WRAPPER_LEN				RX_BUF_LEN
#define COMM_PERIPH_ARR_LEN				RX_BUF_LEN

//Packet types:
#define RX_PTYPE_READ					0
#define RX_PTYPE_WRITE					1
#define RX_PTYPE_REPLY					2
#define RX_PTYPE_INVALID				3
#define RX_PTYPE_MAX_INDEX				2

//Board ID related defines:
#define ID_MATCH						1		//Addressed to me
#define ID_SUB1_MATCH					2		//Addressed to a board on slave bus #1
#define ID_SUB2_MATCH					3		//Addressed to a board on slave bus #2
#define ID_SUB3_MATCH					4		//Addressed to a board on slave bus #3
#define ID_UP_MATCH						6		//Addressed to my master
#define ID_OTHER_MASTER					7		//Addressed to "a" master (special use case)
#define ID_NO_MATCH						0

#define NUMBER_OF_PORTS					7		//Has to match enum!

//Communication protocol payload fields:
#define P_XID							0		//Emitter ID
#define P_RID							1		//Receiver ID
#define P_CMDS							2		//Number of Commands sent
#define P_CMD1							3		//First command
#define P_DATA1							4		//First data

//Parser definitions:
#define PARSE_DEFAULT					0
#define PARSE_ID_NO_MATCH				1
#define PARSE_SUCCESSFUL				2
#define PARSE_UNKNOWN_CMD				3

#define CMD_READ						1
#define CMD_WRITE						2

#define KEEP							0
#define CHANGE							1

//Read, Write, or Read&Write?
#define WRITE							0
#define READ							1

//Update buffer
#define UPDATE_BYTE						0
#define UPDATE_ARRAY					1

//****************************************************************************
// User implementation:
//****************************************************************************

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_COMM_DEF_H_
