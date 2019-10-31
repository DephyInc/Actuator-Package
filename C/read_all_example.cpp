#include "read_all_example.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "Exo.h"
#include "device_wrapper.h"

using namespace std;
using namespace std::literals::chrono_literals;

void displayState(struct ExoState& state)
{
	cout << endl << "imu: " << state._manage._imu._accelx << ", " << state._manage._imu._accely << \
		", " << state._manage._imu._accelz << endl;
	cout << "motor: " << state._execute._motor_data._motor_angle << " angle, " << \
		state._execute._motor_data._motor_voltage << " mV" << endl;
	cout <<"battery: " << state._regulate._battery._battery_voltage << " mV, " << \
		state._regulate._battery._battery_current << " mA, " << \
		state._regulate._battery._battery_temperature << " C" << endl << endl; 
}

void runReadAll(int devId, bool *shouldQuit)
{
    cout << "\n Running the READ-ALL Demo\n" << endl;
    //
    // Start streaming the data
    //
    if(fxStartStreaming(devId, true) != FxSuccess )
    {
        cout << "Streaming failed ..." << endl;
        return;
    }

    //
    // Read and display the data
    //
    ExoState exoState;
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
