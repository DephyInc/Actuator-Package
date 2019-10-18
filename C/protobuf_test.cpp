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

void display_state(struct ExoState& state)
{
	cout << endl << "imu: " << state._manage._imu._accelx << ", " << state._manage._imu._accely << \
		", " << state._manage._imu._accelz << endl;
	cout << "motor: " << state._execute._motor_data._motor_angle << " angle, " << \
		state._execute._motor_data._motor_voltage << " mV" << endl;
	cout <<"battery: " << state._regulate._battery._battery_voltage << " mV, " << \
		state._regulate._battery._battery_current << " mA, " << \
		state._regulate._battery._battery_temperature << " C" << endl;
	cout << "genVar: " << state._genvars._gv0 << ", " << state._genvars._gv1 << endl;
	cout << "ankle angle: " << state._manage._ankle_angle << endl << endl;
}

void cleanup(void)
{
	// Turn off controller and stop streaming
	exo_device->setMotorGains(0, 0, 0);
	exo_device->stopStreaming();
}

// Try out the open controller
void test_open_commands(void)
{
	// State stores the device's sensor and motor data and can be passed into the read method 
	ExoState state;

	// Enable auto streaming to have exo automatically send data
	bool shouldLog = true;
	exo_device->startStreaming(shouldLog);

	const int numSteps = 100;
	int maxVoltage = 3000;
	int iterations = 2;
	int mV = 0;

	for( int time = 0; time < iterations; ++time)
	{
		for(int i= 0; i < numSteps; ++i)
		{
			// Determine the voltage to set the motor to
			mV = maxVoltage * (i*1.0 / numSteps);
			// Queue up a command using protocol buffers
			exo_device->sendMotorCommand(ControllerType::EOpen, mV);
			// Read the latest state of the device
			exo_device->read(state);
			// Print out the motor and sensor data
			display_state(state);
			this_thread::sleep_for(100ms);
			if(shouldQuit)
			{
				cout << "Ending position test early" << endl;
				return;
			}
		}
		// Wait 1 second
		this_thread::sleep_for(1s);
		// And reverse direction
		for( int j = 0; j < numSteps; ++j)
		{
			mV = maxVoltage * ((numSteps - j)*1.0 / numSteps);
			// Queue up a command using protocol buffers
			exo_device->sendMotorCommand(ControllerType::EOpen, mV);
			// Read the latest state of the device
			exo_device->read(state);
			// Print out the motor and sensor data
			display_state(state);
			this_thread::sleep_for(100ms);
			if(shouldQuit)
			{
				cout << "Ending position test early" << endl;
				return;
			}
		}
	}
	cleanup();
}


// Sending a large number of position commands
void test_position_commands(void)
{
	int32_t start_position;
	int32_t position, i;

	// State stores the device's sensor and motor data and can be passed into the read method 
	ExoState state;

	// Enable auto streaming to have exo automatically send data
	bool shouldLog = true;
	exo_device->startStreaming(shouldLog);
	// Set the gains for the position controller
	exo_device->setMotorGains(100, 3, 0);
	// Get the initial state of the exo
	if(exo_device->read(state))
	{
		start_position = state._execute._motor_data._motor_angle;
		cout << "Our starting position will be " << start_position << endl;
	}
	else
	{
		cout << "Unable to read from the device so we are exiting now" << endl;
		// We were unable to read from the device so let's clean up and quit
		cleanup();
		shouldQuit = true;
	}

	while(!shouldQuit)
	{
		for(position = start_position; position <= start_position + 50000; position += 100)
		{
			// Queue up a command using protocol buffers
			exo_device->sendMotorCommand(ControllerType::EPosition, position);
			// Read the latest state of the device
			exo_device->read(state);
			// Print out the motor and sensor data
			display_state(state);
			this_thread::sleep_for(10ms);
			if(shouldQuit)
			{
				cout << "Ending position test early" << endl;
				return;
			}
		}
		for(position = start_position + 50000; position >= start_position; position -= 100)
		{
			// Queue up a command using protocol buffers
			exo_device->sendMotorCommand(ControllerType::EPosition, position);
			// Read the latest state of the device
			exo_device->read(state);
			// Print out the motor and sensor data
			display_state(state);
			this_thread::sleep_for(10ms);
			if(shouldQuit)
			{
				cout << "Ending position test early" << endl;
				return;
			}
		}
	}
	cleanup();
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

	while(!shouldQuit)
	{
		//test_open_commands();
		test_position_commands();
	}
	

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
