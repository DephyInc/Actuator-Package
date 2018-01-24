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
	[This file] flexsea_cmd_calibration: commands specific to the calibration tools
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-02-07 | dweisdorf | Initial GPL-3.0 release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_CALIBRATION_H
#define INC_FLEXSEA_CMD_CALIBRATION_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>

//****************************************************************************
// Prototype(s):
//****************************************************************************

/* Initializes part of the array of function pointers which determines which
	function to call upon receiving a message
*/
void init_flexsea_payload_ptr_calibration(void);

//Calibration mode:


/* Called by master to send a message to the slave, attempting to inititiate a calibration procedure specified by
	'calibrationMode'. Slave will respond with the calibration procedure it is running or about to run.
*/
void tx_cmd_calibration_mode_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t calibrationMode);

/* Called by master to send a message to the slave, attempting to inititiate a
	calibration procedure specified by 'calibrationMode'. Slave will not respond.
	TODO: rename this to 'write'
*/
void tx_cmd_calibration_mode_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t calibrationMode);

/* Master calls this function automatically after receiving a response from slave
*/
void rx_cmd_calibration_mode_rr(uint8_t *buf, uint8_t *info);

/* Slave calls this function automatically after receiving a read from master.
	It determines what to do with the information passed to it,
	And it replies indicating the resulting decision
*/
void rx_cmd_calibration_mode_rw(uint8_t *buf, uint8_t *info);

/* Slave calls this function automatically after receiving a read from master.
	It determines what to do with the information passed to it,
	And it does not reply.
*/
void rx_cmd_calibration_mode_w(uint8_t *buf, uint8_t *info);

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_CALIBRATION_H


