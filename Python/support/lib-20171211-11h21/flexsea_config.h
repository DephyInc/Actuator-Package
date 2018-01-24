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
	[This file] flexsea_board: configuration and functions for this
	particular board
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-09 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CONFIG_H
#define INC_FLEXSEA_CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>
#include "flexsea.h"

//****************************************************************************
// Prototype(s):
//****************************************************************************

void initFlexSEAStack(uint8_t id, void (*fsss)(PacketWrapper* p), \
						void (*fssm)(PacketWrapper* p));
void initFlexSEAStack_minimalist(uint8_t id);

void initMasterCommDefaults(void);
void initSlaveCommDefaults(void);

void mapSendSerialSlave(void (*f)(PacketWrapper* p));
void mapSendSerialMaster(void (*f)(PacketWrapper* p));

//Used by test code:
uint8_t setBoardID(uint8_t id);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern void (*externalSendSerialSlave)(PacketWrapper* p);
extern void (*externalSendSerialMaster)(PacketWrapper* p);

#ifdef __cplusplus
}
#endif

#endif  //INC_FLEXSEA_BOARD_H
