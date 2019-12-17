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
	cout << "Device time: " << state.timestamp << endl;
	cout << "imu: " << state.accelx << ", " << state.accely << ", " << state.accelz << endl;
	cout << state.gyrox << ", " << state.gyroy << ", " << state.gyroz << endl;
	cout << "motor: " << state.encoderAngle << " angle, " << \
		state.motorCurrent << " mA, " <<\
		state.motorVoltage << " mV" << endl;
	cout <<"battery: " << state.batteryVoltage << " mV, " << \
		state.batteryCurrent << " mA, " << \
		state.batteryTemp << " C" << endl << endl; 
}

void init_actPackState(ActPackState* state)
{
	state->rigid = 0;
	state->id = 0;
	state->timestamp = 0;
	state->accelx = 0;
	state->accely = 0;
	state->accelz = 0;
	state->gyrox = 0;
	state->gyroy = 0;
	state->gyroz = 0;
	state->encoderAngle = 0;
	state->encoderVelocity = 0;
	state->encoderAccel = 0;
	state->motorCurrent = 0;
	state->motorVoltage = 0;
	state->batteryVoltage = 0;
	state->batteryCurrent = 0;
	state->batteryTemp = 0;
	state->deviceStatus = 0;
	state->motorStatus = 0;
	state->batteryStatus = 0;
	state->genVar[10] = {0};
	state->ankleAngle = 0;
	state->ankleVelocity = 0;
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
