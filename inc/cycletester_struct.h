#ifndef CYCLETESTER_STRUCT_H
#define CYCLETESTER_STRUCT_H

///
/// \file cycletester_struct.h
///
/// \brief AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
///
/// \core 9aef6d74b18c1c47d64bf9be2e1a769752e5ad8b
///
/// \build fb364600346136d1240bef7b18993a3ef541559a
///
/// \date 2020-06-22 14:42:45
///
/// \author Dephy, Inc.

#include "CycleTester_device_spec.h"
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define CYCLETESTER_SYSTEM_TIME_POS 32
#define CYCLETESTER_STRUCT_DEVICE_FIELD_COUNT 33
#define CYCLETESTER_LABEL_MAX_CHAR_LENGTH 12

/// This is The Device fields * 10 + deviceField + 1. Ten is the max string length of 2^32 in
/// decimal separated from commas
#define CYCLETESTER_DATA_STRING_LENGTH 364

#ifdef __cplusplus
extern "C"
{
#endif

#pragma pack(1)

struct CycleTesterState
{
	int rigid;
	int id;
	int state_time;
	int accelx;
	int accely;
	int accelz;
	int gyrox;
	int gyroy;
	int gyroz;
	int mot_ang;
	int mot_vel;
	int mot_acc;
	int mot_cur;
	int mot_volt;
	int batt_volt;
	int batt_curr;
	int temperature;
	int status_mn;
	int status_ex;
	int status_re;
	int genvar_0;
	int genvar_1;
	int genvar_2;
	int genvar_3;
	int genvar_4;
	int genvar_5;
	int genvar_6;
	int genvar_7;
	int genvar_8;
	int genvar_9;
	int ank_ang;
	int ank_vel;
	int systemTime; /// System time
};

#pragma pack()

///
/// \brief Assigns the data in the buffer to the correct struct parameters
///
/// \param CycleTester is the struct with the data to be set
///
/// \param _deviceStateBuffer is the buffer containing the data to be assigned to the struct
///
/// \param systemStartTime the time the system started. If unknown, use 0.
///
void CycleTesterSetData(struct CycleTesterState *cycletester, uint32_t _deviceStateBuffer[], int systemStartTime);

///
/// \brief takes all data and places it into single, comma separated string
///
/// \param CycleTester is the struct with the data to be placed in the string
///
/// \param dataString is where the new string wll be placed
///
void CycleTesterDataToString(struct CycleTesterState *cycletester, char dataString[CYCLETESTER_DATA_STRING_LENGTH]);

///
/// \brief retrieves the string equivalent of all parameter names
///
/// \param labels is the array of labels containing the parameter names
///
void CycleTesterGetLabels(char labels[CYCLETESTER_STRUCT_DEVICE_FIELD_COUNT][CYCLETESTER_LABEL_MAX_CHAR_LENGTH]);

///
/// \brief retrieves the string equivalent of parameter names starting with state time.
/// Parameters prior to state time, such as id, are not included.
///
/// \param labels is the array of labels containing the parameter names
///
int CycleTesterGetLabelsForLog(char labels[CYCLETESTER_STRUCT_DEVICE_FIELD_COUNT][CYCLETESTER_LABEL_MAX_CHAR_LENGTH]);

///
/// \brief Places data from struct into an array.
///
/// \param cycletester the data to be converte to an array
///
/// \param cycletesterDataArray the array in which to place the data
///
void CycleTesterStructToDataArray(struct CycleTesterState cycletester, int32_t cycletesterDataArray[CYCLETESTER_STRUCT_DEVICE_FIELD_COUNT]);

///
/// \brief Get data based on data position from device communication.
///
/// \param cycletester the data to access
///
/// \param dataPosition the position of data to access
///
/// \param dataValid return false if requested data position is invalid
///
int GetCycleTesterDataByDataPosition( struct CycleTesterState cycletester, int dataPosition);

#ifdef __cplusplus
} //extern "C"
#endif

#endif //CYCLETESTER_STRUCT_H
