#include "read_all_example.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "device_wrapper.h"

using namespace std;
using namespace std::literals::chrono_literals;

void displayState(ActPackState& state)
{
/*	cout << "Device time: \t" << state.state_time << endl;
	cout << "imu: " << state.accelx << ", \t" << state.accely << ", " << state.accelz << endl;
	cout << state.gyrox << ", " << state.gyroy << ", " << state.gyroz << endl;
	cout << "motor: " << state.mot_ang << " angle, \t" << \
		state.mot_cur << " mA, " <<\
		state.mot_volt << " mV" << endl;
	cout <<"battery: " << state.batt_volt << " mV, " << \
		state.batt_curr << " mA, " << \
		state.temperature << " C" << endl << endl;*/

    //get the Log labels
    char labels[ACTPACK_STRUCT_DEVICE_FIELD_COUNT][ACTPACK_LABEL_MAX_CHAR_LENGTH];
    ActPackGetLabels(labels);

    //display everything starting from the state time.  We don't need the id...
    for(int index=ACTPACK_STATE_TIME_POS;index<ACTPACK_STRUCT_DEVICE_FIELD_COUNT;index++)
    {
        //let's put 3 items per line with tabs between them
        char dataString[ACTPACK_LABEL_MAX_CHAR_LENGTH+15];
        strcpy(dataString,"");

        sprintf(dataString,"%s:%i",labels[index],state.deviceData[index]);

        //this puts 3 items per row
        if(index%3==0 || index==0)
        {
            cout <<"\n"<<dataString;
        } else//all the others get a tab or 2 depending on length
        {
            char prevDataString[ACTPACK_LABEL_MAX_CHAR_LENGTH+15];
            strcpy(prevDataString,"");

            //let's check how long the previous string was. if it was short, we need an extra tab
            sprintf(prevDataString,"%s:%i",labels[index-1],state.deviceData[index-1]);
            if(strnlen(prevDataString, ACTPACK_LABEL_MAX_CHAR_LENGTH+10)<15)
            {
                cout<<"\t";
            }
            cout<<"\t"<<dataString;
        }
        if(index%6==0)
        {
            //cout<<"\n";
        }

    }
    cout<<"\n\n\n";

}

void init_actPackState(ActPackState* state)
{
	state->rigid = 0;
	state->id = 0;
	state->state_time = 0;
	state->accelx = 0;
	state->accely = 0;
	state->accelz = 0;
	state->gyrox = 0;
	state->gyroy = 0;
	state->gyroz = 0;
	state->mot_ang = 0;
	state->mot_vel = 0;
	state->mot_acc = 0;
	state->mot_cur = 0;
	state->mot_volt = 0;
	state->batt_volt = 0;
	state->batt_curr= 0;
	state->temperature = 0;
	state->status_mn = 0;
	state->status_ex = 0;
	state->status_re = 0;
	state->genvar_0=0;
    state->genvar_1=0;
    state->genvar_2=0;
    state->genvar_3=0;
    state->genvar_4=0;
    state->genvar_5=0;
    state->genvar_6=0;
    state->genvar_7=0;
    state->genvar_8=0;
    state->genvar_9=0;
	state->ank_ang = 0;
	state->ank_vel = 0;
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
    while(!(*shouldQuit))
    {
	this_thread::sleep_for(10ms);
        clearScreen();
	fxReadDevice(devId, &exoState);
	
	displayState(exoState);

        cout << endl;
    }
    fxStopStreaming(devId);
}
