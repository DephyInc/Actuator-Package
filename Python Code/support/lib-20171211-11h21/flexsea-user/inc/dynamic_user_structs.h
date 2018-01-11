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
	[This file] flexsea_global_structs: contains all the data structures
	used across the project
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-03-14 | David Weisdorf | Initial release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_DYNAMIC_USER_STRUCTS_H
#define INC_FLEXSEA_DYNAMIC_USER_STRUCTS_H

#ifdef __cplusplus
	extern "C" {
#endif

#include <stdint.h>

#if((defined BOARD_TYPE_FLEXSEA_EXECUTE) || (defined BOARD_TYPE_FLEXSEA_MANAGE))

volatile struct DynamicUserData_s
{
	int32_t time;
	int8_t exo_state;
	int8_t gait_state;
	int16_t ank_ang;
	int16_t mot_cur;

	int16_t mot_vol;
	int16_t mot_ang;
	uint16_t bat_volt;
	int16_t exo_torq;
	int16_t exo_power;

	int16_t exo_elec_pow;
	int16_t ank_vel;
	int16_t mot_cur_sp;
	int16_t exo_gyro;
	int16_t gait_min_df_ang;

	int16_t mot_from_ank_ang;
	int16_t ank_from_mot_ang;
	int16_t ana_to_mot_ang;
	int16_t mot_vel;
	int16_t mot_acc;
	int16_t pwm;

	int32_t gen1;
	int32_t gen2;
	int32_t gen3;
	int16_t gen4;
	int16_t gen5;
	int16_t gen6;
} __attribute__((packed));

//The following are for the user to define in dynamic_user_structs_common.c
typedef struct DynamicUserData_s DynamicUserData_t;

#if((defined BOARD_TYPE_FLEXSEA_EXECUTE) || (defined BOARD_TYPE_FLEXSEA_MANAGE))
extern DynamicUserData_t dynamicUserData;
#endif

// you may also wish to typedef this type to another more convenient name
// typedef struct DynamicUserData_s YourNameHere_t
#endif

void tx_cmd_user_dyn_r(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, uint16_t *len, \
						uint8_t sendMetaData);

void tx_cmd_user_dyn_w(uint8_t *shBuf, uint8_t *cmd, uint8_t *cmdType, uint16_t *len);

void rx_cmd_user_dyn_r(uint8_t *buf, uint8_t *info);
void rx_cmd_user_dyn_w(uint8_t *buf, uint8_t *info);

void rx_cmd_user_dyn_rr(uint8_t *buf, uint8_t *info);

void init_flexsea_payload_ptr_dynamic();

#ifdef BOARD_TYPE_FLEXSEA_PLAN

extern uint8_t newMetaDataAvailable;
extern uint8_t packAndSendOffsetRequest;
extern uint8_t newDataAvailable;
extern uint8_t waitingOnFieldFlags;

extern int dynamicUser_slaveId;
extern uint8_t* dynamicUser_data;
extern uint8_t dynamicUser_numFields;
extern uint8_t* dynamicUser_fieldTypes;
extern uint8_t* dynamicUser_labelLengths;
extern char** dynamicUser_labels;

extern uint8_t* dynamicUser_fieldFlagsExec;
extern uint8_t* dynamicUser_fieldFlagsPlan;

#endif

uint16_t packFieldFlags(uint8_t* shBuf, uint8_t numFields, uint8_t* fieldFlags);
int unpackFieldFlags(uint8_t* buf, uint8_t* fieldFlags, uint16_t len);

// Flags
#define SEND_DATA       0x00
#define SEND_METADATA   0x01
#define SEND_FIELD_FLAGS 0x02


#ifdef __cplusplus
	}
#endif

#endif //INC_FLEXSEA_DYNAMIC_USER_STRUCTS_H
