#include "leaderfollower.h"
#include "readOnly.cpp.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "device_wrapper.h"

using namespace std;
using namespace std::literals::chrono_literals;

void runLeaderFollower( int devId0, int devId1, bool *shouldQuit)
{
	FxError errCode[2];

	ActPackState readData[2];
	
	//
	// Start streaming the data
	//
	errCode[0] = fxStartStreaming(devId0, 200, true);
	errCode[1] = fxStartStreaming(devId1, 200, true);
	if(errCode[0] != FxSuccess || errCode[1] != FxSuccess)
	{
		cout << "Streaming failed ..." << endl;
		return;
	}

	//
	// Find the initial angles
	//
	int initialAngle[2] = {-1, -1};
	
	errCode[0] = fxReadDevice(devId0, &readData[0]);
	errCode[1] = fxReadDevice(devId1, &readData[1]);
	if(errCode[0] != FxSuccess || errCode[1] != FxSuccess)
	{
		cout << "Reading failed ..." << endl;
		return;
	}

	initialAngle[0] = readData[0].encoderAngle;
	initialAngle[1] = readData[1].encoderAngle;

	cout << "Initial angles are: " << initialAngle[0] << ", " << initialAngle[1] << endl;

	//
	// Setup both devices
	//
	fxSetGains(devId0, 100, 20, 0, 0, 0);
	fxSendMotorCommand(devId0, FxCurrent, 0);

	fxSetGains(devId1, 50, 3, 0, 0, 0);
	fxSendMotorCommand(devId1, FxPosition, initialAngle[1]);

	int diff  = 0;
	int angle[2] = {0};
	while(! *shouldQuit)
	{
		//
		// Read device 0 angle
		//
		this_thread::sleep_for(50ms);
		
		errCode[0] = fxReadDevice(devId0, &readData[0]);
		if(errCode[0] != FxSuccess)
		{
			cout << "Reading failed ..." << endl;
			return;
		}
		angle[0] = readData[0].encoderAngle;

		//
		// Set device 1 angle
		//
		diff = angle[0] - initialAngle[0];
		fxSendMotorCommand(devId1, FxPosition, initialAngle[1] + diff);
		
		this_thread::sleep_for(50ms);

		clearScreen();
		
		errCode[0] = fxReadDevice(devId0, &readData[0]);
		errCode[1] = fxReadDevice(devId1, &readData[1]);
		if(errCode[0] != FxSuccess || errCode[1] != FxSuccess)
		{
			cout << "Reading failed ..." << endl;
			return;
		}

		cout << "Device " << devId0 << " following device " << devId1 << endl;
		cout << "Device [  " << devId0 << " ]" << endl;
		displayState(readData[0]);
		cout << "Device [ " << devId1 << " ]" << endl;
		displayState(readData[1]);

	}

}
