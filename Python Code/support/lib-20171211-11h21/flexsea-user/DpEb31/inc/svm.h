/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developer] Justin Cechmanek, jcechmanek at dephy dot com
	[Contributors] Jean-Francois Duval, jfduval at dephy dot com
*****************************************************************************
	[This file] svm: Support Vector Machine
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-08-11 | jfduval | Adapted for STM32F4
	*
****************************************************************************/

#ifdef INCLUDE_UPROJ_SVM

#ifndef INC_SVM_H
#define INC_SVM_H

//#define TEST_PC	//Un-comment this to test on a PC...
//#define TEST_STM32	//and this to test on Manage (STM32) with pre-recorded data.
//For normal operation the two lines above should be commented out

//Runtime math:
#define CALC_PER_SLOT			7

//GUI:
#define GUI_MINIMA_FLAG_LATCH	10	//ms (use >= 1, never 0)

// inline helpers
#define len(x) (sizeof(x) / sizeof(*x))

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void svm(void);
void svmBackgroundMath(void);

#ifdef TEST_STM32
void test_svm_blocking(void);
#endif //TEST_STM32

#endif	//INC_SVM_H
#endif 	//INCLUDE_UPROJ_SVM
