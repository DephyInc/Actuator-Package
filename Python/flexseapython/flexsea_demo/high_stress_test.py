"""Perform High Stress Test"""

import os
import sys
from time import sleep, time
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from flexseapython.fxUtil import *
# Next two lines are used to plot in a browser:
import matplotlib
matplotlib.use('WebAgg')

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(pardir)
sys.path.append(pardir)

# Global arrays updated concurrently with every new timestamp
times = []
currentRequests = []
currentMeasurements0 = []  # For devId0
currentMeasurements1 = []  # For devId1
positionRequests = []
positionMeasurements0 = []  # For devId0
positionMeasurements1 = []  # For devId1
readDeviceTimes = []        # Timing data for fxReadDevice()
sendMotorTimes = []         # Timing data for fxSendMotorCommand
setGainsTimes = []          # Timing data for fxSetGains()

# Plotting:
cycleStopTimes = []         # Use to draw a line at end of every period
data0 = 0                   # Contains state of ActPack0
data1 = 0                   # Contains state of ActPack1


def fxHighStressTest(port0, baudRate, port1="", commandFreq=1000,
                     positionAmplitude=10000, currentAmplitude=2500,
                     positionFreq=1, currentFreq=5, currentAsymmetricG=1.25,
                     numberOfLoops=1):
    """
    portX               port with outgoing serial connection to ActPack
    baudRate            baud rate of outgoing serial connection to ActPack
    commandFreq         Desired frequency of issuing commands to controller,
                        actual command frequency will be slower due to OS
                        overhead.
    positionAmplitude   amplitude (in ticks), position controller
    currentAmplitude    amplitude (in mA), current controller
    positionFreq        frequency (Hz) of the sine wave, position controller
    currentFreq         frequency (Hz) of the sine wave, current controller
    currentAsymmetricG  we use more current on the "way back" to come back
                        closer to the staring point. Positive numbers only,
                        1-3 range.
    numberOfLoops       Number of times to send desired signal to controller
    """

    global times            # Elapsed time since strart of run
    global currentRequests
    global positionRequests
    global readDeviceTimes  # Timing data for fxReadDevice()
    global sendMotorTimes  # Timing data for fxSendMotorCommand
    global setGainsTimes  # Timing data for fxSetGains()
    global cycleStopTimes
    global data0            # Contains state of ActPack0
    global data1            # Contains state of ActPack1

    devices = list()

    devices.append({'port': port0})
    if port1:
        devices.append({'port': port1})

    print("Running high stress test with {} device".format(len(devices)) +
          "s" if len(devices) > 1 else "")

    # Debug & Data Logging
    debug_logging_level = 6     # 6 is least verbose, 0 is most verbose
    data_log = False        # Data log logs device data

    delay_time = float(1/(float(commandFreq)))
    print('Delay time: ', delay_time)

    # Open the device and start streaming
    for dev in devices:
        print('Port: ', dev['port'])
        print('BaudRate: ', baudRate)
        print('Logging Level: ', debug_logging_level)
        dev['id'] = fxOpen(dev['port'], baudRate, debug_logging_level)
        fxStartStreaming(dev['id'], commandFreq, data_log)
        print('Connected to device with Id: ', dev['id'])

    # Get initial position:
    print('Reading initial position...')

    # Wait for device to consume the startStreaming command and start streaming
    sleep(0.1)

    # Get initial position
    for dev in devices:
        dev['data'] = fxReadDevice(dev['id'])
        dev['initial_pos'] = dev['data'].mot_ang  # Used to offset readings
        print("Initial Position: ", dev['initial_pos'])

    # Generate control profiles
    print('Generating 3x Command tables...')
    position_samples = sinGenerator(
        positionAmplitude, positionFreq, commandFreq)
    current_samples = sinGenerator(currentAmplitude, currentFreq, commandFreq)
    current_samples_line = lineGenerator(0, 0.15, commandFreq)

    # Initialize lists

    t0 = time()  # Record start time of experiment
    i = 0
    try:
        for rep in range(0, numberOfLoops):
            printLoopCountAndTime(rep, numberOfLoops, time() - t0)

            # Step 0: set position controller
            # -------------------------------
            print("Step 0: set position controller")

            sleep(delay_time)  # Important in loop 2+
            cmds = list()
            for dev in devices:
                if rep:  # Second or later iterations in loop
                    initial_cmd = {{'cur': 0, 'pos': dev['data'].mot_ang}}
                else:
                    initial_cmd = {{'cur': 0, 'pos': dev['initial_pos']}}
                cmds.append(initial_cmd)

            sendAndTimeCmds(t0, devices, cmds, motor_cmd=FxPosition,
                            pos_req=0, set_gains=True)

            # Step 1: go to initial position
            # -------------------------------
            cmds = list()
            if rep:  # Second or later iterations in loop
                print("Step 1: go to initial position")
                lin_samples = linearInterp(data0.mot_ang-initialPos0, 0, 100)

                for sample in lin_samples:
                    for dev in devices:
                        cmd = {{'cur': 0, 'pos': dev['data'].mot_ang}}
                        cmds.append(cmd)

                    sendAndTimeCmds(t0, devices, cmds, motor_cmd=FxPosition,
                                    pos_req=0, set_gains=True)
                    sleep(delay_time)
                    sendAndTimeCmds(t0, devId0, devId1, second_device, initialPos0, initialPos1,
                                    current0=0, current1=0, motor_cmd=FxPosition,
                                    position0=sample + initialPos0, position1=sample + initialPos1,
                                    pos_req=sample, set_gains=False)

                    i = i + 1
            else:
                # First time in loop
                print("Step 1: skipped, first round")

            # Step 2: position sine wave
            # --------------------------
            print("Step 2: track position sine wave")

            for sample in position_samples:

                sleep(delay_time)
                sendAndTimeCmds(t0, devId0, devId1, second_device, initialPos0, initialPos1,
                                current0=0, current1=0, motor_cmd=FxPosition,
                                position0=sample + initialPos0, position1=sample + initialPos1,
                                pos_req=0, set_gains=False)
                i = i + 1

            # Step 3: set current controller
            # -------------------------------
            print("Step 3: set current controller")
            # setCurrentCtrl(   devId0, devId1, second_device, 0, 0)
            sendAndTimeCmds(t0, devId0, devId1, second_device, initialPos0, initialPos1,
                            current0=0, current1=0, motor_cmd=FxCurrent,
                            position0=initialPos0, position1=initialPos1,
                            pos_req=0, set_gains=True)

            # Step 4: current setpoint
            # --------------------------
            print("Step 4: track current sine wave")
            for sample in current_samples:

                sleep(delay_time)
                # We use more current on the "way back" to come back closer to
                # the staring point
                if(sample <= 0):  # No change
                    compensatedSample = sample
                else:  # Apply gain
                    compensatedSample = np.int64(currentAsymmetricG * sample)

                sendAndTimeCmds(t0, devId0, devId1, second_device, initialPos0, initialPos1,
                                current0=compensatedSample, current1=compensatedSample, motor_cmd=FxCurrent,
                                position0=initialPos0, position1=initialPos1,
                                pos_req=0, set_gains=False)
                i = i + 1

            # Step 5: short pause at 0 current to allow a slow-down
            # -----------------------------------------------------
            print("Step 5: motor slow-down, zero current")

            for sample in current_samples_line:

                sleep(delay_time)
                sendAndTimeCmds(t0, devId0, devId1, second_device, initialPos0, initialPos1,
                                current0=sample, current1=sample, motor_cmd=FxCurrent,
                                position0=initialPos0, position1=initialPos1,
                                pos_req=0, set_gains=False)

                i = i + 1

            # We'll draw a line at the end of every period
            cycleStopTimes.append(time() - t0)
            elapsed_time = time() - t0

    except KeyboardInterrupt:
        print('Keypress detected. Exiting gracefully...')

    # Disable the controller, send 0 PWM
    fxSendMotorCommand(devId0, FxVoltage, 0)
    fxSendMotorCommand(devId1, FxVoltage, 0)
    sleep(0.1)

    ######## Stats: #########
    print("")
    print("Final Stats:")
    print("------------")
    actual_period = cycleStopTimes[0]
    command_frequency = i / elapsed_time
    print("Number of commands sent:" + str(i))
    print("Total time (s):" + str(elapsed_time))
    print("Requested command frequency:"+"{:.2f}".format(commandFreq))
    print("Actual command frequency (Hz):"+"{:.2f}".format(command_frequency))
    print("")
    print('current_samples_line:', len(current_samples_line))
    print('size(times):', len(times))
    print('size(currentRequests):', len(currentRequests))
    print('size(currentMeasurements0):',    len(currentMeasurements0))
    print('size(setGainsTimes):',       len(setGainsTimes))
    print('')

    ######## Summary stats about individual arrays: #########
    # print('\n\ntimes: ',          stats.describe(times))
    # print('\n\ncurrentRequests: ',        stats.describe(currentRequests))
    # print('\n\ncurrentMeasurements0: ',   stats.describe(currentMeasurements0))
    # print('\n\ncurrentMeasurements1: ',   stats.describe(currentMeasurements1))
    # print('\n\npositionRequests: ',       stats.describe(positionRequests))
    # print('\n\npositionMeasurements0: ',  stats.describe(positionMeasurements0))
    # print('\n\npositionMeasurements1: ',  stats.describe(positionMeasurements1))
    # print('\n\nreadDeviceTimes: ',        stats.describe(readDeviceTimes))
    # print('\n\nsendMotorTimes: ',     stats.describe(sendMotorTimes))
    # print('\n\nseetGainsTimes: ',     stats.describe(setGainsTimes))

    ######## End of Main Code #########

    ######## Plotting Code, you can edit this ##################

    # Begin Create unique data filename and save desired and measured values
    # now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    # data_fn = 'log/' + now + '_Current.csv'
    # print('Do create Current  data file ['+ data_fn + ']')
    # NON-PYTHONIC, but efficient write to file:
    # with open(data_fn, 'w') as df:
    #   for i in range(len(currentRequests)):
    #       df.write(str(times[i]) + ',' + str(currentRequests[i]) + ','
    #           + str(currentMeasurements0[i]) + '\n')

    # data_fn = 'log/' + now + '_Position.csv'
    # print('Do create Position data file ['+ data_fn + ']')
    # with open(data_fn, 'w') as df:
    #   for i in range(len(positionRequests)):
    #       df.write(str(times[i]) + ',' + str(positionRequests[i]) + ','
    #           + str(positionMeasurements0[i]) + '\n')
    # End Create unique data filename and save desired and measured values

    # Current Plot:
    print('Preparing plot 1')
    plt.figure(1)
    title = "Motor Current"
    plt.plot(times, currentRequests, color='b', label='desired current')
    plt.plot(times, currentMeasurements0, color='r', label='measured current')
    plt.xlabel("Time (s)")
    plt.ylabel("Motor current (mA)")
    plt.title(title)
    plt.legend(loc='upper right')

    # Draw a vertical line at the end of each cycle
    for endpoints in cycleStopTimes:
        plt.axvline(x=endpoints)

    # Position Plot:
    print('Preparing plot 2')
    plt.figure(2)
    title = "Motor Position"
    plt.plot(times, positionRequests, color='b', label='desired position')
    plt.plot(times, positionMeasurements0,
             color='r', label='measured position')
    plt.xlabel("Time (s)")
    plt.ylabel("Encoder position")
    plt.title(title)
    plt.legend(loc='upper right')

    print('Showing plot')
    plt.show()
    sleep(0.1)

    print('End of script, fxCloseAll()')
    fxCloseAll()

# Send FlexSEA commands and record their execution time.
def sendAndTimeCmds(t0, devId0, devId1, device2: bool, initialPos0, initialPos1,
		current0, current1, motorCmd, position0, position1, posReq, setGains: bool):
	"""
	t0: Timestamp for start of run. (Current time-t0) = Elapsed time
	initialPos0, initialPos1: Initial encoder angles for devId0, devId1. Used to provide offsets
		to encoder angle readings.
	current0, current1: Desired currents for devId0 and devId1
	position0, position1: Desired positions for devId0 and devId1
	motorCmd: An enum defined in flexseapython.py. Allowed values:
		FxPosition, FxVoltage, FxCurrent, FxImpedance
	"""
	global times					# Elapsed time from start of run
	global currentRequests
	global currentMeasurements0		# For devId0
	global currentMeasurements1		# For devId1
	global positionRequests
	global positionMeasurements0	# For devId0
	global positionMeasurements1	# For devId1
	global readDeviceTimes			# Timing data for fxReadDevice()
	global sendMotorTimes			# Timing data for fxSendMotorCommand
	global setGainsTimes			# Timing data for fxSetGains()
	global data0					# Contains state of ActPack0
	global data1 					# Contains state of ActPack1

	tstart = time()
	data0 = fxReadDevice(devId0)	# Get ActPackState
	readDeviceTimes.append(time() - tstart)
	if(device2):
		data1 = fxReadDevice(devId1)

	if setGains:
		tstart = time()
		for i in range(2):
			fxSetGains(devId0, 300, 50, 0, 0, 0)
		setGainsTimes.append(time() - tstart)
		if(device2):
			fxSetGains(devId1, 300, 50, 0, 0, 0)
	else:
		setGainsTimes.append(0)

	if motorCmd == FxCurrent:	# Set device(s) for current control
		tstart = time()
		fxSendMotorCommand(devId0, FxCurrent, current0)
		sendMotorTimes.append(time() - tstart)
		if(device2):
			fxSendMotorCommand(devId1, FxCurrent, current1)
			positionMeasurements1.append(data1.mot_ang)
		positionMeasurements0.append(data0.mot_ang)

	elif motorCmd == FxPosition:	# Set device(s) for position control
		tstart = time()
		fxSendMotorCommand(devId0, FxPosition, position0)
		sendMotorTimes.append(time() - tstart)
		if(device2):
			fxSendMotorCommand(devId1, FxPosition, position1)
			positionMeasurements1.append(data1.mot_ang)
		positionMeasurements0.append(data0.mot_ang)

	else:	# Defensive code.  It should not execute!
		assert 0, 'Unexpected motor command in record_timing()'

	currentRequests.append(current0)
	currentMeasurements0.append(data0.mot_cur)
	if(device2):
		currentMeasurements1.append(data1.mot_cur)
	positionRequests.append(position0)
	times.append(time() - t0)

if __name__ == '__main__':
    baudRate = sys.argv[1]
    ports = sys.argv[2:3]
    try:
        fxHighStressTest(ports, baudRate)
    except Exception as err:
        print("broke: {}".format(err))
