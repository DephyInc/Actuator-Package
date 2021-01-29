#ifndef I2T_STRUCT_H
#define I2T_STRUCT_H

// Defined in i2t-current-limit.h
// TODO: Unify

#include <cstdint>

struct i2tVals
{
	//Variables exchanged during calibration:	
	uint16_t leak;
	uint32_t limit;
	uint16_t nonLinThreshold;	
	uint8_t config;	//Contains shift and UseNL
	
	//Generated from above:
	uint8_t shift;	
	uint8_t useNL;
	uint32_t warning;	
};

#endif // I2T_STRUCT_H
