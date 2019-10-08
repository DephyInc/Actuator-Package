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

using namespace std;
using namespace std::literals::chrono_literals;

void printMenu();
char userSelection(void);
void getUserPort(const string filename, string *ports, int *baudRate);

int		activeDemo = 0;
string	configFile = "com.txt";
bool	shouldQuit = false;

void my_handler(int s)
{
	(void)s;
	cout << "Caught CTRL-C, exiting...\n";
	shouldQuit = true;
}

int main()
{
	//
	// Capture the CTRL-C signal
	//
	std::signal(SIGINT, my_handler);

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
	// Open the port
	//
	// fxOpen((char *)portName[idx].c_str(), idx, baudRate);
	this_thread::sleep_for(200ms);

	cout << "Waiting for port: " << portName[idx] << endl;

	//
	// Wait for the port to open
	//
	unsigned waited  = 0;
	bool waiting = true;
	while (waiting )
	{
		if(waited >= 5)
		{
			cout << "device didn't open in time "<< idx << endl;
			break;
		}
		sleep( 1 );
		waited  = waited + 1;
		waiting = true;

		// if( fxIsOpen(idx))
		// {
		// 	waiting = false;
		// }
	}
	if(waiting)
	{
		cout << "Couldn't connect " << endl;
		exit(0);
	}

	while(!shouldQuit)
	{
		printf("alive\r\n");
		this_thread::sleep_for(1s);
	}

	// //
	// // Close all of the FlexSEA devices
	// //
	// cout << "closing ports" << endl;
	// for(uint8_t i = 0; i < devicesOpened; ++i)
	// {
	// 	fxClose( i );
	// }

	// //
	// // Cleanup and shutdown the FlexSEA environment
	// //
	// cout << "Turning device control off..." << endl;
	// fxCleanup();


	// // wait to make sure the command goes through before we quit
	// this_thread::sleep_for(100ms);

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
