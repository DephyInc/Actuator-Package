#ifndef BMS_STRUCT_H
#define BMS_STRUCT_H

/*
 * bms_struct.h
 *
 * AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
 * CORE:ecdab88c05df58d9ba18cb5e4d6e41c2f32b3e85
 * BUILD:065ba7c027caf247c3a01011370de5bc31a467f7
 *
 *
 * Specification File Created on: 2020-08-19 10:28:50
 * Author: Dephy, Inc.
 *
 */

#include "BMS_device_spec.h"
#include <stdio.h> 
#include <time.h> 
#include <string.h> 
#include <stdint.h> 

#include <stdbool.h> 

#define BMS_SYSTEM_TIME_POS 29
#define BMS_STRUCT_DEVICE_FIELD_COUNT 30
#define BMS_LABEL_MAX_CHAR_LENGTH 15

//This is The Device fields*10 + deviceField+1. Ten is the max string length of 2^32 in decimal separated from commas
#define BMS_DATA_STRING_LENGTH 331

#ifdef __cplusplus
extern "C"
{
#endif

#pragma pack(1)

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
	int error;
	int current;
	int stack_voltage;
	int temperature_0;
	int temperature_1;
	int temperature_2;
	int pack_imbalance;
	int balancing;
	int timer;
	int user_interface;
	int bq_sys_stat;
	int bq_sys_ctrl1;
	int bq_sys_ctrl2;
	int fw_version;
	int genvar_0_;
	int genvar_1_;

	//the system time
	int systemTime;
};

#pragma pack()

/// \brief Assigns the data in the buffer to the correct struct parameters
///
///@param BMS is the struct with the data to be set
///
///@param _deviceStateBuffer is the buffer containing the data to be assigned to the struct
///
///@param systemStartTime the time the system started. If unknown, use 0.
///
void BMSSetData(struct BMSState *bms, uint32_t _deviceStateBuffer[], int systemStartTime);

/// \brief takes all data and places it into single, comma separated string
///
///@param BMS is the struct with the data to be placed in the string
///
///@param dataString is where the new string wll be placed 
///
void BMSDataToString(struct BMSState *bms, char dataString[BMS_DATA_STRING_LENGTH]);

/// \brief retrieves the string equivalent of all parameter names
///
///@param labels is the array of labels containing the parameter names
///
void BMSGetLabels(char labels[BMS_STRUCT_DEVICE_FIELD_COUNT][BMS_LABEL_MAX_CHAR_LENGTH]);

/// \brief retrieves the string equivalent of parameter names starting with state time.  Parameters 
/// prior to state time, such as id,  are not included. 
///
///@param labels is the array of labels containing the parameter names
///
int BMSGetLabelsForLog(char labels[BMS_STRUCT_DEVICE_FIELD_COUNT][BMS_LABEL_MAX_CHAR_LENGTH]);

/// \brief Places data from struct into an array.
///
///@param actpack the data to be converte to an array
///
///@param actpackDataArray the array in which to place the data
///
void BMSStructToDataArray(struct BMSState bms, int32_t bmsDataArray[BMS_STRUCT_DEVICE_FIELD_COUNT]);

/// \brief Get data based on data position from device communication.
///
///@param actpack the data to access
///
///@param dataPosition the position of data to access
///
///@param dataValid return false if requested data position is invalid
///
int GetBMSDataByDataPosition( struct BMSState bms, int dataPosition);

#ifdef __cplusplus
}//extern "C"
#endif

#endif ////ACTPACK_STRUCT_H
