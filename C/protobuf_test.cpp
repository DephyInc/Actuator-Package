#include <iostream>

#include <csignal>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <chrono>
#include <thread>
#include <fstream>

#ifdef _WIN32
	#include "windows.h"
#endif

#include "device.h"
#include "serial.h"

using namespace std;
using namespace std::literals::chrono_literals;

// Read the com port out of com.txt
void getUserPort(const string filename, string *ports, int *baudRate);

// File to look for the com port names in
string configFile = "../com.txt";
// This flag gets set when ctrl+c is pressed
bool shouldQuit = false;

// This object is used for connecting, sending, and receiving data from a device
Device* exo_device;

// This callback is just to quit the program if someone presses ctrl+c
void sigint_handler(int s)
{
	(void)s;
	cout << "Caught CTRL-C, exiting...\n";
	shouldQuit = true;
}

// Sending a large number of position commands
void test_position_commands(void)
{
	int32_t STARTING_POSITION = 0;
	int32_t ENDING_POSITION = 10000;
	int32_t ITERATIONS = 1;

	int32_t position, i;

	// Enable auto streaming to have exo automatically send data
	exo_device->startStreaming();
	while(!shouldQuit)
	{
		for(position = STARTING_POSITION; position <= ENDING_POSITION; position += 1000)
		{
			// Queue up a command using protocol buffers
			exo_device->sendMotorCommand(ControllerType::EPosition, position);
			exo_device->read();
			this_thread::sleep_for(10ms);
			if(shouldQuit)
			{
				cout << "Ending position test early" << endl;
				return;
			}
		}
		for(position = ENDING_POSITION; position >= STARTING_POSITION; position -= 1000)
		{
			// Queue up a command using protocol buffers
			exo_device->sendMotorCommand(ControllerType::EPosition, position);
			exo_device->read();
			this_thread::sleep_for(10ms);
			if(shouldQuit)
			{
				cout << "Ending position test early" << endl;
				return;
			}
		}
	}
}

int main()
{
	//
	// Capture the CTRL-C signal
	//
	std::signal(SIGINT, sigint_handler);

	cout << "Protocol buffer test script" << endl;

	unsigned idx = 0;
	string portName[2];
	int baudRate;
	//
	// Read the COM ports from COM.TXT
	//
	getUserPort(configFile, portName, &baudRate);

	cout << "Connecting to port: " << portName[0] << endl;

	//
	// Construct the device
	//
	try 
	{
		exo_device = new Device(portName[idx], baudRate, 200, 0);
	}
	catch (const std::exception& e)
	{
		cout << "Exception: " << e.what() << endl;
		exit(0);
	}	
	catch (...)
	{
		cout << "Unexpected error occured" << endl;
		exit(0);
	}

	cout << "Successful connection to " << portName[idx] << endl;

	bool doLog = true;
	exo_device->startStreaming(doLog);

	while(!shouldQuit)
	{
		test_position_commands();
	}
	
	exo_device->stopStreaming();

	cout << "Quitting application, closing serial port now" << endl;


	return 0;
}

void getUserPort(const string filename, string *ports, int *baudRate)
{
	cout << "Opening file: " << filename << endl;
	ifstream cfgFile( filename );

	if( ! cfgFile)
	{
		cout << endl << "No com.txt found..." << endl;
		cout << "Please copy com_template.txt to a file named com.txt" << endl;
		cout << "Be sure to use the same format of baud rate on the first line," \
			" and com ports on preceding lines" << endl;
		exit(1);
	}

	string line;
	getline(cfgFile, line);
	*baudRate = std::stoi(line);

	std::cout << "using baud rate: " << *baudRate << std::endl;

	int i = 0;
	while( ! cfgFile.eof() )
	{
		getline(cfgFile, line);
		if(! line.empty())
		{
			ports[i] = line;
			cout << "read Com port " << line << " (" << ports[i] << ")" << endl;
		}
	}
}
