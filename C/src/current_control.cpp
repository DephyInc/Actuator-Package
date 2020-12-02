#include "current_control.h"
#include "readOnly.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "device_wrapper.h"

using namespace std;
using namespace std::literals::chrono_literals;

void runCurrentControl(int devId, bool* shouldQuit)
{
	int holdCurrent = 500;
	ActPackState readData;
	FxError errCode;

	errCode = fxStartStreaming(devId, 200, true);
	if(errCode != FxSuccess)
	{
		cout << "Streaming Failed..." << endl;
		return;
	}

	cout << "Setting controller to current..." << endl;
	
	// Start the current, holdCurrent is in mA
	fxSetGains(devId, 100, 20, 0, 0, 0, 0);
	fxSendMotorCommand(devId, FxCurrent, holdCurrent);	 

	int n = 0;
	while(! *shouldQuit)
	{
		this_thread::sleep_for(100ms);
		clearScreen();	                          //Clear terminal (Win)
		
		
		errCode = fxReadDevice(devId, &readData);
		if(errCode != FxSuccess)
		{
			cout << "Reading Failed..." << endl;
			return;
		}


		// displayState deffined in read_all_example.h
		displayState(readData);

		cout << "Holding Current: "<< holdCurrent << " mA" << endl;
	}

	cout << "Turning off current control..." << endl;

	//
	// Ramp down first
	//
	n = 50;
	for(int i =0; i < n; ++i)
	{
		fxSendMotorCommand(devId, FxCurrent, holdCurrent * (n-i)/n);	 
		this_thread::sleep_for(40ms);
	}

	//
	// Wait for motor to spin down
	//
	cout << "Waiting for motor to spin down..." << endl;
	fxSendMotorCommand(devId, FxCurrent, 0);	 

	// Read "last" encode angle
	int lastAngle = 0;
	
	errCode = fxReadDevice(devId, &readData);
	if(errCode != FxSuccess)
	{
		cout << "Reading Failed..." << endl;
		exit(2);
	}

	lastAngle = readData.encoderAngle;
	this_thread::sleep_for(200ms);

	// Read "Current" encoder angle
	int currentAngle = 0;
	
	errCode = fxReadDevice(devId, &readData);
	if(errCode != FxSuccess)
	{
		cout << "Reading Failed..." << endl;
		exit(2);
	}

	currentAngle = readData.encoderAngle;
	this_thread::sleep_for(200ms);

	// Wait for motor to stop spinning
	while( abs(currentAngle - lastAngle) > 100)
	{
	
		lastAngle = currentAngle;
		
		errCode = fxReadDevice(devId, &readData);
		if(errCode != FxSuccess)
		{
			cout << "Reading Failed..." << endl;
			exit(2);
		}
	
		currentAngle = readData.encoderAngle;

	}

}

