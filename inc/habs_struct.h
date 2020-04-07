#ifndef HABS_STRUCT_H
#define HABS_STRUCT_H

#include "Habsolute_device_spec.h"
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

    ///Enum defines the location of each variable in the device state buffer as defined by the device spec
/*    enum HabsoluteDeviceStateBufferEnum
    {
        HABS_POS        =0,
        HABS_ID         =1,
        HABS_STATE_TIME =2,
        HABS_ANK_ANG    =3,
        HABS_ANK_VEL    =4,
        HABS_ADC_0      =5,
        HABS_ADC_1      =6,
        HABS_ADC_2      =7,
        HABS_ADC_3      =8,
        HABS_ADC_4      =9,
        HABS_ADC_5      =10,
        HABS_ADC_6      =11,
        HABS_ADC_7      =12,
        HABS_GENVAR_0   =13,
        HABS_GENVAR_1   =14,
        HABS_GENVAR_2   =15,
        HABS_GENVAR_3   =16,
        HABS_STATUS     =17
    };*/

	void setData(uint32_t _deviceStateBuffer[])
    {
        habsolute = _deviceStateBuffer[HABSOLUTE_HABSOLUTE_POS];
        id = _deviceStateBuffer[HABSOLUTE_ID_POS];
        timestamp = _deviceStateBuffer[HABSOLUTE_STATE_TIME_POS];
        ankleAngle = _deviceStateBuffer[HABSOLUTE_ANK_ANG_POS];
        ankleVelocity = _deviceStateBuffer[HABSOLUTE_ANK_VEL_POS];
        adc[0] = _deviceStateBuffer[HABSOLUTE_ADC_0_POS];
        adc[1] = _deviceStateBuffer[HABSOLUTE_ADC_1_POS];
        adc[2] = _deviceStateBuffer[HABSOLUTE_ADC_2_POS];
        adc[3] = _deviceStateBuffer[HABSOLUTE_ADC_3_POS];
        adc[4] = _deviceStateBuffer[HABSOLUTE_ADC_4_POS];
        adc[5] = _deviceStateBuffer[HABSOLUTE_ADC_5_POS];
        adc[6] = _deviceStateBuffer[HABSOLUTE_ADC_6_POS];
        adc[7] = _deviceStateBuffer[HABSOLUTE_ADC_7_POS];
        genvar[0] = _deviceStateBuffer[HABSOLUTE_GENVAR_0_POS];
        genvar[1] = _deviceStateBuffer[HABSOLUTE_GENVAR_1_POS];
        genvar[2] = _deviceStateBuffer[HABSOLUTE_GENVAR_2_POS];
        genvar[3] = _deviceStateBuffer[HABSOLUTE_GENVAR_3_POS];
        status = _deviceStateBuffer[HABSOLUTE_STATUS_POS];
    }

    ///function places data from the struct into a stringstream
    void sendToStream(std::stringstream& ss)
    {
        ss << habsolute << "," ;
        ss << id << ",";
        ss << timestamp << ",";
        ss << ankleAngle << ",";
        ss << ankleVelocity << ",";
        ss << adc[0] << ",";
        ss << adc[1] << ",";
        ss << adc[2] << ",";
        ss << adc[3] << ",";
        ss << adc[4] << ",";
        ss << adc[5] << ",";
        ss << adc[6] << ",";
        ss << adc[7] << ",";
        ss << genvar[0] << ",";
        ss << genvar[1] << ",";
        ss << genvar[2] << ",";
        ss << genvar[3] << ",";
        ss << status << ",";
    }
};


#endif // HABS_STRUCT_H

