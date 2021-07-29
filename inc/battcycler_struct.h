#ifndef BATTCYCLER_STRUCT_H
#define BATTCYCLER_STRUCT_H

///
/// \file battcycler_struct.h
///
/// \brief AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
///
/// \core c5e60a9b936218bf28732038398d20790a7e43c4
///
/// \build 6fe6c6d940447fd3d97f371713be0ccbc5a692c8
///
/// \date 2020-09-28 18:37:52
///
/// \author Dephy, Inc.

#include "BattCycler_device_spec.h"
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#define BATTCYCLER_SYSTEM_TIME_POS 22
#define BATTCYCLER_STRUCT_DEVICE_FIELD_COUNT 23
#define BATTCYCLER_LABEL_MAX_CHAR_LENGTH 34

/// This is The Device fields * 10 + deviceField + 1. Ten is the max string length of 2^32 in
/// decimal separated from commas
#define BATTCYCLER_DATA_STRING_LENGTH 254

#ifdef __cplusplus
extern "C"
{
#endif

#pragma pack(1)

struct BattCyclerState
{
	int battcycler;
	int id;
	int state_time;
	int current;
	int voltage;
	int esr;
	int fsm_state;
	int button;
	int leds;
	int genvar_0;
	int genvar_1;
	int genvar_2;
	int genvar_3;
	int status;
	int test_in_progress_now;
	int last_completed_test;
	int result_of_last_test;
	int time_elapsed_in_test;
	int error_codes;
	int charge_discharge_cycles_completed;
	int charge_discharge_total_cycles;
	int desired_battery_current;
	int systemTime; /// System time
};

#pragma pack()

///
/// \brief Assigns the data in the buffer to the correct struct parameters
///
/// \param BattCycler is the struct with the data to be set
///
/// \param _deviceStateBuffer is the buffer containing the data to be assigned to the struct
///
/// \param systemStartTime the time the system started. If unknown, use 0.
///
void BattCyclerSetData(struct BattCyclerState *battcycler, uint32_t _deviceStateBuffer[], int systemStartTime);

///
/// \brief takes all data and places it into single, comma separated string
///
/// \param BattCycler is the struct with the data to be placed in the string
///
/// \param dataString is where the new string wll be placed
///
void BattCyclerDataToString(struct BattCyclerState *battcycler, char dataString[BATTCYCLER_DATA_STRING_LENGTH]);

///
/// \brief retrieves the string equivalent of all parameter names
///
/// \param labels is the array of labels containing the parameter names
///
void BattCyclerGetLabels(char labels[BATTCYCLER_STRUCT_DEVICE_FIELD_COUNT][BATTCYCLER_LABEL_MAX_CHAR_LENGTH]);

///
/// \brief retrieves the string equivalent of parameter names starting with state time.
/// Parameters prior to state time, such as id, are not included.
///
/// \param labels is the array of labels containing the parameter names
///
int BattCyclerGetLabelsForLog(char labels[BATTCYCLER_STRUCT_DEVICE_FIELD_COUNT][BATTCYCLER_LABEL_MAX_CHAR_LENGTH]);

///
/// \brief Places data from struct into an array.
///
/// \param battcycler the data to be converte to an array
///
/// \param battcyclerDataArray the array in which to place the data
///
void BattCyclerStructToDataArray(struct BattCyclerState battcycler, int32_t battcyclerDataArray[BATTCYCLER_STRUCT_DEVICE_FIELD_COUNT]);

///
/// \brief Get data based on data position from device communication.
///
/// \param battcycler the data to access
///
/// \param dataPosition the position of data to access
///
/// \param dataValid return false if requested data position is invalid
///
int GetBattCyclerDataByDataPosition( struct BattCyclerState battcycler, int dataPosition);

#ifdef __cplusplus
} //extern "C"
#endif

#endif //BATTCYCLER_STRUCT_H
