#ifndef BMS_STRUCT_H
#define BMS_STRUCT_H

struct BMSState
{
	int bms;
	int id;
	int timestamp;
	int cellVoltage[9];
	int status;
	int current;
	int timer;
	int balancing;
	int stackVoltage;
	int packImbalance;
	int temperature[3];
	int genvar[4];
};

#endif // BMS_STRUCT_H

