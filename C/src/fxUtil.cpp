#include "fxUtil.h"

void printDevice(struct ActPackState *actpack)
{
	cout<<"[ Printing ActPack ]\n";
	cout<<"State time:           "<<actpack->state_time<<"\n";
	cout<<"Accel X:              "<<actpack->accelx<<"\n";
	cout<<"Accel Y:              "<<actpack->accely<<"\n";
	cout<<"Accel Z:              "<<actpack->accelz<<"\n";
	cout<<"Gyro X:               "<<actpack->gyrox<<"\n";
	cout<<"Gyro Y:               "<<actpack->gyroy<<"\n";
	cout<<"Gyro Z:               "<<actpack->gyroz<<"\n";
	cout<<"Motor Angle:          "<<actpack->mot_ang<<"\n";
	cout<<"Motor Voltage (mV):   "<<actpack->mot_volt<<"\n";
	cout<<"Battery Current (mA): "<<actpack->batt_curr<<"\n";
	cout<<"Battery Voltage (mV): "<<actpack->batt_volt<<"\n";
	cout<<"Battery Temp (C):     "<<actpack->temperature<<"\n";
}

void printDevice(struct ExoState *exoState)
{
	cout<<"[ Printing Exo/ActPack Plus ]\n";
	cout<<"State time:           "<<exoState->state_time<<"\n";
	cout<<"Accel X:              "<<exoState->accelx<<"\n";
	cout<<"Accel Y:              "<<exoState->accely<<"\n";
	cout<<"Accel Z:              "<<exoState->accelz<<"\n";
	cout<<"Gyro X:               "<<exoState->gyrox<<"\n";
	cout<<"Gyro Y:               "<<exoState->gyroy<<"\n";
	cout<<"Gyro Z:               "<<exoState->gyroz<<"\n";
	cout<<"Motor Angle:          "<<exoState->mot_ang<<"\n";
	cout<<"Motor Voltage (mV):   "<<exoState->mot_volt<<"\n";
	cout<<"Battery Current (mA): "<<exoState->batt_curr<<"\n";
	cout<<"Battery Voltage (mV): "<<exoState->batt_volt<<"\n";
	cout<<"Battery Temp (C):     "<<exoState->temperature<<"\n";
	cout<<"GenVar 0:             "<<exoState->genvar_0<<"\n";
	cout<<"GenVar 1:             "<<exoState->genvar_1<<"\n";
	cout<<"GenVar 2:             "<<exoState->genvar_2<<"\n";
	cout<<"GenVar 3:             "<<exoState->genvar_3<<"\n";
	cout<<"GenVar 4:             "<<exoState->genvar_4<<"\n";
	cout<<"GenVar 5:             "<<exoState->genvar_5<<"\n";
	cout<<"GenVar 6:             "<<exoState->genvar_6<<"\n";
	cout<<"GenVar 7:             "<<exoState->genvar_7<<"\n";
	cout<<"GenVar 8:             "<<exoState->genvar_8<<"\n";
	cout<<"GenVar 9:             "<<exoState->genvar_9<<"\n";
}

void printDevice(struct NetMasterState *netMasterState)
{
	cout<<"[ Printing Exo/ActPack Plus ]\n";
	cout<<"State time:           "<<netMasterState->state_time<<"\n";
	cout<<"GenVar[0]:            "<<netMasterState->genvar_0<<"\n";
	cout<<"GenVar[1]:            "<<netMasterState->genvar_1<<"\n";
	cout<<"GenVar[2]:            "<<netMasterState->genvar_2<<"\n";
	cout<<"GenVar[3]:            "<<netMasterState->genvar_3<<"\n";
	cout<<"Status:               "<<netMasterState->status<<"\n";
	cout<<"NetNode 0 - AccelX:   "<<netMasterState->a_accelx<<", accely:  "<<netMasterState->a_accely<<", accelz: "<<netMasterState->a_accelz<<"\n";
	cout<<"NetNode 0 - GyroX:    "<<netMasterState->a_gyrox <<", gyroY:   "<<netMasterState->a_gyroy <<",  gyroZ: "<<netMasterState->a_gyroz<<"\n";
	cout<<"NetNode 1 - AccelX:   "<<netMasterState->b_accelx<<", accely:  "<<netMasterState->b_accely<<", accelz: "<<netMasterState->b_accelz<<"\n";
	cout<<"NetNode 1 - GyroX:    "<<netMasterState->b_gyrox <<", gyroY:   "<<netMasterState->b_gyroy <<",  gyroZ: "<<netMasterState->b_gyroz<<"\n";
	cout<<"NetNode 2 - AccelX:   "<<netMasterState->c_accelx<<", accely:  "<<netMasterState->c_accely<<", accelz: "<<netMasterState->c_accelz<<"\n";
	cout<<"NetNode 2 - GyroX:    "<<netMasterState->c_gyrox <<", gyroY:   "<<netMasterState->c_gyroy <<",  gyroZ: "<<netMasterState->c_gyroz<<"\n";
	cout<<"NetNode 3 - AccelX:   "<<netMasterState->d_accelx<<", accely:  "<<netMasterState->d_accely<<", accelz: "<<netMasterState->d_accelz<<"\n";
	cout<<"NetNode 3 - GyroX:    "<<netMasterState->d_gyrox <<", gyroY:   "<<netMasterState->d_gyroy <<",  gyroZ: "<<netMasterState->d_gyroz<<"\n";
	cout<<"NetNode 4 - AccelX:   "<<netMasterState->e_accelx<<", accely:  "<<netMasterState->e_accely<<", accelz: "<<netMasterState->e_accelz<<"\n";
	cout<<"NetNode 4 - GyroX:    "<<netMasterState->e_gyrox <<", gyroY:   "<<netMasterState->e_gyroy <<",  gyroZ: "<<netMasterState->e_gyroz<<"\n";
	cout<<"NetNode 5 - AccelX:   "<<netMasterState->f_accelx<<", accely:  "<<netMasterState->f_accely<<", accelz: "<<netMasterState->f_accelz<<"\n";
	cout<<"NetNode 5 - GyroX:    "<<netMasterState->f_gyrox <<", gyroY:   "<<netMasterState->f_gyroy <<",  gyroZ: "<<netMasterState->f_gyroz<<"\n";
	cout<<"NetNode 6 - AccelX:   "<<netMasterState->g_accelx<<", accely:  "<<netMasterState->g_accely<<", accelz: "<<netMasterState->g_accelz<<"\n";
	cout<<"NetNode 6 - GyroX:    "<<netMasterState->g_gyrox <<", gyroY:   "<<netMasterState->g_gyroy <<",  gyroZ: "<<netMasterState->g_gyroz<<"\n";
	cout<<"NetNode 7 - AccelX:   "<<netMasterState->h_accelx<<", accely:  "<<netMasterState->h_accely<<", accelz: "<<netMasterState->h_accelz<<"\n";
	cout<<"NetNode 7 - GyroX:    "<<netMasterState->h_gyrox <<", gyroY:   "<<netMasterState->h_gyroy <<",  gyroZ: "<<netMasterState->h_gyroz<<"\n";
}

void printDevice(struct BMSState *bmsState)
{
	cout<<"[ Printing BMS ]\n";
	cout<<"State time:      "<<bmsState->state_time<<"\n";
	cout<<"Cell 0 mV:       "<<bmsState->cells_0_mv<<"\n";
	cout<<"Cell 1 mV:       "<<bmsState->cells_1_mv<<"\n";
	cout<<"Cell 2 mV:       "<<bmsState->cells_2_mv<<"\n";
	cout<<"Cell 3 mV:       "<<bmsState->cells_3_mv<<"\n";
	cout<<"Cell 4 mV:       "<<bmsState->cells_4_mv<<"\n";
	cout<<"Cell 5 mV:       "<<bmsState->cells_5_mv<<"\n";
	cout<<"Cell 6 mV:       "<<bmsState->cells_6_mv<<"\n";
	cout<<"Cell 7 mV:       "<<bmsState->cells_7_mv<<"\n";
	cout<<"Cell 8 mV:       "<<bmsState->cells_8_mv<<"\n";
	cout<<"Current:         "<<bmsState->current<<"\n";
	cout<<"timer:           "<<bmsState->timer<<"\n";
	cout<<"temp 0:          "<<bmsState->temperature_0<<"\n";
	cout<<"temp 1:          "<<bmsState->temperature_1<<"\n";
	cout<<"temp 2:          "<<bmsState->temperature_2<<"\n";
}
