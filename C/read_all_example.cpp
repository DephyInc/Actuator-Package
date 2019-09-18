#include "read_all_example.h"
#include "cppFlexSEA.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "flexsea_sys_def.h"

using namespace std;
using namespace std::literals::chrono_literals;

static int varsToStream[] = {

    FX_RIGID_STATETIME,
    FX_RIGID_ACCELX,	FX_RIGID_ACCELY,	FX_RIGID_ACCELZ,
    FX_RIGID_GYROX,  	FX_RIGID_GYROY,  	FX_RIGID_GYROZ,
    FX_RIGID_ENC_ANG,
    FX_RIGID_GEN_VAR_9,                     // Var9 => FX_RIGID_ANKLE_ANG,
    FX_RIGID_MOT_VOLT
   };

static string varLabels[] = {
    "State time",
    "Accel X", "Accel Y", "Accel Z",
    "Gyro X",  "Gyro Y",  "Gyro Z",
    "Enc Angle",
    "Ankle Angle",
    "Motor Voltage"
};
static const int VARSTOSTREAMSIZE = sizeof(varsToStream) / sizeof(int);

void runReadAll( int devId, bool *shouldQuit)
{
    cout << "\n Running the READ-ALL Demo\n" << endl;
    //
    // Set up the variables to monitor
    //
    fxSetStreamVariables(devId, varsToStream, VARSTOSTREAMSIZE );

    //
    // Start streaming the data
    //
    if( ! fxStartStreaming( devId, 100, false, 0) )
    {
        cout << "Streaming failed ..." << endl;
        exit(2);
    }

    //
    // Read and display the data
    //
    while(!(*shouldQuit))
    {
        this_thread::sleep_for(50ms);
        clearScreen();
		printDevice( devId, varsToStream, varLabels, VARSTOSTREAMSIZE);
        cout << endl;
    }
    fxStopStreaming(devId);
}
