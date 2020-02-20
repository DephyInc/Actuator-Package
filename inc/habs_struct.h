#ifndef HABS_STRUCT_H
#define HABS_STRUCT_H

struct HabsoluteState
{
	int habsolute;
	int id;
	int timestamp;
	int ankleAngle;
	int ankleVelocity;
	int adc[8];
	int genvar[4];
	int status;
};

#endif // HABS_STRUCT_H

