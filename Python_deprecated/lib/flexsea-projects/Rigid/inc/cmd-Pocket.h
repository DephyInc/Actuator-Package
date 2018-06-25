/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] flexsea-projects' User projects
	Copyright (C) 2018 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developer] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] cmd-Pocket: Pocket Commands
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2018-02-28 | jfduval | New code
****************************************************************************/

#ifndef INC_FLEXSEA_CMD_POCKET_H
#define INC_FLEXSEA_CMD_POCKET_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>
#include "flexsea_user_structs.h"

//****************************************************************************
// RX/TX Prototype(s):
//****************************************************************************

void rx_cmd_pocket_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_pocket_rr(uint8_t *buf, uint8_t *info);

void tx_cmd_pocket_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_pocket_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_pocket_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t offset, uint8_t controller, \
						int32_t setpoint, uint8_t setGains, int16_t g0, int16_t g1,\
						int16_t g2, int16_t g3, uint8_t controllerB, \
						int32_t setpointB, uint8_t setGainsB, int16_t g0B, int16_t g1B,\
						int16_t g2B, int16_t g3B, uint8_t system);

//****************************************************************************
// Prototype(s) - simplified functions (DLL):
//****************************************************************************

void ptx_cmd_pocket_r(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
							uint8_t offset);
void ptx_cmd_pocket_rw(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
							uint8_t offset, uint8_t controller, \
							int32_t setpoint, uint8_t setGains, int16_t g0, int16_t g1,\
							int16_t g2, int16_t g3, uint8_t controllerB, \
							int32_t setpointB, uint8_t setGainsB, int16_t g0B, int16_t g1B,\
							int16_t g2B, int16_t g3B, uint8_t system);

uint8_t newPocketRRpacketAvailable(void);
void getLastPocketData(struct pocket_s *r);
void init_pocket(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s):
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_POCKET_H
