#ifndef NETMASTER_STRUCT_H
#define NETMASTER_STRUCT_H
/*
 * netmaster_struct.h
 *
 * AUTOGENERATED FILE! ONLY EDIT IF YOU ARE A MACHINE!
 *
 *
 *  Created on: 2020-04-11 09:05:24.603269
 *      Author: Dephy Inc
 */

#include "NetMaster_device_spec.h "
#include <sstream> 
#include <stdio.h> 
#include <string> 

#include <ctime> 

#define NETMASTER_SYSTEM_TIME_POS 72
#define NETMASTER_STRUCT_DEVICE_FIELD_COUNT 73

struct NetMasterState 
 { 

	int netmaster;
	int id;
	int state_time;
	int genvar_0;
	int genvar_1;
	int genvar_2;
	int genvar_3;
	int status;
	int a_accelx;
	int a_accely;
	int a_accelz;
	int a_gyrox;
	int a_gyroy;
	int a_gyroz;
	int a_pressure;
	int a_status;
	int b_accelx;
	int b_accely;
	int b_accelz;
	int b_gyrox;
	int b_gyroy;
	int b_gyroz;
	int b_pressure;
	int b_status;
	int c_accelx;
	int c_accely;
	int c_accelz;
	int c_gyrox;
	int c_gyroy;
	int c_gyroz;
	int c_pressure;
	int c_status;
	int d_accelx;
	int d_accely;
	int d_accelz;
	int d_gyrox;
	int d_gyroy;
	int d_gyroz;
	int d_pressure;
	int d_status;
	int e_accelx;
	int e_accely;
	int e_accelz;
	int e_gyrox;
	int e_gyroy;
	int e_gyroz;
	int e_pressure;
	int e_status;
	int f_accelx;
	int f_accely;
	int f_accelz;
	int f_gyrox;
	int f_gyroy;
	int f_gyroz;
	int f_pressure;
	int f_status;
	int g_accelx;
	int g_accely;
	int g_accelz;
	int g_gyrox;
	int g_gyroy;
	int g_gyroz;
	int g_pressure;
	int g_status;
	int h_accelx;
	int h_accely;
	int h_accelz;
	int h_gyrox;
	int h_gyroy;
	int h_gyroz;
	int h_pressure;
	int h_status;
	//the system time
	clock_t systemTime;
	uint32_t deviceData[NETMASTER_STRUCT_DEVICE_FIELD_COUNT];

	// sets the data.  Requires system start time.  If unavailable, please use 0
	void setData(uint32_t _deviceStateBuffer[], clock_t systemStartTime) 
 	{
		netmaster=_deviceStateBuffer[NETMASTER_NETMASTER_POS ];
		deviceData[NETMASTER_NETMASTER_POS ]=_deviceStateBuffer[NETMASTER_NETMASTER_POS ];
		id=_deviceStateBuffer[NETMASTER_ID_POS ];
		deviceData[NETMASTER_ID_POS ]=_deviceStateBuffer[NETMASTER_ID_POS ];
		state_time=_deviceStateBuffer[NETMASTER_STATE_TIME_POS ];
		deviceData[NETMASTER_STATE_TIME_POS ]=_deviceStateBuffer[NETMASTER_STATE_TIME_POS ];
		genvar_0=_deviceStateBuffer[NETMASTER_GENVAR_0_POS ];
		deviceData[NETMASTER_GENVAR_0_POS ]=_deviceStateBuffer[NETMASTER_GENVAR_0_POS ];
		genvar_1=_deviceStateBuffer[NETMASTER_GENVAR_1_POS ];
		deviceData[NETMASTER_GENVAR_1_POS ]=_deviceStateBuffer[NETMASTER_GENVAR_1_POS ];
		genvar_2=_deviceStateBuffer[NETMASTER_GENVAR_2_POS ];
		deviceData[NETMASTER_GENVAR_2_POS ]=_deviceStateBuffer[NETMASTER_GENVAR_2_POS ];
		genvar_3=_deviceStateBuffer[NETMASTER_GENVAR_3_POS ];
		deviceData[NETMASTER_GENVAR_3_POS ]=_deviceStateBuffer[NETMASTER_GENVAR_3_POS ];
		status=_deviceStateBuffer[NETMASTER_STATUS_POS ];
		deviceData[NETMASTER_STATUS_POS ]=_deviceStateBuffer[NETMASTER_STATUS_POS ];
		a_accelx=_deviceStateBuffer[NETMASTER_A_ACCELX_POS ];
		deviceData[NETMASTER_A_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_A_ACCELX_POS ];
		a_accely=_deviceStateBuffer[NETMASTER_A_ACCELY_POS ];
		deviceData[NETMASTER_A_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_A_ACCELY_POS ];
		a_accelz=_deviceStateBuffer[NETMASTER_A_ACCELZ_POS ];
		deviceData[NETMASTER_A_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_A_ACCELZ_POS ];
		a_gyrox=_deviceStateBuffer[NETMASTER_A_GYROX_POS ];
		deviceData[NETMASTER_A_GYROX_POS ]=_deviceStateBuffer[NETMASTER_A_GYROX_POS ];
		a_gyroy=_deviceStateBuffer[NETMASTER_A_GYROY_POS ];
		deviceData[NETMASTER_A_GYROY_POS ]=_deviceStateBuffer[NETMASTER_A_GYROY_POS ];
		a_gyroz=_deviceStateBuffer[NETMASTER_A_GYROZ_POS ];
		deviceData[NETMASTER_A_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_A_GYROZ_POS ];
		a_pressure=_deviceStateBuffer[NETMASTER_A_PRESSURE_POS ];
		deviceData[NETMASTER_A_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_A_PRESSURE_POS ];
		a_status=_deviceStateBuffer[NETMASTER_A_STATUS_POS ];
		deviceData[NETMASTER_A_STATUS_POS ]=_deviceStateBuffer[NETMASTER_A_STATUS_POS ];
		b_accelx=_deviceStateBuffer[NETMASTER_B_ACCELX_POS ];
		deviceData[NETMASTER_B_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_B_ACCELX_POS ];
		b_accely=_deviceStateBuffer[NETMASTER_B_ACCELY_POS ];
		deviceData[NETMASTER_B_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_B_ACCELY_POS ];
		b_accelz=_deviceStateBuffer[NETMASTER_B_ACCELZ_POS ];
		deviceData[NETMASTER_B_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_B_ACCELZ_POS ];
		b_gyrox=_deviceStateBuffer[NETMASTER_B_GYROX_POS ];
		deviceData[NETMASTER_B_GYROX_POS ]=_deviceStateBuffer[NETMASTER_B_GYROX_POS ];
		b_gyroy=_deviceStateBuffer[NETMASTER_B_GYROY_POS ];
		deviceData[NETMASTER_B_GYROY_POS ]=_deviceStateBuffer[NETMASTER_B_GYROY_POS ];
		b_gyroz=_deviceStateBuffer[NETMASTER_B_GYROZ_POS ];
		deviceData[NETMASTER_B_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_B_GYROZ_POS ];
		b_pressure=_deviceStateBuffer[NETMASTER_B_PRESSURE_POS ];
		deviceData[NETMASTER_B_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_B_PRESSURE_POS ];
		b_status=_deviceStateBuffer[NETMASTER_B_STATUS_POS ];
		deviceData[NETMASTER_B_STATUS_POS ]=_deviceStateBuffer[NETMASTER_B_STATUS_POS ];
		c_accelx=_deviceStateBuffer[NETMASTER_C_ACCELX_POS ];
		deviceData[NETMASTER_C_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_C_ACCELX_POS ];
		c_accely=_deviceStateBuffer[NETMASTER_C_ACCELY_POS ];
		deviceData[NETMASTER_C_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_C_ACCELY_POS ];
		c_accelz=_deviceStateBuffer[NETMASTER_C_ACCELZ_POS ];
		deviceData[NETMASTER_C_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_C_ACCELZ_POS ];
		c_gyrox=_deviceStateBuffer[NETMASTER_C_GYROX_POS ];
		deviceData[NETMASTER_C_GYROX_POS ]=_deviceStateBuffer[NETMASTER_C_GYROX_POS ];
		c_gyroy=_deviceStateBuffer[NETMASTER_C_GYROY_POS ];
		deviceData[NETMASTER_C_GYROY_POS ]=_deviceStateBuffer[NETMASTER_C_GYROY_POS ];
		c_gyroz=_deviceStateBuffer[NETMASTER_C_GYROZ_POS ];
		deviceData[NETMASTER_C_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_C_GYROZ_POS ];
		c_pressure=_deviceStateBuffer[NETMASTER_C_PRESSURE_POS ];
		deviceData[NETMASTER_C_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_C_PRESSURE_POS ];
		c_status=_deviceStateBuffer[NETMASTER_C_STATUS_POS ];
		deviceData[NETMASTER_C_STATUS_POS ]=_deviceStateBuffer[NETMASTER_C_STATUS_POS ];
		d_accelx=_deviceStateBuffer[NETMASTER_D_ACCELX_POS ];
		deviceData[NETMASTER_D_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_D_ACCELX_POS ];
		d_accely=_deviceStateBuffer[NETMASTER_D_ACCELY_POS ];
		deviceData[NETMASTER_D_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_D_ACCELY_POS ];
		d_accelz=_deviceStateBuffer[NETMASTER_D_ACCELZ_POS ];
		deviceData[NETMASTER_D_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_D_ACCELZ_POS ];
		d_gyrox=_deviceStateBuffer[NETMASTER_D_GYROX_POS ];
		deviceData[NETMASTER_D_GYROX_POS ]=_deviceStateBuffer[NETMASTER_D_GYROX_POS ];
		d_gyroy=_deviceStateBuffer[NETMASTER_D_GYROY_POS ];
		deviceData[NETMASTER_D_GYROY_POS ]=_deviceStateBuffer[NETMASTER_D_GYROY_POS ];
		d_gyroz=_deviceStateBuffer[NETMASTER_D_GYROZ_POS ];
		deviceData[NETMASTER_D_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_D_GYROZ_POS ];
		d_pressure=_deviceStateBuffer[NETMASTER_D_PRESSURE_POS ];
		deviceData[NETMASTER_D_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_D_PRESSURE_POS ];
		d_status=_deviceStateBuffer[NETMASTER_D_STATUS_POS ];
		deviceData[NETMASTER_D_STATUS_POS ]=_deviceStateBuffer[NETMASTER_D_STATUS_POS ];
		e_accelx=_deviceStateBuffer[NETMASTER_E_ACCELX_POS ];
		deviceData[NETMASTER_E_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_E_ACCELX_POS ];
		e_accely=_deviceStateBuffer[NETMASTER_E_ACCELY_POS ];
		deviceData[NETMASTER_E_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_E_ACCELY_POS ];
		e_accelz=_deviceStateBuffer[NETMASTER_E_ACCELZ_POS ];
		deviceData[NETMASTER_E_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_E_ACCELZ_POS ];
		e_gyrox=_deviceStateBuffer[NETMASTER_E_GYROX_POS ];
		deviceData[NETMASTER_E_GYROX_POS ]=_deviceStateBuffer[NETMASTER_E_GYROX_POS ];
		e_gyroy=_deviceStateBuffer[NETMASTER_E_GYROY_POS ];
		deviceData[NETMASTER_E_GYROY_POS ]=_deviceStateBuffer[NETMASTER_E_GYROY_POS ];
		e_gyroz=_deviceStateBuffer[NETMASTER_E_GYROZ_POS ];
		deviceData[NETMASTER_E_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_E_GYROZ_POS ];
		e_pressure=_deviceStateBuffer[NETMASTER_E_PRESSURE_POS ];
		deviceData[NETMASTER_E_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_E_PRESSURE_POS ];
		e_status=_deviceStateBuffer[NETMASTER_E_STATUS_POS ];
		deviceData[NETMASTER_E_STATUS_POS ]=_deviceStateBuffer[NETMASTER_E_STATUS_POS ];
		f_accelx=_deviceStateBuffer[NETMASTER_F_ACCELX_POS ];
		deviceData[NETMASTER_F_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_F_ACCELX_POS ];
		f_accely=_deviceStateBuffer[NETMASTER_F_ACCELY_POS ];
		deviceData[NETMASTER_F_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_F_ACCELY_POS ];
		f_accelz=_deviceStateBuffer[NETMASTER_F_ACCELZ_POS ];
		deviceData[NETMASTER_F_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_F_ACCELZ_POS ];
		f_gyrox=_deviceStateBuffer[NETMASTER_F_GYROX_POS ];
		deviceData[NETMASTER_F_GYROX_POS ]=_deviceStateBuffer[NETMASTER_F_GYROX_POS ];
		f_gyroy=_deviceStateBuffer[NETMASTER_F_GYROY_POS ];
		deviceData[NETMASTER_F_GYROY_POS ]=_deviceStateBuffer[NETMASTER_F_GYROY_POS ];
		f_gyroz=_deviceStateBuffer[NETMASTER_F_GYROZ_POS ];
		deviceData[NETMASTER_F_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_F_GYROZ_POS ];
		f_pressure=_deviceStateBuffer[NETMASTER_F_PRESSURE_POS ];
		deviceData[NETMASTER_F_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_F_PRESSURE_POS ];
		f_status=_deviceStateBuffer[NETMASTER_F_STATUS_POS ];
		deviceData[NETMASTER_F_STATUS_POS ]=_deviceStateBuffer[NETMASTER_F_STATUS_POS ];
		g_accelx=_deviceStateBuffer[NETMASTER_G_ACCELX_POS ];
		deviceData[NETMASTER_G_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_G_ACCELX_POS ];
		g_accely=_deviceStateBuffer[NETMASTER_G_ACCELY_POS ];
		deviceData[NETMASTER_G_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_G_ACCELY_POS ];
		g_accelz=_deviceStateBuffer[NETMASTER_G_ACCELZ_POS ];
		deviceData[NETMASTER_G_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_G_ACCELZ_POS ];
		g_gyrox=_deviceStateBuffer[NETMASTER_G_GYROX_POS ];
		deviceData[NETMASTER_G_GYROX_POS ]=_deviceStateBuffer[NETMASTER_G_GYROX_POS ];
		g_gyroy=_deviceStateBuffer[NETMASTER_G_GYROY_POS ];
		deviceData[NETMASTER_G_GYROY_POS ]=_deviceStateBuffer[NETMASTER_G_GYROY_POS ];
		g_gyroz=_deviceStateBuffer[NETMASTER_G_GYROZ_POS ];
		deviceData[NETMASTER_G_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_G_GYROZ_POS ];
		g_pressure=_deviceStateBuffer[NETMASTER_G_PRESSURE_POS ];
		deviceData[NETMASTER_G_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_G_PRESSURE_POS ];
		g_status=_deviceStateBuffer[NETMASTER_G_STATUS_POS ];
		deviceData[NETMASTER_G_STATUS_POS ]=_deviceStateBuffer[NETMASTER_G_STATUS_POS ];
		h_accelx=_deviceStateBuffer[NETMASTER_H_ACCELX_POS ];
		deviceData[NETMASTER_H_ACCELX_POS ]=_deviceStateBuffer[NETMASTER_H_ACCELX_POS ];
		h_accely=_deviceStateBuffer[NETMASTER_H_ACCELY_POS ];
		deviceData[NETMASTER_H_ACCELY_POS ]=_deviceStateBuffer[NETMASTER_H_ACCELY_POS ];
		h_accelz=_deviceStateBuffer[NETMASTER_H_ACCELZ_POS ];
		deviceData[NETMASTER_H_ACCELZ_POS ]=_deviceStateBuffer[NETMASTER_H_ACCELZ_POS ];
		h_gyrox=_deviceStateBuffer[NETMASTER_H_GYROX_POS ];
		deviceData[NETMASTER_H_GYROX_POS ]=_deviceStateBuffer[NETMASTER_H_GYROX_POS ];
		h_gyroy=_deviceStateBuffer[NETMASTER_H_GYROY_POS ];
		deviceData[NETMASTER_H_GYROY_POS ]=_deviceStateBuffer[NETMASTER_H_GYROY_POS ];
		h_gyroz=_deviceStateBuffer[NETMASTER_H_GYROZ_POS ];
		deviceData[NETMASTER_H_GYROZ_POS ]=_deviceStateBuffer[NETMASTER_H_GYROZ_POS ];
		h_pressure=_deviceStateBuffer[NETMASTER_H_PRESSURE_POS ];
		deviceData[NETMASTER_H_PRESSURE_POS ]=_deviceStateBuffer[NETMASTER_H_PRESSURE_POS ];
		h_status=_deviceStateBuffer[NETMASTER_H_STATUS_POS ];
		deviceData[NETMASTER_H_STATUS_POS ]=_deviceStateBuffer[NETMASTER_H_STATUS_POS ];

		systemTime= systemStartTime-clock();
		deviceData[NETMASTER_SYSTEM_TIME_POS]=systemTime;
	};

	void sendToStream(std::stringstream &ss) 
 	{
		ss << state_time <<",";
		ss << genvar_0 <<",";
		ss << genvar_1 <<",";
		ss << genvar_2 <<",";
		ss << genvar_3 <<",";
		ss << status <<",";
		ss << a_accelx <<",";
		ss << a_accely <<",";
		ss << a_accelz <<",";
		ss << a_gyrox <<",";
		ss << a_gyroy <<",";
		ss << a_gyroz <<",";
		ss << a_pressure <<",";
		ss << a_status <<",";
		ss << b_accelx <<",";
		ss << b_accely <<",";
		ss << b_accelz <<",";
		ss << b_gyrox <<",";
		ss << b_gyroy <<",";
		ss << b_gyroz <<",";
		ss << b_pressure <<",";
		ss << b_status <<",";
		ss << c_accelx <<",";
		ss << c_accely <<",";
		ss << c_accelz <<",";
		ss << c_gyrox <<",";
		ss << c_gyroy <<",";
		ss << c_gyroz <<",";
		ss << c_pressure <<",";
		ss << c_status <<",";
		ss << d_accelx <<",";
		ss << d_accely <<",";
		ss << d_accelz <<",";
		ss << d_gyrox <<",";
		ss << d_gyroy <<",";
		ss << d_gyroz <<",";
		ss << d_pressure <<",";
		ss << d_status <<",";
		ss << e_accelx <<",";
		ss << e_accely <<",";
		ss << e_accelz <<",";
		ss << e_gyrox <<",";
		ss << e_gyroy <<",";
		ss << e_gyroz <<",";
		ss << e_pressure <<",";
		ss << e_status <<",";
		ss << f_accelx <<",";
		ss << f_accely <<",";
		ss << f_accelz <<",";
		ss << f_gyrox <<",";
		ss << f_gyroy <<",";
		ss << f_gyroz <<",";
		ss << f_pressure <<",";
		ss << f_status <<",";
		ss << g_accelx <<",";
		ss << g_accely <<",";
		ss << g_accelz <<",";
		ss << g_gyrox <<",";
		ss << g_gyroy <<",";
		ss << g_gyroz <<",";
		ss << g_pressure <<",";
		ss << g_status <<",";
		ss << h_accelx <<",";
		ss << h_accely <<",";
		ss << h_accelz <<",";
		ss << h_gyrox <<",";
		ss << h_gyroy <<",";
		ss << h_gyroz <<",";
		ss << h_pressure <<",";
		ss << h_status <<",";
		ss << systemTime <<",";
	};

	 static void GetLabels(std::string *labels) 
 	{
		labels[NETMASTER_NETMASTER_POS]= "netmaster";
		labels[NETMASTER_ID_POS]= "id";
		labels[NETMASTER_STATE_TIME_POS]= "state_time";
		labels[NETMASTER_GENVAR_0_POS]= "genVar_0";
		labels[NETMASTER_GENVAR_1_POS]= "genVar_1";
		labels[NETMASTER_GENVAR_2_POS]= "genVar_2";
		labels[NETMASTER_GENVAR_3_POS]= "genVar_3";
		labels[NETMASTER_STATUS_POS]= "status";
		labels[NETMASTER_A_ACCELX_POS]= "A_accelx";
		labels[NETMASTER_A_ACCELY_POS]= "A_accely";
		labels[NETMASTER_A_ACCELZ_POS]= "A_accelz";
		labels[NETMASTER_A_GYROX_POS]= "A_gyrox";
		labels[NETMASTER_A_GYROY_POS]= "A_gyroy";
		labels[NETMASTER_A_GYROZ_POS]= "A_gyroz";
		labels[NETMASTER_A_PRESSURE_POS]= "A_pressure";
		labels[NETMASTER_A_STATUS_POS]= "A_status";
		labels[NETMASTER_B_ACCELX_POS]= "B_accelx";
		labels[NETMASTER_B_ACCELY_POS]= "B_accely";
		labels[NETMASTER_B_ACCELZ_POS]= "B_accelz";
		labels[NETMASTER_B_GYROX_POS]= "B_gyrox";
		labels[NETMASTER_B_GYROY_POS]= "B_gyroy";
		labels[NETMASTER_B_GYROZ_POS]= "B_gyroz";
		labels[NETMASTER_B_PRESSURE_POS]= "B_pressure";
		labels[NETMASTER_B_STATUS_POS]= "B_status";
		labels[NETMASTER_C_ACCELX_POS]= "C_accelx";
		labels[NETMASTER_C_ACCELY_POS]= "C_accely";
		labels[NETMASTER_C_ACCELZ_POS]= "C_accelz";
		labels[NETMASTER_C_GYROX_POS]= "C_gyrox";
		labels[NETMASTER_C_GYROY_POS]= "C_gyroy";
		labels[NETMASTER_C_GYROZ_POS]= "C_gyroz";
		labels[NETMASTER_C_PRESSURE_POS]= "C_pressure";
		labels[NETMASTER_C_STATUS_POS]= "C_status";
		labels[NETMASTER_D_ACCELX_POS]= "D_accelx";
		labels[NETMASTER_D_ACCELY_POS]= "D_accely";
		labels[NETMASTER_D_ACCELZ_POS]= "D_accelz";
		labels[NETMASTER_D_GYROX_POS]= "D_gyrox";
		labels[NETMASTER_D_GYROY_POS]= "D_gyroy";
		labels[NETMASTER_D_GYROZ_POS]= "D_gyroz";
		labels[NETMASTER_D_PRESSURE_POS]= "D_pressure";
		labels[NETMASTER_D_STATUS_POS]= "D_status";
		labels[NETMASTER_E_ACCELX_POS]= "E_accelx";
		labels[NETMASTER_E_ACCELY_POS]= "E_accely";
		labels[NETMASTER_E_ACCELZ_POS]= "E_accelz";
		labels[NETMASTER_E_GYROX_POS]= "E_gyrox";
		labels[NETMASTER_E_GYROY_POS]= "E_gyroy";
		labels[NETMASTER_E_GYROZ_POS]= "E_gyroz";
		labels[NETMASTER_E_PRESSURE_POS]= "E_pressure";
		labels[NETMASTER_E_STATUS_POS]= "E_status";
		labels[NETMASTER_F_ACCELX_POS]= "F_accelx";
		labels[NETMASTER_F_ACCELY_POS]= "F_accely";
		labels[NETMASTER_F_ACCELZ_POS]= "F_accelz";
		labels[NETMASTER_F_GYROX_POS]= "F_gyrox";
		labels[NETMASTER_F_GYROY_POS]= "F_gyroy";
		labels[NETMASTER_F_GYROZ_POS]= "F_gyroz";
		labels[NETMASTER_F_PRESSURE_POS]= "F_pressure";
		labels[NETMASTER_F_STATUS_POS]= "F_status";
		labels[NETMASTER_G_ACCELX_POS]= "G_accelx";
		labels[NETMASTER_G_ACCELY_POS]= "G_accely";
		labels[NETMASTER_G_ACCELZ_POS]= "G_accelz";
		labels[NETMASTER_G_GYROX_POS]= "G_gyrox";
		labels[NETMASTER_G_GYROY_POS]= "G_gyroy";
		labels[NETMASTER_G_GYROZ_POS]= "G_gyroz";
		labels[NETMASTER_G_PRESSURE_POS]= "G_pressure";
		labels[NETMASTER_G_STATUS_POS]= "G_status";
		labels[NETMASTER_H_ACCELX_POS]= "H_accelx";
		labels[NETMASTER_H_ACCELY_POS]= "H_accely";
		labels[NETMASTER_H_ACCELZ_POS]= "H_accelz";
		labels[NETMASTER_H_GYROX_POS]= "H_gyrox";
		labels[NETMASTER_H_GYROY_POS]= "H_gyroy";
		labels[NETMASTER_H_GYROZ_POS]= "H_gyroz";
		labels[NETMASTER_H_PRESSURE_POS]= "H_pressure";
		labels[NETMASTER_H_STATUS_POS]= "H_status";
		labels[NETMASTER_SYSTEM_TIME_POS]="sys_time";
	};

	 static std::string GetLabelsForLog() 
 	{
		std::string labels[NETMASTER_STRUCT_DEVICE_FIELD_COUNT];
		GetLabels(labels);
		std::string outputString;
		for(int index=NETMASTER_STATE_TIME_POS;index<NETMASTER_STRUCT_DEVICE_FIELD_COUNT;index++)
		{
			 outputString=outputString +labels[index]+",";
		}
		return outputString;
	};
}; 
#endif ////NETMASTER_STRUCT_H
