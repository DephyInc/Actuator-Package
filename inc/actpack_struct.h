#ifndef ACTPACK_STRUCT_H
#define ACTPACK_STRUCT_H

struct ActPackState
{
	int rigid;
	int id;
	int timestamp;
	int accelx;
	int accely;
	int accelz;
	int gyrox;
	int gyroy;
	int gyroz;
	int encoderAngle;
	int encoderVelocity;
	int encoderAccel;
	int motorCurrent;
	int motorVoltage;
	int batteryVoltage;
	int batteryCurrent;
	int batteryTemp;
	int deviceStatus;
	int motorStatus;
	int batteryStatus;
	int genVar[10];
	int ankleAngle;
	int ankleVelocity;
};



#endif // ACTPACK_STRUCT_H

