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
#define PROJECT_BAREBONE		0	//Barebone Manage, default option.
#define PROJECT_ANKLE_2DOF		1	//Biomechatronics 2-DOF Ankle
#define PROJECT_RICNU_KNEE		3	//RIC/NU Knee
#define PROJECT_MOTORTB			4
#define PROJECT_DEV				5	//Experimental code - use with care
#define PROJECT_CYCLE_TESTER	6	//Automatic Cycle Tester
#define PROJECT_DPEB			7	//DpEb2.1 and below
#define PROJECT_DPEB31			8	//DpEb3.1 Exo
#define PROJECT_BB_RIGID		9	//Barebone Rigid
#define PROJECT_UMICH_KNEE		10	//University of Michigan's Knee

//List of sub-projects:
#define SUBPROJECT_NONE			0
#define SUBPROJECT_A			1	//(typically the right side)
#define SUBPROJECT_B			2	//(typically the left side)
//(ex.: the 2-DoF ankle has 2 Execute. They both use PROJECT_2DOF_ANKLE, and each
// 		of them has a sub-project for specific configs)

//Exo sign:
#define RIGHT					1
#define LEFT					2

//Step 1) Select active project (from list):
//==========================================

#define ACTIVE_PROJECT			PROJECT_UMICH_KNEE
#define ACTIVE_SUBPROJECT		NONE

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
	//#define USE_SPI_PLAN		//Expansion/Plan
	//#define USE_BATTBOARD		//Battery Board, requires USE_I2C_2
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		DISABLED
	#define RUNTIME_FSM2		DISABLED

	//Project specific definitions:
	//...

#endif	//PROJECT_BAREBONE

//RIC/NU Knee
#if(ACTIVE_PROJECT == PROJECT_RICNU_KNEE)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	#define USE_I2C_2			//3V3, Expansion
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_BATTBOARD		//Battery Board, requires USE_I2C_2

	//Runtime finite state machine (FSM):
	//Disable both FSM to use manage as a passthru
	#define RUNTIME_FSM1		DISABLED 	//Control
	#define RUNTIME_FSM2		ENABLED 	//Comm w/ Execute 1
	//FSM2: Communication, we enabled this state machine to send data
	//back to the GUI.  Manage will now control execute, rather than the GUI.

	//Project specific definitions:
	//...

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

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

	//Project specific definitions:
	//...

#endif	//PROJECT_ANKLE_2DOF

//Dephy's Motor Test Bench
#if(ACTIVE_PROJECT == PROJECT_MOTORTB)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	#define USE_I2C_2			//3V3, Expansion
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_BATTBOARD		//Battery Board, requires USE_I2C_1

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

	//Project specific definitions:
	//...

#endif	//PROJECT_MOTORTB

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

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

	//Project specific definitions:
	//...

#endif	//PROJECT_DEV

//Automatic Cycle Tester
#if(ACTIVE_PROJECT == PROJECT_CYCLE_TESTER)

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

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

#endif	//PROJECT_CYCLE_TESTER

//DpEb3.1 Exo
#if(ACTIVE_PROJECT == PROJECT_DPEB31)

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
	//#define USE_SVM			//Support vector machine

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

	#if(ACTIVE_SUBPROJECT == RIGHT)

		#define EXO_SIDE	RIGHT

	#elif(ACTIVE_SUBPROJECT == LEFT)

		#define EXO_SIDE	LEFT

	#else

		#error "PROJECT_DPEB31 requires a subproject"

	#endif

#endif	//PROJECT_DPEB31

//BareBone Rigid
#if(ACTIVE_PROJECT == PROJECT_BB_RIGID)

	//Enable/Disable sub-modules:
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_I2C_1			//3V3, IMU & Digital pot
	//#define USE_I2C_2			//3V3, Expansion
	#define USE_I2C_3			//Onboard, Regulate & Execute
	#define USE_IMU				//Requires USE_I2C_1
	#define USE_UART3			//Bluetooth
	//#define USE_SPI_PLAN		//Expansion/Plan
	#define USE_EEPROM			//Emulated EEPROM, onboard FLASH

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

#endif	//PROJECT_BB_RIGID

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
	#define USE_6CH_AMP			//Requires USE_I2C_1. 6-ch Strain Amp.

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM1		ENABLED
	#define RUNTIME_FSM2		ENABLED

#endif	//PROJECT_BB_RIGID

//****************************************************************************
// Structure(s)
//****************************************************************************

struct ankle2dof_s
{
	uint8_t r_w;					//Read/write values
	uint8_t ctrl;					//Controller
	uint8_t ctrl_change;			//KEEP or CHANGE
	uint8_t ctrl_o;					//Open speed
	uint8_t ctrl_i;					//Current
	struct gains_s ctrl_i_gains;	//Current controller gains
};

//****************************************************************************
// Shared variable(s)
//****************************************************************************

//MIT Ankle 2-DoF:
#if(ACTIVE_PROJECT == PROJECT_ANKLE_2DOF)

extern struct ankle2dof_s ankle2dof_left, ankle2dof_right;

#endif	//PROJECT_ANKLE_2DOF

#endif	//INC_USER_MN_H

#endif //BOARD_TYPE_FLEXSEA_MANAGE
