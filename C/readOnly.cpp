#include "readOnly.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "device_wrapper.h"

#define TIME_STEP .1 //in seconds
#define TIME 8

using namespace std;
using namespace std::literals::chrono_literals;

void displayState(ActPackState& state)
{

    //get the Log labels
    char labels[ACTPACK_STRUCT_DEVICE_FIELD_COUNT][ACTPACK_LABEL_MAX_CHAR_LENGTH];
    ActPackGetLabels(labels);
    char dataString[ACTPACK_LABEL_MAX_CHAR_LENGTH+15];//the label plus the colon and data being displayed

    //display everything starting from the state time.  We don't need the id...
    for(int index=ACTPACK_STATE_TIME_POS;index<ACTPACK_STRUCT_DEVICE_FIELD_COUNT;index++)
    {
        strcpy(dataString,"");

        if(strnlen(labels[index],ACTPACK_LABEL_MAX_CHAR_LENGTH)<=6)
        {
            sprintf(dataString,"%s:\t\t%i\n",labels[index],state.deviceData[index]);
        }else if((strnlen(labels[index],ACTPACK_LABEL_MAX_CHAR_LENGTH)<=12))
        {
            sprintf(dataString,"%s:\t%i\n",labels[index],state.deviceData[index]);
        } else
        {
            sprintf(dataString,"%s:\t%i\n",labels[index],state.deviceData[index]);
        }
        cout<<dataString;
    }
    cout<<"\n\n";

}

void init_actPackState(ActPackState* state)
{
    //make a temp buffer of all zeros to load
    uint32_t tempDeviceStateBuffer[ACTPACK_STRUCT_DEVICE_FIELD_COUNT];
    memset(tempDeviceStateBuffer,0,sizeof(uint32_t)*ACTPACK_STRUCT_DEVICE_FIELD_COUNT);

    //set struct with the data from the zero buffer
    ActPackSetData(state,tempDeviceStateBuffer,0);

}

void runReadAll(int devId, bool *shouldQuit)
{
    cout << "\n Running the READ-ALL Demo\n" << endl;
    //
    // Start streaming the data
    //
    if(fxStartStreaming(devId, 200, true) != FxSuccess )
    {
        cout << "Streaming failed ..." << endl;
        return;
    }

    //
    // Read and display the data
    //
    ActPackState exoState;
    init_actPackState(&exoState);
    //while(!(*shouldQuit))
    int reps=TIME/TIME_STEP;
    for(int index=0;index<reps ;index++)
    {

	this_thread::sleep_for(100ms);
        clearScreen();
	fxReadDevice(devId, &exoState);
	
	displayState(exoState);

        cout << endl;
    }
    fxStopStreaming(devId);
}
