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
	[This file] flexsea_comm: Data-Link layer of the FlexSEA protocol
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FX_COMM_H
#define INC_FX_COMM_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include "flexsea.h"
#include "flexsea_buffers.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

uint8_t comm_gen_str(uint8_t payload[], uint8_t *cstr, uint8_t bytes);
int8_t unpack_payload(uint8_t *buf, uint8_t *packed, uint8_t rx_cmd[PACKAGED_PAYLOAD_LEN]);
uint16_t unpack_payload_cb(circularBuffer_t *cb, uint8_t *packed, uint8_t rx_cmd[PACKAGED_PAYLOAD_LEN]);

/*
int8_t unpack_payload_1(void);
int8_t unpack_payload_2(void);
int8_t unpack_payload_3(void);
int8_t unpack_payload_4(void);
int8_t unpack_payload_5(void);
int8_t unpack_payload_6(void);
*/

//int8_t unpack_payload_test(uint8_t *buf, uint8_t *packed, uint8_t rx_cmd[PACKAGED_PAYLOAD_LEN]);

//Random numbers and arrays:
void initRandomGenerator(int seed);
uint8_t generateRandomUint8_t(void);
void generateRandomUint8_tArray(uint8_t *arr, uint8_t size);

void fillPacketFromCommPeriph(CommPeriph *cp, PacketWrapper *pw);
void copyPacket(PacketWrapper *from, PacketWrapper *to, TravelDirection td);
void initCommPeriph(CommPeriph *cp, Port port, PortType pt, uint8_t *input, \
					uint8_t *unpacked, uint8_t *packed, circularBuffer_t* rx_cb, \
					PacketWrapper *inbound, PacketWrapper *outbound);
void linkCommPeriphPacketWrappers(CommPeriph *cp, PacketWrapper *inbound, \
					PacketWrapper *outbound);

//****************************************************************************
// Definition(s):
//****************************************************************************

//Enable this to debug with the terminal:
//#define DEBUG_COMM_PRINTF_

//Conditional printf() statement:
#ifdef DEBUG_COMM_PRINTF_
	#define DEBUG_COMM_PRINTF(...) printf(__VA_ARGS__)
#else
	#define DEBUG_COMM_PRINTF(...) do {} while (0)
#endif	//DEBUG_COMM_PRINTF_

//****************************************************************************
// Structure(s):
//****************************************************************************

//Communication test tools:
struct commSpy_s
{
	uint8_t counter;
	uint8_t bytes;
	uint8_t total_bytes;
	uint8_t escapes;
	uint8_t checksum;
	uint8_t retVal;
	uint8_t error;
};

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern uint8_t comm_str_tmp[COMM_STR_BUF_LEN];

extern uint8_t comm_str_1[COMM_PERIPH_ARR_LEN];
extern uint8_t rx_command_1[COMM_PERIPH_ARR_LEN];
extern uint8_t comm_str_2[COMM_PERIPH_ARR_LEN];
extern uint8_t rx_command_2[COMM_PERIPH_ARR_LEN];
extern uint8_t comm_str_3[COMM_PERIPH_ARR_LEN];
extern uint8_t rx_command_3[COMM_PERIPH_ARR_LEN];
extern uint8_t comm_str_4[COMM_PERIPH_ARR_LEN];
extern uint8_t rx_command_4[COMM_PERIPH_ARR_LEN];
extern uint8_t comm_str_5[COMM_PERIPH_ARR_LEN];
extern uint8_t rx_command_5[COMM_PERIPH_ARR_LEN];
extern uint8_t comm_str_6[COMM_PERIPH_ARR_LEN];
extern uint8_t rx_command_6[COMM_PERIPH_ARR_LEN];

extern PacketWrapper packet[NUMBER_OF_PORTS][2];
extern CommPeriph commPeriph[NUMBER_OF_PORTS];

extern struct commSpy_s commSpy1;

#ifdef __cplusplus
}
#endif

#endif	//INC_FX_COMM_H
