/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
	Copyright (C) 2017 Dephy, Inc. <http://dephy.com/>
*****************************************************************************
	[Lead developer] Justin Cechmanek, jcechmanek at dephy dot com
	[Contributors] Jean-Francois Duval, jfduval at dephy dot com
*****************************************************************************
	[This file] svm: Support Vector Machine Math Functions
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2017-08-14 | jfduval | Adapted for STM32F4
	*
****************************************************************************/

#ifdef INCLUDE_UPROJ_SVM

#ifndef INC_SVM_MATH_FCT_H
#define INC_SVM_MATH_FCT_H

//Faster exp() approximation.
//method described in: https://nic.schraudolph.org/pubs/Schraudolph99.pdf
static union
{
	double d;
	struct
	{
		int j, i;
	}n;
}_eco;

#define EXP_A 	(1048576/M_LN2) 	//use 1512775 for integer version
#define EXP_C 	60801 				//see text for choice of c values
#define EXP(y) 	(_eco.n.i = EXP_A*(y) + (1072693248 - EXP_C), _eco.d)

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void add(float* vec1, float* vec2, float* return_vec, int length);
void subtract(float* vec1, float* vec2, float* return_vec, int length);
float dotProduct(float* vec1, float* vec2, int length);
int sign(float value);

#endif	//INC_SVM_MATH_FCT_H
#endif 	//INCLUDE_UPROJ_SVM
