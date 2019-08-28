#include "hold_position_example.h"
#include "cppFlexSEA.h"
#include "cmd-ActPack.h"
#include <iostream>
#include <chrono>
#include <thread>
#include "utils.h"
using namespace std;
using namespace std::literals::chrono_literals;

static string labels[] = {
    "State time",
    "accel x", "accel y", "accel z",
    "gyro x",  "gyro y",  "gyro z",
    "encoder angle",
    "motor voltage"
};

static int varsToStream[] = {
    FX_RIGID_STATETIME,
    FX_RIGID_ACCELX, FX_RIGID_ACCELY, FX_RIGID_ACCELZ,
    FX_RIGID_GYROX,  FX_RIGID_GYROY,  FX_RIGID_GYROZ,
    FX_RIGID_ENC_ANG,
    FX_RIGID_MOT_VOLT
};
static const int VARSTOSTREAMSIZE = sizeof(varsToStream) / sizeof(int);

void runHoldPosition(int devId, bool *shouldQuit)
{
    int *retData;
    uint8_t success[VARSTOSTREAMSIZE];

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
    // wait for device initial position to update
    //
    std::this_thread::sleep_for(400ms);

    int timeout = 100;
    int initialAngle = 0;
    success[7]       = false;
    while( !success[7] )
    {
        retData = fxReadDevice(devId, varsToStream, success, VARSTOSTREAMSIZE);
        if(success[7])
        {
            initialAngle = retData[7];
            break;
        }
        --timeout;
        this_thread::sleep_for(100ms);
    }
    if(timeout == 0)
    {
        cout << "Timeout out waiting for initial encoder angle" << endl;

        // Clean up
        this_thread::sleep_for(100ms);
        fxStopStreaming(devId);

        return;
    }

    //
    // Set the motor control
    //
    setPosition(devId, initialAngle);
    setControlMode(devId, CTRL_POSITION);
    setPosition(devId, initialAngle);
    setGains(devId, 50, 3, 0, 0);

    while(!(*shouldQuit))
    {
        std::this_thread::sleep_for(50ms);
		clearScreen();
		cout << "Holding position " << initialAngle << endl;
        printDevice(devId, varsToStream, labels, VARSTOSTREAMSIZE);
    }

    setControlMode(devId, CTRL_NONE);
    this_thread::sleep_for(100ms);
    fxStopStreaming(devId);
}
