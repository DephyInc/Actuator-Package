#include "cppFlexSEA.h"
#include "two_dev_position_example.h"

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
    FX_RIGID_MOT_VOLT
   };

static string varLabels[] = {
    "State time",
    "Accel X", "Accel Y", "Accel Z",
    "Gyro X",  "Gyro Y",  "Gyro Z",
    "Enc Angle",
    "Motor Voltage"
};
static const int VARSTOSTREAMSIZE = sizeof(varsToStream) / sizeof(int);


void runTwoDevicePositionControl(int devId0, int devId1, bool* shouldQuit)
{
    uint8_t streamSuccess0, streamSuccess1;
    uint8_t success[VARSTOSTREAMSIZE];

    //
    // Set up the variables to monitor
    //
    fxSetStreamVariables(devId0, varsToStream, VARSTOSTREAMSIZE );
    fxSetStreamVariables(devId1, varsToStream, VARSTOSTREAMSIZE );

    //
    // Start streaming the data
    //
    streamSuccess0 = fxStartStreaming( devId0, 100, false, 0);
    streamSuccess1 = fxStartStreaming( devId1, 100, false, 0);
    if( ! streamSuccess0 || ! streamSuccess1)
    {
        cout << "Streaming failed ..." << endl;
        exit(2);
    }

    //
    // Find the initial angle
    //
    int timeout       = 100;
    int initialAngle0 = -1;
    int initialAngle1 = -1;
    int *retData;
    while( timeout > 0)
    {
        retData = fxReadDevice(devId0, varsToStream, success, VARSTOSTREAMSIZE);
        if( success[7])
        {
            initialAngle0 = retData[7];
            break;
        }
        else
        {
            --timeout;
        }
        if( !timeout )
        {
            cout << "Timed out waiting for valid encoder reading" << endl;
            this_thread::sleep_for(200ms);
            fxStopStreaming(devId0);
            fxStopStreaming(devId1);
            return;
        }
    }

    timeout = 100;
    while( timeout > 0)
    {
        retData = fxReadDevice(devId1, varsToStream, success, VARSTOSTREAMSIZE);
        if( success[7])
        {
            initialAngle1 = retData[7];
            break;
        }
        else
        {
            --timeout;
        }
        if( !timeout )
        {
            cout << "Timed out waiting for valid encoder reading" << endl;
            this_thread::sleep_for(200ms);
            fxStopStreaming(devId0);
            fxStopStreaming(devId1);
            return;
        }
    }

    cout << "Initial angle " << initialAngle0 << endl;

    //
    // Set position controller for both devices
    //
    setPosition(devId0, initialAngle0);
    setControlMode(devId0, CTRL_POSITION);
    setPosition(devId0, initialAngle0);
    setGains(devId0, 50, 3, 0, 0);

    setPosition(devId1, initialAngle1);
    setControlMode(devId1, CTRL_POSITION);
    setPosition(devId1, initialAngle1);
    setGains(devId1, 50, 3, 0, 0);

    while(! *shouldQuit)
    {
        this_thread::sleep_for(200ms);
        clearScreen();

        cout << "Holding position, two devices: " << endl;
        printDevice( devId0, varsToStream, varLabels, VARSTOSTREAMSIZE);
        cout << endl;
        printDevice( devId1, varsToStream, varLabels, VARSTOSTREAMSIZE);
    }

    cout << "Turning off position control..." << endl;
    setControlMode(devId0, CTRL_NONE);
    setControlMode(devId1, CTRL_NONE);

    //
    // Let the command process before we stop streaming
    //
    this_thread::sleep_for(200ms);
    fxStopStreaming(devId0);
    fxStopStreaming(devId1);

    return;
}
