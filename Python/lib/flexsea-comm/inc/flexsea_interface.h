/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-comm' Communication stack
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
	[This file] flexsea_interface: simple in & out functions
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-09-11 | jfduval | Initial release
****************************************************************************/

#ifndef INC_FLEXSEA_INTERFACE_H_
#define INC_FLEXSEA_INTERFACE_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include "flexsea.h"

//****************************************************************************
// Prototype(s):
//****************************************************************************

void receiveFlexSEAPacket(Port p, uint8_t *newPacketFlag, \
							uint8_t *parsedPacketFlag);
uint8_t receiveFlexSEABytes(uint8_t *d, uint8_t len, uint8_t autoParse);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************


//****************************************************************************
// Macro(s):
//****************************************************************************


#ifdef __cplusplus
}
#endif

#endif
