#include "fxUtil.h"

void printDevice(struct ActPackState *actpack)
{
    cout<<"[ Printing Actpack ]\n";
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
    cout<<"[ Printing Exo/Actpack Plus ]\n";
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
    cout<<"[ Printing Exo/Actpack Plus ]\n";
    cout<<"State time:           "<<netMasterState->state_time<<"\n";
    cout<<"Accel X:              "<<netMasterState->genvar_0<<"\n";
    cout<<"Accel Y:              "<<netMasterState->genvar_1<<"\n";
    cout<<"Accel Z:              "<<netMasterState->genvar_2<<"\n";
    cout<<"Gyro X:               "<<netMasterState->genvar_3<<"\n";
    cout<<"Gyro Y:               "<<netMasterState->status<<"\n";
    cout<<"Gyro Z:               "<<netMasterState->a_accelx<<"\n";
    cout<<"Motor Angle:          "<<netMasterState->a_gyrox<<"\n";
    cout<<"Motor Voltage (mV):   "<<netMasterState->mot_volt<<"\n";
    cout<<"Battery Current (mA): "<<netMasterState->batt_curr<<"\n";
    cout<<"Battery Voltage (mV): "<<netMasterState->batt_volt<<"\n";
    cout<<"Battery Temp (C):     "<<netMasterState->temperature<<"\n";
    cout<<"GenVar 0:             "<<netMasterState->a_accelx"\n";
    cout<<"GenVar 1:             "<<netMasterState->a_gyrox<<"\n";
    cout<<"GenVar 2:             "<<netMasterState->b_accelx<<"\n";
    cout<<"GenVar 3:             "<<netMasterState->b_gyrox<<"\n";
    cout<<"GenVar 4:             "<<netMasterState->c_accelx<<"\n";
    cout<<"GenVar 5:             "<<netMasterState->c_gyrox<<"\n";
    cout<<"GenVar 6:             "<<netMasterState->d_accelx<<"\n";
    cout<<"GenVar 7:             "<<netMasterState->d_gyrox<<"\n";
    cout<<"GenVar 8:             "<<netMasterState->genvar_8<<"\n";
    cout<<"GenVar 9:             "<<netMasterState->genvar_9<<"\n";
}