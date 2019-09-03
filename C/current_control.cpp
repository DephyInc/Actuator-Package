#include "read_all_example.h"
#include "cppFlexSEA.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "flexsea_sys_def.h"

using namespace std;
using namespace std::literals::chrono_literals;

static string labels[] = {
    "State time",
    "encoder angle",
    "motor current"
};

static int varsToStream[] = {
    FX_RIGID_STATETIME,
    FX_RIGID_ENC_ANG,
    FX_RIGID_MOT_CURR
};

static const int VARSTOSTREAMSIZE = sizeof(varsToStream) / sizeof(int);

void runCurrentControl(int devId, bool* shouldQuit)
{
    int     holdCurrent = 500;
    int     streamSuccess = 0;
    int     *retData;
    uint8_t success[MAX_FLEXSEA_VARS];

    fxSetStreamVariables(devId, varsToStream, VARSTOSTREAMSIZE);
    streamSuccess = fxStartStreaming(devId, 100, false, 0);
    if(! streamSuccess)
    {
        cout << "Streaming Failed..." << endl;
        exit(2);
    }

    cout << "Setting controller to current..." << endl;
    setControlMode(devId, CTRL_CURRENT);
    setGains(devId, 100, 20, 0, 0);
    setMotorCurrent(devId, holdCurrent);     // Start the current, holdCurrent is in mA

    int n = 0;
    while(! *shouldQuit)
    {
        this_thread::sleep_for(100ms);
        clearScreen();                              //Clear terminal (Win)
        printDevice(devId, varsToStream, labels, VARSTOSTREAMSIZE);
        cout << "Holding Current: "<< holdCurrent << " mA" << endl;
    }

    cout << "Turning off current control..." << endl;

    //
    // Ramp down first
    //
    n = 50;
    for(int i =0; i < n; ++i)
    {
        setMotorCurrent(devId, holdCurrent * (n-i)/n);
        this_thread::sleep_for(40ms);
    }

    //
    // Wait for motor to spin down
    //
    cout << "Waiting for motor to spin down..." << endl;
    setMotorCurrent(devId, 0);

    // Read "last" encode angle
    int lastAngle = 0;
    retData = fxReadDevice(devId, varsToStream, success, VARSTOSTREAMSIZE);
    if( success[1] )
        lastAngle = retData[1];
    this_thread::sleep_for(200ms);

    // Read "Current" encoder angle
    int currentAngle = 0;
    retData = fxReadDevice(devId, varsToStream, success, VARSTOSTREAMSIZE);
    if( success[1] )
        currentAngle = retData[1];
    this_thread::sleep_for(200ms);

    // Wait for motor to stop spinning
    while( abs(currentAngle - lastAngle) > 100)
    {
        this_thread::sleep_for(200ms);
        lastAngle    = currentAngle;
        retData = fxReadDevice(devId, varsToStream, success, VARSTOSTREAMSIZE);
        if( success[1] )
        {
            currentAngle = retData[1];
        }
    }

    setControlMode(devId, CTRL_NONE);
    fxStopStreaming(devId);
}

