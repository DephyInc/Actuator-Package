/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
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
	[Lead developper] Jean-Francois Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user-ex: User Projects & Functions, FlexSEA-Execute
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-10-30 | jfduval | New release
	*
****************************************************************************/

/*Important: we reached a point where we couldn't support all configurations
  without changing the TopDesign (we ran out of ressources). You might have
  to select a different TopDesign file than the one included by default (check
  the folder, there is more than one included) */

#ifdef BOARD_TYPE_FLEXSEA_EXECUTE

#ifndef INC_USER_EX_H
#define INC_USER_EX_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"
#include "flexsea_board.h"
#include "../MIT_2DoF_Ankle_v1/inc/user-ex-MIT_2DoF_Ankle_v1.h"
#include "../RICNU_Knee_v1/inc/user-ex-RICNU_Knee_v1.h"
#include "../MotorTestBench/inc/user-ex-MotorTestBench.h"
#include "flexsea_sys_def.h"
//#include "user-ex.h"
//Add your project specific user_x.h file here

//****************************************************************************
// Shared variable(s)
//****************************************************************************

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_user(void);
void user_fsm(void);

//****************************************************************************
// Definition(s):
//****************************************************************************

//List of encoders that can be used by controllers (position, impedance),
//and for commutation:
#define ENC_NONE				0	//No encoder
#define ENC_HALL				1	//Hall effect (motor commutation)
#define ENC_QUADRATURE			2	//Optical or magnetic, AB/I inputs on QEI1
#define ENC_ANALOG				3	//Potentiometer (or other), on ext. analog in.
#define ENC_AS5047				4	//16-bit Magnetic Position Sensor, SPI
#define ENC_AS5048B				5	//14-bit Magnetic Position Sensor, I2C
#define ENC_CUSTOM			  	6	//Heavily modified user variable that cannot
									//be represented CTRL_ENC_FCT
//(later you'll assign what encoder is used by the controllers, for motor
// commutation, and which one is displayed in the GUI)

//Type of motor commutation:
#define COMMUT_BLOCK			0
#define COMMUT_SINE				1
#define COMMUT_NONE				2	//Software test, no motor

//Current sensing strategy:
#define CS_LEGACY				0
#define CS_DEFAULT				1

//Types of motor orientation. Rotation of motor when you are looking at the rotor
#define CLOCKWISE_ORIENTATION 			1
#define COUNTER_CLOCKWISE_ORIENTATION 	-1

//List of projects:
#define PROJECT_BAREBONE		0	//Barebone Execute, nothing connected*
#define PROJECT_SIMPLE_MOTOR	1	//Barebone + BLDC Motor (sine commut.)
#define PROJECT_ANKLE_2DOF		2	//Biomechatronics 2-DOF Ankle
#define PROJECT_RICNU_KNEE		3	//RIC/NU Knee
#define PROJECT_MOTORTB			4	//Motor TestBench
#define PROJECT_SIMPLE_MAXON	5	//Demo/test code, Maxon + Hall + QEI
#define PROJECT_DPEB21  		6	//DpEb21 project
#define PROJECT_CYCLE_TESTER	7
//*No external sensor, no sinusoidal commutation

//List of sub-projects:
#define SUBPROJECT_NONE			0
#define SUBPROJECT_A			1
#define SUBPROJECT_B			2
//(ex.: the 2-DoF ankle has 2 Execute. They both use PROJECT_2DOF_ANKLE, and each
// 		of them has a sub-project for specific configs)

//Step 1) Select active project (from list):
//==========================================

#define ACTIVE_PROJECT			PROJECT_BAREBONE
#define ACTIVE_SUBPROJECT		SUBPROJECT_B //A is Left

//Step 2) Customize the enabled/disabled sub-modules:
//===================================================

//Barebone FlexSEA-Execute project - no external peripherals (and no motor)
#if(ACTIVE_PROJECT == PROJECT_BAREBONE)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_IMU				//Requires USE_I2C_0
	#define USE_STRAIN			//Requires USE_I2C_1
	//#define USE_EEPROM		//
	//#define USE_FLASH			//
	//#define USE_BLUETOOTH		//
	#define USE_I2T_LIMIT		//I2t current limit
	
	#define RUNTIME_FSM	 		DISABLED
	
	//Motor type, direction and commutation:
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	#define MOTOR_COMMUT 		COMMUT_NONE
	#define CURRENT_ZERO		((int32)2048)
	
	//Encoders:
	#define ENC_CONTROL			ENC_NONE
	#define ENC_COMMUT			ENC_NONE
	#define ENC_DISPLAY			ENC_NONE
	
	//Control encoder function:
	#define PWM_SIGN			1
	#define CTRL_ENC_FCT(x) 	(x)
	#define CTRL_ENC_VEL_FCT(x) (x)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif	//PROJECT_BAREBONE

//Similar to Barebone, but including a motor
#if(ACTIVE_PROJECT == PROJECT_SIMPLE_MOTOR)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_STRAIN			//Requires USE_I2C_1
	#define USE_AS5047			//16-bit Position Sensor, SPI
	#define USE_EEPROM			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	#define MOTOR_ORIENTATION 	COUNTER_CLOCKWISE_ORIENTATION

	//Runtime finite state machine (FSM):

	//#define FINDPOLES //define if you want to find the poles

	#ifdef FINDPOLES
		#define RUNTIME_FSM	 DISABLED
	#else
		#ifdef USE_TRAPEZ
			#define RUNTIME_FSM	 DISABLED
		#else
			#define RUNTIME_FSM	 ENABLED
		#endif
	#endif

	//Encoders:
	#define ENC_CONTROL			ENC_AS5047
	#define ENC_COMMUT			ENC_AS5047
	#define ENC_DISPLAY			ENC_CONTROL
    
    #define CURRENT_ZERO		((int32)2048)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_SIMPLE_MOTOR

//MIT 2-DoF Ankle
#if(ACTIVE_PROJECT == PROJECT_ANKLE_2DOF)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_IMU				//Requires USE_I2C_0
	//#define USE_STRAIN		//Requires USE_I2C_1
	#define USE_AS5047			//16-bit Position Sensor, SPI
	//#define USE_SPI_COMMUT	//
	#define USE_EEPROM			//
	#define USE_FLASH			//
	#define USE_BLUETOOTH		//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS

	//Runtime finite state machine (FSM):

	//#define FINDPOLES //define if you want to find the poles

	#ifdef FINDPOLES
		#define RUNTIME_FSM	 DISABLED
	#else
		#ifdef USE_TRAPEZ
			#define RUNTIME_FSM	 DISABLED
		#else
			//#define RUNTIME_FSM	 ENABLED
		#endif
	#endif

	#define CURRENT_ZERO		((int32)2065)

	//Encoders:
	#define ENC_CONTROL			ENC_AS5047
	#define ENC_COMMUT			ENC_AS5047
	#define ENC_DISPLAY			ENC_CONTROL

	//Subproject A: Left execute board looking at the back of the ankle while it is standing up
	#if(ACTIVE_SUBPROJECT == SUBPROJECT_A)

		//Control encoder function:

		#define PWM_SIGN			1
		#define CTRL_ENC_FCT(x) 	(x)
		#define CTRL_ENC_VEL_FCT(x) (x)
		//...

		//Slave ID:
		#define SLAVE_ID		FLEXSEA_EXECUTE_2

	#endif  //SUBPROJECT_A

	//Subproject B: Right actuator
	#if(ACTIVE_SUBPROJECT == SUBPROJECT_B)

		//Control encoder function:
		#define PWM_SIGN		 -1
		#define CTRL_ENC_FCT(x) (x)
		#define CTRL_ENC_VEL_FCT(x) (x)
		//...

		//Slave ID:
		#define SLAVE_ID		FLEXSEA_EXECUTE_1

	#endif  //SUBPROJECT_B

	//Project specific definitions:
	extern int32 ankle_ang, ankle_trans, mot_vel;
	//...

#endif  //PROJECT_ANKLE_2DOF

//RIC/NU Knee
#if(ACTIVE_PROJECT == PROJECT_RICNU_KNEE)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_IMU				//Requires USE_I2C_0
	//#define USE_STRAIN		//Requires USE_I2C_1
	#define USE_AS5047			//16-bit Position Sensor, SPI
	//#define USE_MINM_RGB		//External RGB LED. Requires USE_I2C_0.
	#define USE_EEPROM			//Non-volatile memory, EEPROM
	//#define USE_FLASH			//Non-volatile memory, FLASH
	//#define USE_BLUETOOTH		//Bluetooth module on EX12/EX13
	#define USE_I2T_LIMIT		//I2t current limit
	#define USE_EXT_I2C_STRAIN	//External Strain Amplifier, on I2C0
	#define USE_AS5048B			//14-bit Position Sensor, on I2C0

	//Motor type, direction and commutation:
	#define MOTOR_COMMUT 			COMMUT_SINE
	#define MOTOR_TYPE				MOTOR_BRUSHLESS
	#define PWM_SIGN				1

	//Define if you want to find the poles:
	//#define FINDPOLES

	//Runtime finite state machine (FSM):
	#ifdef FINDPOLES
		#define RUNTIME_FSM	 	DISABLED
	#else
		#ifdef USE_TRAPEZ
			#define RUNTIME_FSM	 DISABLED
		#else
			#define RUNTIME_FSM	 ENABLED
		#endif
	#endif

	//Encoders:
	#define ENC_CONTROL				ENC_AS5047
	#define ENC_COMMUT				ENC_AS5047
	#define ENC_DISPLAY				ENC_CONTROL

	//Control encoder function:
	#if (ENC_CONTROL == ENC_AS5047)
		#define CTRL_ENC_FCT(x) 		(x)	//ToDo make better
		#define CTRL_ENC_VEL_FCT(x) 	((x>>10))	//encoder velocity is measured in clicks/ms x 1024
	#elif (ENC_CONTROL == ENC_AS5048B)
		#define CTRL_ENC_FCT(x) 		(x)	//ToDo make better
		#define CTRL_ENC_VEL_FCT(x) 	((x>>8))	//encoder velocity is measured in clicks/ms x 1024
	#endif

	//Project specific definitions:
	#define CURRENT_ZERO			((int32)2065)

	//Slave ID:
	#define SLAVE_ID				FLEXSEA_EXECUTE_1

#endif	//PROJECT_RICNU_KNEE

//Motor test bench
#if(ACTIVE_PROJECT == PROJECT_MOTORTB)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_IMU				//Requires USE_I2C_0
	#define USE_STRAIN			//Requires USE_I2C_1
	#define USE_AS5047			//16-bit Position Sensor, SPI
	//#define USE_SPI_COMMUT	//
	#define USE_EEPROM			//
	#define USE_FLASH			//
	#define USE_BLUETOOTH		//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS

	//Runtime finite state machine (FSM):

	//#define FINDPOLES //define if you want to find the poles

	#ifdef FINDPOLES
		#define RUNTIME_FSM	 DISABLED
	#else
		#ifdef USE_TRAPEZ
			#define RUNTIME_FSM	 DISABLED
		#else
			#define RUNTIME_FSM	 ENABLED
		#endif
	#endif

	//Encoders:
	#define ENC_CONTROL			ENC_AS5047
	#define ENC_COMMUT			ENC_AS5047
	#define ENC_DISPLAY			ENC_CONTROL

	//Subproject A: No torque sensor, execute 2
	#if(ACTIVE_SUBPROJECT == SUBPROJECT_A)

		//Control encoder function:

		#define PWM_SIGN			1
		#define CTRL_ENC_FCT(x) 	(x)
		#define CTRL_ENC_VEL_FCT(x) (x)
		//...
        
        #define CURRENT_ZERO		((int32)1981)

		//Slave ID:
		#define SLAVE_ID		FLEXSEA_EXECUTE_2

	#endif  //SUBPROJECT_A

	//Subproject B: Has the torque sensor, Execute 1
	#if(ACTIVE_SUBPROJECT == SUBPROJECT_B)

		//Control encoder function:
		#define PWM_SIGN		 -1
		#define CTRL_ENC_FCT(x) (x)
		#define CTRL_ENC_VEL_FCT(x) (x)
		//...
        
        #define CURRENT_ZERO		((int32)2123)
        
		//Slave ID:
		#define SLAVE_ID		FLEXSEA_EXECUTE_1

	#endif  //SUBPROJECT_B

	//Project specific definitions:
	//...

#endif  //PROJECT_MOTORTB

//Similar to Barebone, but including a Maxon motor and its typical companions:
//Hall sensors (commutation) and QEI encoder
#if(ACTIVE_PROJECT == PROJECT_SIMPLE_MAXON)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_QEI
	#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_IMU				//Requires USE_I2C_0
	#define USE_STRAIN			//Requires USE_I2C_1
	//#define USE_AS5047		//16-bit Position Sensor, SPI. Used by Sine Commut.
	#define USE_EEPROM			//
	#define USE_FLASH			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_BLOCK
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	
	//Current sensing:
	#define CURRENT_SENSING		CS_DEFAULT

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM	 DISABLED

	//Encoders:
	#define ENC_CONTROL			ENC_QUADRATURE
	#define ENC_COMMUT			ENC_HALL
	#define ENC_DISPLAY			ENC_QUADRATURE

	//Control encoder function:
	#define PWM_SIGN			1
	#define CTRL_ENC_FCT(x) 	(x)
	#define CTRL_ENC_VEL_FCT(x) (x)
	//...
    
    #define CURRENT_ZERO		((int32)2091)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_SIMPLE_MAXON

//DPEB21
#if(ACTIVE_PROJECT == PROJECT_DPEB21)

	//Enable/Disable sub-modules:
	#define USE_RS485
	#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, IMU & Expansion.
	#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	#define USE_IMU				//Requires USE_I2C_0
	#define USE_STRAIN			//Requires USE_I2C_1
	#define USE_AS5047			//16-bit Position Sensor, SPI
	#define USE_EEPROM			//
	#define USE_FLASH			//
	#define USE_BLUETOOTH		//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS

	//Runtime finite state machine (FSM):

	//#define FINDPOLES //define if you want to find the poles

	#ifdef FINDPOLES
		#define RUNTIME_FSM	 DISABLED
	#else
		#ifdef USE_TRAPEZ
			#define RUNTIME_FSM	 DISABLED
		#else
			#define RUNTIME_FSM	 ENABLED
		#endif
	#endif

	//Encoders:
	#define ENC_CONTROL			ENC_AS5047
	#define ENC_COMMUT			ENC_AS5047
	#define ENC_DISPLAY			ENC_CONTROL

	//Subproject A: Left Proto
	#if(ACTIVE_SUBPROJECT == SUBPROJECT_A)
        #define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION
		//Slave ID:
		#define SLAVE_ID		FLEXSEA_EXECUTE_1
	#endif  //SUBPROJECT_A
    
    //Subproject B: Right Proto
	#if(ACTIVE_SUBPROJECT == SUBPROJECT_B)
        #define MOTOR_ORIENTATION 	COUNTER_CLOCKWISE_ORIENTATION
		//Slave ID:
		#define SLAVE_ID		FLEXSEA_EXECUTE_1
	#endif  //SUBPROJECT_A

	//Project specific definitions:
	//...

#endif  //DPEB21

//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Default(s)
//****************************************************************************
#ifndef MOTOR_ORIENTATION
#define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION
#endif

#endif	//INC_USER_EX_H

#endif //BOARD_TYPE_FLEXSEA_EXECUTE
