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
	[This file] flexsea_cmd_stream: commands allowing plan to put execute into a streaming mode
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-03-13 | dudds4 | Initial GPL-3.0 release
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_STREAM_H
#define INC_FLEXSEA_CMD_STREAM_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

void init_flexsea_payload_ptr_stream(void);

void tx_cmd_stream_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t cmdToStream, uint8_t periodInMS, \
						uint8_t startStop, uint8_t firstIndex, uint8_t lastIndex);
void tx_cmd_stream_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len);

void rx_cmd_stream_w(uint8_t *buf, uint8_t *info);
void rx_cmd_stream_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_stream_rr(uint8_t *buf, uint8_t *info);

extern uint8_t isStreaming;

#define MAX_STREAMS 2

extern int streamCmds[MAX_STREAMS];
extern uint16_t streamPeriods[MAX_STREAMS];
extern uint16_t streamReceivers[MAX_STREAMS];
extern uint8_t streamPortInfos[MAX_STREAMS];
extern uint16_t streamIndex[MAX_STREAMS][2];
extern uint8_t streamCurrentOffset[MAX_STREAMS];

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_STREAM_H
