/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-manage' Mid-level computing, and networking
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
	[This file] user: User Projects & Functions
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-09-23 | jfduval | Initial GPL-3.0 release
	*
****************************************************************************/

#ifdef BOARD_TYPE_FLEXSEA_MANAGE

#ifndef INC_USER_MN_H
#define INC_USER_MN_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"
#include "flexsea_board.h"
#include "flexsea_sys_def.h"
#include "flexsea_global_structs.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_user(void);
void user_fsm_1(void);
void user_fsm_2(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//List of projects:
#define PROJECT_DEPHY			-1
#define PROJECT_BAREBONE		0	//Barebone Manage, default option.
#define PROJECT_BB_RIGID		1	//Barebone Rigid
#define PROJECT_ACTPACK			2	//Dephy's Actuator Package (ActPack)
#define PROJECT_DEV				3	//Experimental code - use with care
#define PROJECT_ANKLE_2DOF		4	//Biomechatronics 2-DOF Ankle
#define PROJECT_RICNU_KNEE		5	//RIC/NU Knee
#define PROJECT_UMICH_KNEE		6	//University of Michigan's Knee
#define PROJECT_POCKET_2XDC		7	//FlexSEA-Pocket, 2x Brushed DC
#define PROJECT_MIT_DLEG		8	//Biomechatronics' Rigid + Relative encoder

//List of sub-projects:
#define SUBPROJECT_NONE			0
#define SUBPROJECT_A			1	//(typically the right side)
#define SUBPROJECT_B			2	//(typically the left side)
//(ex.: the 2-DoF ankle has 2 Execute. They both use PROJECT_2DOF_ANKLE, and each
// 		of them has a sub-project for specific configs)

//Leg sign:
#define RIGHT					1
#define LEFT					2

//Step 1) Select active project (from list):
//==========================================

#define ACTIVE_PROJECT			PROJECT_POCKET_2XDC
#define ACTIVE_SUBPROJECT		SUBPROJECT_A

//Step 2) Customize the enabled/disabled sub-modules:
//===================================================

//Barebone FlexSEA-Manage project - no external peripherals.
#if(ACTIVE_PROJECT == PROJECT_BAREBONE)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	//#define USE_I2C_2			//3V3, Expansion
	#define USE_I2C_3			//Onboard, Regulate & Execute
	#define USE_IMU				//Requires USE_I2C_1
	//#define USE_FLASH_MEM		//FLASH memory
	//#define USE_COMM_TEST		//Comm. characterization tool
	#define USE_UART3			//Bluetooth
	#define USE_SPI_PLAN		//Expansion/Plan
	//#define USE_BATTBOARD		//Battery Board, requires USE_I2C_2
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		DISABLED
	#define RUNTIME_FSM2		DISABLED

	#define MULTI_DOF_N 		0

	//Project specific definitions:
	//...

#endif	//PROJECT_BAREBONE

//RIC/NU Knee
#if(ACTIVE_PROJECT == PROJECT_RICNU_KNEE)

	#ifndef BOARD_SUBTYPE_RIGID

	//Setup when using FlexSEA-Manage:

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	#define USE_I2C_2			//3V3, Expansion
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_BATTBOARD		//Battery Board, requires USE_I2C_2

	#define MULTI_DOF_N 		0

	//Runtime finite state machine (FSM):
	//Disable both FSM to use manage as a passthru
	#define RUNTIME_FSM1		DISABLED 	//Control
	#define RUNTIME_FSM2		ENABLED 	//Comm w/ Execute 1
	//FSM2: Communication, we enabled this state machine to send data
	//back to the GUI.  Manage will now control execute, rather than the GUI.

	//Project specific definitions:
	//...

	#else

	//Setup when using Rigid-Mn (Actuator Package):

	//Enable/Disable sub-modules:
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	//#define USE_I2C_2			//3V3, Expansion
	#define USE_I2C_3			//Onboard, Regulate & Execute
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_UART3			//Bluetooth
	#define USE_SPI_PLAN		//Expansion/Plan
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH

	#define MULTI_DOF_N 		0

	//Runtime finite state machine (FSM):
	//Disable both FSM to use manage as a passthru
	#define RUNTIME_FSM1		DISABLED 	//Control
	#define RUNTIME_FSM2		ENABLED 	//Comm w/ Execute 1
	//FSM2: Communication, we enabled this state machine to send data
	//back to the GUI.  Manage will now control execute, rather than the GUI.

	//#define CO_ENABLE_ACTPACK

	#endif

#endif	//PROJECT_RICNU_KNEE

//MIT 2-DoF Ankle
#if(ACTIVE_PROJECT == PROJECT_ANKLE_2DOF)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	//#define USE_I2C_2			//3V3, Expansion
	#define USE_IMU				//Requires USE_I2C_1

	#define MULTI_DOF_N 		0

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

	//Project specific definitions:
	//...

#endif	//PROJECT_ANKLE_2DOF

//Experimental/Dev/Use only if you know what you are doing
#if(ACTIVE_PROJECT == PROJECT_DEV)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	//#define USE_I2C_2			//3V3, Expansion
	#define USE_IMU				//Requires USE_I2C_1
	//#define USE_BATTBOARD		//Battery Board, requires USE_I2C_1
	//#define USE_FLASH_MEM		//FLASH memory

	#define MULTI_DOF_N 		0

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

	//Project specific definitions:
	//...

#endif	//PROJECT_DEV

//BareBone Rigid
#if(ACTIVE_PROJECT == PROJECT_BB_RIGID)

	#if (HW_VER < 10)

		//Enable/Disable sub-modules:
		#define USE_USB
		#define USE_COMM			//Requires USE_RS485 and/or USE_USB
		#define USE_I2C_1			//3V3, IMU & Digital pot
		//#define USE_I2C_2			//3V3, Expansion
		#define USE_I2C_3			//Onboard, Regulate & Execute
		#define USE_IMU				//Requires USE_I2C_1
		#define USE_UART3			//Bluetooth
		#define USE_SPI_PLAN		//Expansion/Plan
		#define USE_EEPROM			//Emulated EEPROM, onboard FLASH

		//Runtime finite state machine (FSM):
		#define RUNTIME_FSM1		ENABLED
		#define RUNTIME_FSM2		ENABLED

	#else

		//Enable/Disable sub-modules:
		#define USE_USB
		#define USE_COMM			//Requires USE_RS485 and/or USE_USB
		#define USE_I2C_1			//3V3, IMU & Digital pot
		//#define USE_I2C_2			//3V3, Expansion
		#define USE_I2C_3			//Onboard, Regulate & Execute
		#define USE_IMU				//Requires USE_I2C_1
		//#define USE_UART3			//Bluetooth
		//#define USE_SPI_PLAN		//Expansion/Plan
		//#define USE_EEPROM			//Emulated EEPROM, onboard FLASH

		//Runtime finite state machine (FSM):
		#define RUNTIME_FSM1		ENABLED
		#define RUNTIME_FSM2		ENABLED

	#endif

	#define MULTI_DOF_N 			0

#endif	//PROJECT_BB_RIGID

//Dephy's Actuator Package (ActPack)
#if(ACTIVE_PROJECT == PROJECT_ACTPACK)

	#if (HW_VER < 10)

		//Enable/Disable sub-modules:
		#define USE_USB
		#define USE_COMM			//Requires USE_RS485 and/or USE_USB
		#define USE_I2C_1			//3V3, IMU & Digital pot
		#define USE_I2C_2			//3V3, Expansion
		#define USE_I2C_3			//Onboard, Regulate & Execute
		#define USE_IMU				//Requires USE_I2C_1
		#define USE_UART3			//Bluetooth
		#define USE_EEPROM			//Emulated EEPROM, onboard FLASH
		#define USE_WATCHDOG		//Independent watchdog (IWDG)
		#define USE_6CH_AMP			//Requires USE_I2C_2. 6-ch Strain Amp.
		#define USE_SPI_PLAN		//Enables the external SPI port

		//Runtime finite state machine (FSM):
		//#define RUNTIME_FSM1		ENABLED	//Enable only if you DO NOT use Plan
		#define RUNTIME_FSM2		ENABLED	//Enable at all time, Mn <> Ex comm.

		#if(ACTIVE_SUBPROJECT == SUBPROJECT_A)

		#define MULTI_DOF_N			0

		#endif

		#if(ACTIVE_SUBPROJECT == SUBPROJECT_B)

		#define MULTI_DOF_N			1

		#endif

	#else

		//Enable/Disable sub-modules:
		#define USE_USB
		#define USE_COMM			//Requires USE_RS485 and/or USE_USB
		#define USE_I2C_1			//3V3, IMU & Digital pot
		//#define USE_I2C_2			//3V3, Expansion
		#define USE_I2C_3			//Onboard, Regulate & Execute
		#define USE_IMU				//Requires USE_I2C_1
		#define USE_UART3			//Bluetooth #1
		#define USE_EEPROM			//Emulated EEPROM, onboard FLASH
		//#define USE_WATCHDOG		//Independent watchdog (IWDG)
		//#define USE_6CH_AMP		//Requires USE_I2C_2. 6-ch Strain Amp.
		//#define USE_SPI_PLAN		//Enables the external SPI port

		//Runtime finite state machine (FSM):
		//#define RUNTIME_FSM1		ENABLED	//Enable only if you DO NOT use Plan
		#define RUNTIME_FSM2		ENABLED	//Enable at all time, Mn <> Ex comm.

		#define MULTI_DOF_N 		0

	#endif

#endif	//PROJECT_ACTPACK

//University of Michigan's Knee
#if(ACTIVE_PROJECT == PROJECT_UMICH_KNEE)

	//Enable/Disable sub-modules:
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	#define USE_I2C_2			//3V3, Expansion
	#define USE_I2C_3			//Onboard, Regulate & Execute
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_UART3			//Bluetooth
	//#define USE_SPI_PLAN		//Expansion/Plan
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH
	#define USE_6CH_AMP			//Requires USE_I2C_2. 6-ch Strain Amp.

	#define MULTI_DOF_N 		0

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

#endif	//PROJECT_UMICH_KNEE

//FlexSEA-Pocket
#if(ACTIVE_PROJECT == PROJECT_POCKET_2XDC)

	//Enable/Disable sub-modules:
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	//#define USE_I2C_2			//3V3, Expansion
	#define USE_I2C_3			//Onboard, Regulate & Execute
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_UART3			//Bluetooth
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH
	#define USE_WATCHDOG		//Independent watchdog (IWDG)
	//#define USE_SPI_PLAN		//Enables the external SPI port

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED	//Enable only if you DO NOT use Plan
	#define RUNTIME_FSM2		ENABLED	//Enable at all time, Mn <> Ex comm.

	#define CO_ENABLE_ACTPACK	//Enables the ActPack state machine(s)

	#define MULTI_DOF_N			0

#endif	//PROJECT_POCKET_2XDC

//Biomechatronics' Rigid + Relative encoder
#if(ACTIVE_PROJECT == PROJECT_MIT_DLEG)

	//Enable/Disable sub-modules:
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	#define USE_I2C_2			//3V3, Expansion
	#define USE_I2C_3			//Onboard, Regulate & Execute
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_UART3			//Bluetooth
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH
	#define USE_WATCHDOG		//Independent watchdog (IWDG)
	//#define USE_6CH_AMP			//Requires USE_I2C_2. 6-ch Strain Amp.
	#define USE_SPI_PLAN		//Enables the external SPI port

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED	//Enable only if you DO NOT use Plan
	#define RUNTIME_FSM2		ENABLED	//Enable at all time, Mn <> Ex comm.

	#define CO_ENABLE_ACTPACK	//Enables the ActPack state machine(s)

	#if(ACTIVE_SUBPROJECT == SUBPROJECT_A)

	#define MULTI_DOF_N			0

	#endif

	#if(ACTIVE_SUBPROJECT == SUBPROJECT_B)

	#define MULTI_DOF_N			1

	#endif

#endif	//PROJECT_MIT_DLEG

#if(ACTIVE_PROJECT == PROJECT_DEPHY)

	#include "dephy-mn.h"

#endif	//PROJECT_DEPHY

//****************************************************************************
// Structure(s)
//****************************************************************************

//MIT 2-DoF Ankle
#if(ACTIVE_PROJECT == PROJECT_ANKLE_2DOF)

struct ankle2dof_s
{
	uint8_t r_w;					//Read/write values
	uint8_t ctrl;					//Controller
	uint8_t ctrl_change;			//KEEP or CHANGE
	uint8_t ctrl_o;					//Open speed
	uint8_t ctrl_i;					//Current
	struct gains_s ctrl_i_gains;	//Current controller gains
};

#endif	//PROJECT_ANKLE_2DOF

//****************************************************************************
// Shared variable(s)
//****************************************************************************

//MIT Ankle 2-DoF:
#if(ACTIVE_PROJECT == PROJECT_ANKLE_2DOF)

extern struct ankle2dof_s ankle2dof_left, ankle2dof_right;

#endif	//PROJECT_ANKLE_2DOF

#endif	//INC_USER_MN_H

#endif //BOARD_TYPE_FLEXSEA_MANAGE
