#include "open_speed_example.h"
#include "device_wrapper.h"
#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "readOnly.h"

using namespace std;
using namespace std::literals::chrono_literals;

void runOpenSpeed(int devId, bool *shouldQuit)
{
	if(fxStartStreaming(devId, 200, true) != FxSuccess )
	{
		cout << "Streaming failed..." << endl;
		return;
	}

	cout << "Setting open control..." << endl;

	fxSetGains(devId, 100, 30, 0, 0, 0);
	const int numSteps	 = 100;
	int maxVoltage   = 3000;
	int numTimes	 = 2;
	int mV		   = 0;
	ActPackState readData;
	for( int time = 0; time < numTimes; ++time)
	{
		for(int i= 0; i < numSteps; ++i)
		{
			this_thread::sleep_for(100ms);
			mV = maxVoltage * (i*1.0 / numSteps);
			fxSendMotorCommand(devId, FxVoltage, mV);
			clearScreen();
			cout << "Ramping up open controller..." << endl;
				

			if (fxReadDevice(devId, &readData) == FxSuccess)
			{
				// Display State is defined in read_all_example.h
				displayState(readData);
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
			fxSendMotorCommand(devId, FxVoltage, mV);
			clearScreen();
			cout << "Ramping down open controller..." << endl;
			if (fxReadDevice(devId, &readData) == FxSuccess)
			{

				displayState(readData);
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

