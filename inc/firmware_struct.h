#ifndef FW_VERSION_STRUCT_H
#define FW_VERSION_STRUCT_H

//Defined in firmware_version.h

typedef enum
{
	FW_VER_MN = 0,
	FW_VER_EX,
	FW_VER_RE,
	FW_VER_HA,
	FW_VER_SIZE	//Used to define arrays
}
FirmwareVersionIndex;

struct FirmwareVersionStruct
{
	uint32_t mcu[FW_VER_SIZE];
};

#endif // FW_VERSION_STRUCT_H
