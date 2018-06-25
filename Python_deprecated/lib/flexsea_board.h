/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'plan-gui' Graphical User Interface
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
	[This file] flexsea_board: configuration and functions for this
	particular board
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_BOARD_H
#define INC_FLEXSEA_BOARD_H

#ifdef __cplusplus
extern "C" {
#endif

// Although it's a part of the FlexSEA stack that file doesn't live in
// flexsea-comm or flexsea-system, as it needs to be unique to each board.

//****************************************************************************
// Definition(s):
//****************************************************************************

#ifdef BUILD_SHARED_LIB_DLL

//Enabled the required FlexSEA Buffers for this board:
#define ENABLE_FLEXSEA_BUF_1        //USB
#define ENABLE_FLEXSEA_BUF_2        //SPI
//#define ENABLE_FLEXSEA_BUF_3      //
//#define ENABLE_FLEXSEA_BUF_4      //
//#define ENABLE_FLEXSEA_BUF_5      //

#endif	//BUILD_SHARED_LIB_DLL

//****************************************************************************
// Include(s)
//****************************************************************************

#ifdef BUILD_SHARED_LIB_DLL
#include <stdint.h>
#include "../flexsea-comm/inc/flexsea_comm.h"
//#include "../flexsea-comm/inc/flexsea.h"
#endif	//BUILD_SHARED_LIB_DLL

//****************************************************************************
// Prototype(s):
//****************************************************************************

void flexsea_send_serial_slave(PacketWrapper* p);
void flexsea_send_serial_master(PacketWrapper* p);

#ifdef BUILD_SHARED_LIB_DLL
uint8_t getBoardID(void);
uint8_t getBoardUpID(void);
uint8_t getBoardSubID(uint8_t sub, uint8_t idx);
uint8_t getSlaveCnt(uint8_t sub);
#endif	//BUILD_SHARED_LIB_DLL

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#ifdef BUILD_SHARED_LIB_DLL
extern uint8_t board_id;
#endif	//BUILD_SHARED_LIB_DLL

#ifdef __cplusplus
}
#endif

#endif  //INC_FLEXSEA_BOARD_H
