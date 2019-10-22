#include "open_speed_example.h"
#include "device_wrapper.h"
#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "read_all_example.h"

using namespace std;
using namespace std::literals::chrono_literals;

void runOpenSpeed(int devId, bool *shouldQuit)
{
	if(fxStartStreaming(devId, true) != ESuccess )
	{
		cout << "Streaming failed..." << endl;
		exit(2);
	}

	cout << "Setting open control..." << endl;

	fxSetGains(devId, 100, 30, 0, 0);
	const int numSteps	 = 100;
	int maxVoltage   = 3000;
	int numTimes	 = 2;
	int mV		   = 0;
	ExoState readData;
	for( int time = 0; time < numTimes; ++time)
	{
		for(int i= 0; i < numSteps; ++i)
		{
			this_thread::sleep_for(100ms);
			mV = maxVoltage * (i*1.0 / numSteps);
			fxSendMotorCommand(devId, EVoltage, mV);
			clearScreen();
			cout << "Ramping up open controller..." << endl;
				

			if (fxReadDevice(devId, &readData) == ESuccess)
			{

				display_state(readData);
			}
			else
			{
				cout << "Failed to read device" << endl;
			}

			if(*shouldQuit)
				break;
		}

		this_thread::sleep_for(100ms);
		for( int j = 0; j < numSteps; ++j)
		{
			this_thread::sleep_for(100ms);
			mV = maxVoltage * ((numSteps - j)*1.0 / numSteps);
			fxSendMotorCommand(devId, EVoltage, mV);
			clearScreen();
			cout << "Ramping down open controller..." << endl;
			if (fxReadDevice(devId, &readData) == ESuccess)
			{

				display_state(readData);
			}
			else
			{
				cout << "Failed to read device" << endl;
			}

			if(*shouldQuit)
				break;
		}

		if(*shouldQuit)
			break;
	}

}

