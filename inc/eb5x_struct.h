#ifndef EB5X_STRUCT_H
#define EB5X_STRUCT_H

///
/// \file eb5x_struct.h
///
/// \brief AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
///
/// \core ac127769c2b60626825529bf7ddb50b667c6af6d
///
/// \build f9ccae449c72f4903da60273a24f0ff0682cf39d
///
/// \date 2021-07-19 16:06:35
///
/// \author Dephy, Inc.

#include "EB5x_device_spec.h"
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define EB5X_SYSTEM_TIME_POS 59
#define EB5X_STRUCT_DEVICE_FIELD_COUNT 60
#define EB5X_LABEL_MAX_CHAR_LENGTH 19

/// This is The Device fields * 10 + deviceField + 1. Ten is the max string length of 2^32 in
/// decimal separated from commas
#define EB5X_DATA_STRING_LENGTH 661

#ifdef __cplusplus
extern "C"
{
#endif

#pragma pack(1)

struct EB5xState
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
	int genvar_10;
	int genvar_11;
	int genvar_12;
	int genvar_13;
	int genvar_14;
	int ank_ang;
	int ank_vel;
	int shank_ang;
	int shank_vel;
	int global_shank_ang;
	int ank_pos_x;
	int ank_pos_y;
	int ank_pos_z;
	int ank_linear_vel_x;
	int ank_linear_vel_y;
	int ank_linear_vel_z;
	int mot_from_ank;
	int ank_from_mot;
	int trans_ratio;
	int ank_torque;
	int peak_ank_torque;
	int step_energy;
	int step_count;
	int step_time;
	int gait_state;
	int intermediate_state;
	int movement;
	int speed;
	int incline;
	int systemTime; /// System time
};

#pragma pack()

///
/// \brief Assigns the data in the buffer to the correct struct parameters
///
/// \param EB5x is the struct with the data to be set
///
/// \param _deviceStateBuffer is the buffer containing the data to be assigned to the struct
///
/// \param systemStartTime the time the system started. If unknown, use 0.
///
void EB5xSetData(struct EB5xState *eb5x, const uint32_t _deviceStateBuffer[], int systemStartTime);

///
/// \brief takes all data and places it into single, comma separated string
///
/// \param EB5x is the struct with the data to be placed in the string
///
/// \param dataString is where the new string wll be placed
///
void EB5xDataToString(struct EB5xState *eb5x, char dataString[EB5X_DATA_STRING_LENGTH]);

///
/// \brief retrieves the string equivalent of all parameter names
///
/// \param labels is the array of labels containing the parameter names
///
void EB5xGetLabels(char labels[EB5X_STRUCT_DEVICE_FIELD_COUNT][EB5X_LABEL_MAX_CHAR_LENGTH]);

///
/// \brief retrieves the string equivalent of parameter names starting with state time.
/// Parameters prior to state time, such as id, are not included.
///
/// \param labels is the array of labels containing the parameter names
///
int EB5xGetLabelsForLog(char labels[EB5X_STRUCT_DEVICE_FIELD_COUNT][EB5X_LABEL_MAX_CHAR_LENGTH]);

///
/// \brief Places data from struct into an array.
///
/// \param eb5x the data to be converted to an array
///
/// \param eb5xDataArray the array in which to place the data
///
void EB5xStructToDataArray(struct EB5xState eb5x, int32_t eb5xDataArray[EB5X_STRUCT_DEVICE_FIELD_COUNT]);

///
/// \brief Get data based on data position from device communication.
///
/// \param eb5x the data to access
///
/// \param dataPosition the position of data to access
///
/// \param dataValid return false if requested data position is invalid
///
int GetEB5xDataByDataPosition( struct EB5xState eb5x, int dataPosition);

#ifdef __cplusplus
} //extern "C"
#endif

#endif //EB5X_STRUCT_H
