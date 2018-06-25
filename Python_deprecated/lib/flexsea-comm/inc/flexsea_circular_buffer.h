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
	[This file] flexsea_circular_buffer.c: simple circular buffer implementation
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-03-21 | dudds4 | Initial GPL-3.0 release
****************************************************************************/

#ifndef FLEXSEA_CIRCULAR_BUFFER_H
#define FLEXSEA_CIRCULAR_BUFFER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <flexsea_comm_def.h>
#include <stdint.h>

#define CB_BUF_LEN (RX_BUF_LEN)

typedef struct circularBuffer {
	uint8_t bytes[CB_BUF_LEN];
	int head;
	int tail;
	int size;
} circularBuffer_t;

// Basic Circular Buffer Operations
void circ_buff_init(circularBuffer_t* cb);
int circ_buff_write(circularBuffer_t* cb, uint8_t *writeFrom, uint16_t len);
int circ_buff_read(circularBuffer_t* cb, uint8_t* readInto, uint16_t numBytes);
int circ_buff_read_section(circularBuffer_t* cb, uint8_t* readInto, uint16_t start, uint16_t numBytes);
int circ_buff_move_head(circularBuffer_t* cb, uint16_t numBytes);
int circ_buff_get_size(circularBuffer_t* cb);
int circ_buff_get_space(circularBuffer_t* cb);

// Convenience Operations for Parsing Buffer Data
uint8_t circ_buff_peak(circularBuffer_t* cb, uint16_t offset);
int32_t circ_buff_search(circularBuffer_t* cb, uint8_t value, uint16_t start);
uint8_t circ_buff_checksum(circularBuffer_t* cb, uint16_t start, uint16_t end);

#ifdef __cplusplus
}
#endif

#endif //FLEXSEA_CIRCULAR_BUFFER_H
