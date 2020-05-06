#ifndef BMS_STRUCT_H
#define BMS_STRUCT_H
/*
 * bms_struct.h
 *
 * AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
 *
 *
 *  Created on: 2020-04-29 14:39:25.841293
 *      Author: Dephy Inc
 */

#include "BMS_device_spec.h"
#include <stdio.h> 
#include <time.h> 
#include <string.h> 
#include <stdint.h> 

#define BMS_SYSTEM_TIME_POS 25
#define BMS_STRUCT_DEVICE_FIELD_COUNT 26
#define BMS_LABEL_MAX_CHAR_LENGTH 14

//this is The Device fields*10 + deviceField.  Ten is the max string length of 2^32 in decimal separated from commas
#define BMS_DATA_STRING_LENGTH 286

#ifdef __cplusplus
extern "C"
{
#endif

struct BMSState 
 { 

	int bms_state_0;
	int id;
	int state_time;
	int cells_0_mv;
	int cells_1_mv;
	int cells_2_mv;
	int cells_3_mv;
	int cells_4_mv;
	int cells_5_mv;
	int cells_6_mv;
	int cells_7_mv;
	int cells_8_mv;
	int bms_state;
	int current;
	int timer;
	int balancing;
	int stack_voltage;
	int pack_imbalance;
	int temp_0_;
	int temp_1_;
	int temp_2_;
	int genvar_0_;
	int genvar_1_;
	int genvar_2_;
	int genvar_3_;
	//the system time
	clock_t systemTime;
	uint32_t deviceData[BMS_STRUCT_DEVICE_FIELD_COUNT];
};

/// \brief Assigns the data in the buffer to the correct struct parameters
///
///@param BMS is the struct with the data to be set
///
///@param _deviceStateBuffer is the buffer containing the data to be assigned to the struct
///
///@param systemStartTime the time the system started. If unknown, use 0.
///
void BMSSetData (struct BMSState *bms, uint32_t _deviceStateBuffer[], clock_t systemStartTime);

/// \brief takes all data and places it into single, comma separated string
///
///@param BMS is the struct with the data to be placed in the string
///
///@param dataString is where the new string wll be placed 
///
void BMSDataToString (struct BMSState *bms, char dataString[BMS_DATA_STRING_LENGTH]);

/// \brief retrieves the string equivalent of all parameter names
///
///@param labels is the array of labels containing the parameter names
///
void BMSGetLabels (char labels[BMS_STRUCT_DEVICE_FIELD_COUNT][BMS_LABEL_MAX_CHAR_LENGTH]);

/// \brief retrieves the string equivalent of parameter names starting with state time.  Parameters 
/// prior to state time, such as id,  are not included. 
///
///@param labels is the array of labels containing the parameter names
///
int BMSGetLabelsForLog (char labels[BMS_STRUCT_DEVICE_FIELD_COUNT][BMS_LABEL_MAX_CHAR_LENGTH]);



#ifdef __cplusplus
}//extern "C"
#endif


#endif ////ACTPACK_STRUCT_H