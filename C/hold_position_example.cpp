#include "hold_position_example.h"
#include "read_all_example.h"

#include <iostream>
#include <chrono>
#include <thread>
#include "device_wrapper.h"
#include "utils.h"

using namespace std;
using namespace std::literals::chrono_literals;

void runHoldPosition(int devId, bool *shouldQuit)
{
	ActPackState readData;
	FxError errCode;

	//
	// Start streaming the data
	//
	if(fxStartStreaming( devId, true) != FxSuccess)
	{
		cout << "Streaming failed ..." << endl;
		return;
	}

	//
	// wait for device initial position to update
	//
	std::this_thread::sleep_for(400ms);

	int timeout = 100;
	int initialAngle = 0;
		
	errCode = fxReadDevice(devId, &readData);
	if(errCode != FxSuccess)
	{
		cout << "Reading failed ..." << endl;
		return;
	}
	
	initialAngle = readData._execute._motor_data._motor_angle;

	//
	// Set the motor control
	//
	fxSetGains(devId, 50, 3, 0, 0, 0);
	fxSendMotorCommand(devId, FxPosition, initialAngle);	 

	while(!(*shouldQuit))
	{
		std::this_thread::sleep_for(50ms);
		clearScreen();
		cout << "Holding position " << initialAngle << endl;
	
		errCode = fxReadDevice(devId, &readData);
		if(errCode != FxSuccess)
		{	
			cout << "Reading failed ..." << endl;
			return;
		}
		// Defined in read_all_example.h
		displayState(readData);

	}

}
