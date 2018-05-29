/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developper] Jean-Francois Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user-ex: User Projects & Functions, FlexSEA-Rigid Ex
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-04-24 | jfduval | New release
	*
****************************************************************************/

#ifdef BOARD_TYPE_FLEXSEA_EXECUTE

#ifndef INC_USER_EX_H
#define INC_USER_EX_H

//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"
#include "flexsea_board.h"
#include "flexsea_sys_def.h"
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
#define PROJECT_DEPHY			-1
#define PROJECT_BAREBONE		0	//Barebone Execute, nothing connected*
#define PROJECT_SIMPLE_MOTOR	1	//Barebone + BLDC Motor (sine commut.)
#define PROJECT_ACTPACK			2	//Dephy's Actuator Package
#define PROJECT_POCKET_BLDC     3   //FlexSEA-Pocket v0.1, 1x BLDC
#define PROJECT_POCKET_2XDC     4   //FlexSEA-Pocket v0.1, 2x DC
#define PROJECT_BIO_RIGID		5	//Biomech's version of Rigid (BLDC w/ QEI)
//*No external sensor, no sinusoidal commutation

//List of sub-projects:
#define SUBPROJECT_NONE			0
#define SUBPROJECT_A			1
#define SUBPROJECT_B			2
//(ex.: the 2-DoF ankle has 2 Execute. They both use PROJECT_2DOF_ANKLE, and each
// 		of them has a sub-project for specific configs)

//Step 1) Select active project (from list):
//==========================================

#define ACTIVE_PROJECT			PROJECT_ACTPACK
#define ACTIVE_SUBPROJECT		SUBPROJECT_A //A is Left

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
	//#define USE_I2C_0			//3V3, IMU & Expansion.
	//#define USE_I2C_1			//5V, Safety-CoP & strain gauge pot.
	//#define USE_IMU				//Requires USE_I2C_0
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
	#define USE_QEI
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, Onboard (Manage)
	#define USE_I2C_1			//5V, External (Angle sensor)
	#define USE_STRAIN			//Requires USE_I2C_1
	//#define USE_AS5047		//16-bit Position Sensor, SPI
	//#define USE_AS5048B		//Joint angle sensor (I2C)
	#define USE_EEPROM			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	#define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION

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
	#define ENC_CONTROL			ENC_QUADRATURE
	#define ENC_COMMUT			ENC_QUADRATURE
	#define ENC_DISPLAY			ENC_QUADRATURE
	
	#define CTRL_ENC_FCT(x) 	(x)  
	#define CTRL_ENC_VEL_FCT(x) (x)    
    #define CURRENT_ZERO		((int32)2048)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_SIMPLE_MOTOR

//FlexSEA-Pocket v0.1 - Default setup (1x BLDC)
#if(ACTIVE_PROJECT == PROJECT_POCKET_BLDC)

	//Enable/Disable sub-modules:
	#define USE_RS485
	//#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, Onboard (Manage)
	#define USE_I2C_1			//5V, External (Angle sensor)
	#define USE_STRAIN			//Requires USE_I2C_1
	#define USE_AS5047		//16-bit Position Sensor, SPI
	//#define USE_AS5048B		//Joint angle sensor (I2C)
	#define USE_EEPROM			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	#define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION

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
	
	#define CTRL_ENC_FCT(x) 	(x)  
	#define CTRL_ENC_VEL_FCT(x) (x)    
    #define CURRENT_ZERO		((int32)2048)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_SIMPLE_MOTOR

//Similar to Simple Motor, but specialized for ActPack
#if(ACTIVE_PROJECT == PROJECT_ACTPACK)

	//Enable/Disable sub-modules:
	#define USE_RS485
	//#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	//#define USE_QEI
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, Onboard (Manage)
	#define USE_I2C_1			//5V, External (Angle sensor)
	//#define USE_STRAIN		//Requires USE_I2C_1
	#define USE_AS5047			//16-bit Position Sensor, SPI
	#define USE_AS5048B			//Joint angle sensor (I2C)
	#define USE_EEPROM			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	#define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION

	//Runtime finite state machine (FSM):
	#define RUNTIME_FSM			ENABLED

	//Encoders:
	#define ENC_CONTROL			ENC_AS5047
	#define ENC_COMMUT			ENC_AS5047
	#define ENC_DISPLAY			ENC_CONTROL
    
    #define CURRENT_ZERO		((int32)2048)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_ACTPACK

//Biomech's version of Rigid (BLDC w/ QEI)
#if(ACTIVE_PROJECT == PROJECT_BIO_RIGID)

	//Enable/Disable sub-modules:
	#define USE_RS485
	//#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_QEI
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, Onboard (Manage)
	#define USE_I2C_1			//5V, External (Angle sensor)
	#define USE_STRAIN			//Requires USE_I2C_1
	//#define USE_AS5047		//16-bit Position Sensor, SPI
	#define USE_AS5048B			//Joint angle sensor (I2C)
	#define USE_EEPROM			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_SINE
	#define MOTOR_TYPE			MOTOR_BRUSHLESS
	#define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION

	//Runtime finite state machine (FSM):
    #define CO_ENABLE_ACTPACK
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
	#define ENC_CONTROL			ENC_QUADRATURE
	#define ENC_COMMUT			ENC_QUADRATURE
	#define ENC_DISPLAY			ENC_QUADRATURE
	
	#define CTRL_ENC_FCT(x) 	(x)  
	#define CTRL_ENC_VEL_FCT(x) (x)    
    #define CURRENT_ZERO		((int32)2048)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_BIO_RIGID

//FlexSEA-Pocket v0.1 - 2x BLDC
#if(ACTIVE_PROJECT == PROJECT_POCKET_2XDC)

	//Enable/Disable sub-modules:
	#define USE_RS485
	//#define USE_USB
	#define USE_COMM			//Requires USE_RS485 and/or USE_USB
	#define USE_QEI				//Primary quadrature encoder
	#define USE_QEI2			//	Second channel
	//#define USE_TRAPEZ
	#define USE_I2C_0			//3V3, Onboard (Manage)
	//#define USE_I2C_1			//5V, External (Angle sensor)
	#define USE_STRAIN			//
	//#define USE_AS5047		//16-bit Position Sensor, SPI
	//#define USE_AS5048B		//Joint angle sensor (I2C)
	#define USE_EEPROM			//
	#define USE_I2T_LIMIT		//I2t current limit

	//Motor type and commutation:
	#define MOTOR_COMMUT		COMMUT_NONE
	#define MOTOR_TYPE			MOTOR_BRUSHED
	#define MOTOR_ORIENTATION 	CLOCKWISE_ORIENTATION
	
	#define CO_ENABLE_ACTPACK	//Enables the ActPack state machine(s)

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
	#define ENC_CONTROL			ENC_QUADRATURE
	#define ENC_COMMUT			ENC_QUADRATURE
	#define ENC_DISPLAY			ENC_QUADRATURE
	
	#define CTRL_ENC_FCT(x) 	(x)  
	#define CTRL_ENC_VEL_FCT(x) (x)    
    #define CURRENT_ZERO		((int32)2048)

	//Slave ID:
	#define SLAVE_ID			FLEXSEA_EXECUTE_1

	//Project specific definitions:
	//...

#endif  //PROJECT_POCKET_2XDC

#if(ACTIVE_PROJECT == PROJECT_DEPHY)

	#include "dephy-ex.h"

#endif	//PROJECT_DEPHY

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
