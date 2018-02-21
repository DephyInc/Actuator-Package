/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'user/ActPack' Dephy's Actuator Package (ActPack)
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] cmd-ActPack: Custom commands for the Actuator package
****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-09-27 | jfduval | Initial release
	*
****************************************************************************/

#ifdef INCLUDE_UPROJ_ACTPACK

#ifndef INC_FLEXSEA_CMD_ACTPACK_H
#define INC_FLEXSEA_CMD_ACTPACK_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include "flexsea_system.h"

//****************************************************************************
// Prototype(s):
//****************************************************************************

void tx_cmd_actpack_rw(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
						uint16_t *len, uint8_t offset, uint8_t controller, \
						int32_t setpoint, uint8_t setGains, int16_t g0, int16_t g1,\
						int16_t g2, int16_t g3, uint8_t system);
void tx_cmd_actpack_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
					uint16_t *len, uint8_t offset);
void tx_cmd_actpack_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, \
							uint16_t *len, uint8_t offset);

void rx_cmd_actpack_rw(uint8_t *buf, uint8_t *info);
void rx_cmd_actpack_rr(uint8_t *buf, uint8_t *info);

//****************************************************************************
// Prototype(s) - simplified functions (DLL):
//****************************************************************************

void ptx_cmd_actpack_rw(uint8_t slaveId, uint16_t *numb, uint8_t *commStr, \
						uint8_t offset, uint8_t controller, \
						int32_t setpoint, uint8_t setGains, int16_t g0, int16_t g1,\
						int16_t g2, int16_t g3, uint8_t system);

uint8_t newActPackRRpacketAvailable(void);
//void getLastRigidData(struct rigid_s *r);
//void init_rigid(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

#ifndef NULL
#define NULL   ((void *) 0)
#endif

//System variable states:
#define SYS_NORMAL			0
#define SYS_DISABLE_FSM2	1

//****************************************************************************
// Structure(s):
//****************************************************************************

struct ActPack_s
{
	uint8_t controller;
	int32_t setpoint;
	uint8_t setGains;
	int16_t g0;
	int16_t g1;
	int16_t g2;
	int16_t g3;
	uint8_t system;
};

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern uint8_t ActPackSys;

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_CMD_ACTPACK_H
#endif //INCLUDE_UPROJ_ACTPACK
