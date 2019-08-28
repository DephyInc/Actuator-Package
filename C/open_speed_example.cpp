#include "open_speed_example.h"
#include "cppFlexSEA.h"
#include "cmd-ActPack.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
using namespace std;
using namespace std::literals::chrono_literals;

static int varsToStream[] = {
    FX_RIGID_STATETIME,
    FX_RIGID_ENC_ANG,
    FX_RIGID_MOT_VOLT
};

static const int SIZEVARSTOSTREAM = sizeof(varsToStream) /sizeof(int);
static string varLabels[] = {
    "State time",
    "Enc Angle",
    "Motor Voltage"
};


void runOpenSpeed( int devId, bool *shouldQuit)
{
    //
    // Set up the variables to monitor
    //
    fxSetStreamVariables(devId, varsToStream, SIZEVARSTOSTREAM);

    //
    // Start reading the data from the FlexSEA device
    //
    if( ! fxStartStreaming( devId, 100, false, 0) )
    {
        cout << "Streaming failed..." << endl;
        exit(2);
    }

    cout << "Setting open control..." << endl;

    setControlMode(devId, CTRL_OPEN);
    const int numSteps     = 100;
    int maxVoltage   = 3000;
    int numTimes     = 2;
    int mV           = 0;
    for( int time = 0; time < numTimes; ++time)
    {
        for(int i= 0; i < numSteps; ++i)
        {
            this_thread::sleep_for(100ms);
            mV = maxVoltage * (i*1.0 / numSteps);
            setMotorVoltage(devId, mV);
            clearScreen();
            cout << "Ramping up open controller..." << endl;
            printDevice( devId, varsToStream, varLabels, SIZEVARSTOSTREAM);
            if(*shouldQuit)
                break;
        }

        this_thread::sleep_for(500ms);
        for( int j = 0; j < numSteps; ++j)
        {
            this_thread::sleep_for(100ms);
            mV = maxVoltage * ((numSteps - j)*1.0 / numSteps);
            setMotorVoltage(devId, mV);
            clearScreen();
			cout << "Ramping down open controller..." << endl;
            printDevice( devId, varsToStream, varLabels, SIZEVARSTOSTREAM);
            if(*shouldQuit)
                break;
        }

        if(*shouldQuit)
            break;
    }

    this_thread::sleep_for(100ms);
    setMotorVoltage(devId, 0);
    this_thread::sleep_for(5ms);
    setControlMode(devId, CTRL_NONE);
    fxStopStreaming(devId);
}

