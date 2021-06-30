#ifndef FW_CMD_EXO_CONTROL_STRUCT_H
#define FW_CMD_EXO_CONTROL_STRUCT_H

//Defined in flexsea_cmd_exo_control.h
//Copied here to make it available to the GUI

enum exoPowerEnum
{
	EXO_POWER_OFF 		= 0,
	EXO_POWER_ON 		= 1,
	EXO_POWER_UNKNOWN	= 2		//Unknown, or Do Not Change
};

enum exoTrialEnum
{
	EXO_TRIAL_STOP		= 0,
	EXO_TRIAL_START 	= 1,
	EXO_TRIAL_UNKNOWN	= 2		//Unknown, or Do Not Change
};

struct exoCommandStruct
{
	//Power On/Off
	enum exoPowerEnum powerWrite;	//Write to device
	enum exoPowerEnum powerRead;	//Read from device

	//Trial start/stop
	enum exoTrialEnum trialWrite;	//Write to device
	enum exoTrialEnum trialRead;	//Read from device
};

#endif // FW_CMD_EXO_CONTROL_STRUCT_H
