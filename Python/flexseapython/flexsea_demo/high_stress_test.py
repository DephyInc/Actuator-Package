"""Perform High Stress Test"""

import os
import sys
from time import sleep, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from flexseapython.fxUtil import *

# Plot in a browser:
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
    print('Generating three Command tables...')
    position_samples = sinGenerator(
        positionAmplitude, positionFreq, commandFreq)
    current_samples = sinGenerator(currentAmplitude, currentFreq, commandFreq)
    current_samples_line = lineGenerator(0, 0.15, commandFreq)

    # Initialize lists

    t0 = time()  # Record start time of experiment
    cmd_count = 0
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
                    initial_cmd = {'cur': 0, 'pos': dev['data'].mot_ang}
                else:
                    initial_cmd = {'cur': 0, 'pos': dev['initial_pos']}
                cmds.append(initial_cmd)

            sendAndTimeCmds(t0, devices, cmds, FxPosition, True)

            # Step 1: go to initial position
            # -------------------------------
            if rep:  # Second or later iterations in loop
                print("Step 1: go to initial position")
                # Create interpolation angles for each device
                lin_samples = list()
                for dev in devices:
                    lin_samples.append(linearInterp(
                        dev['data'].mot_ang - dev['initial_pos'], 0, 100))

                for samples in lin_samples:
                    for sample in samples:
                        cmds = [{'cur': 0, 'pos': sample + dev['initial_pos']}
                                for dev in devices]
                        sleep(delay_time)
                        sendAndTimeCmds(t0, devices, cmds, FxPosition, False)
                        cmd_count += 1
            else:
                # First time in loop
                print("Step 1: skipped, first round")

            # Step 2: position sine wave
            # --------------------------
            print("Step 2: track position sine wave")

            for sample in position_samples:
                cmds = [{'cur': 0, 'pos': sample + dev['initial_pos']}
                        for dev in devices]
                sleep(delay_time)
                sendAndTimeCmds(t0, devices, cmds, FxPosition, False)
                cmd_count += 1

            # Step 3: set current controller
            # -------------------------------
            print("Step 3: set current controller")
            cmds = [{'cur': 0, 'pos': 0} for dev in devices]
            sendAndTimeCmds(t0, devices, cmds, FxCurrent, True)

            # Step 4: current setpoint
            # --------------------------
            print("Step 4: track current sine wave")
            for sample in current_samples:
                sleep(delay_time)
                # We use more current on the "way back" to come back closer to
                # the staring point
                if sample > 0:  # Apply gain
                    sample = np.int64(currentAsymmetricG * sample)
                cmds = [{'cur': sample, 'pos': dev['initial_pos']}
                        for dev in devices]

                sleep(delay_time)
                sendAndTimeCmds(t0, devices, cmds, FxCurrent, False)
                cmd_count += 1

            # Step 5: short pause at 0 current to allow a slow-down
            # -----------------------------------------------------
            print("Step 5: motor slow-down, zero current")

            for sample in current_samples_line:
                cmds = [{'cur': sample, 'pos': dev['initial_pos']}
                        for dev in devices]
                sleep(delay_time)
                sendAndTimeCmds(t0, devices, cmds, FxCurrent, False)
                cmd_count += 1

            # Draw a line at the end of every loop
            cycleStopTimes.append(time() - t0)

    except KeyboardInterrupt:
        print('Keypress detected. Exiting gracefully...')

    elapsed_time = time() - t0

    # Disable the controller, send 0 PWM
    for dev in devices:
        fxSendMotorCommand(dev['id'], FxVoltage, 0)
    sleep(0.1)

    ######## Stats: #########
    print("")
    print("Final Stats:")
    print("------------")
    print("Number of commands sent: {}".format(cmd_count))
    print("Total time (s): {}".format(elapsed_time))
    print("Requested command frequency: {:.2f}".format(commandFreq))
    assert (elapsed_time != 0), "Elapsed time is 0."
    print("Actual command frequency (Hz): {:.2f}".format(
        cmd_count / elapsed_time))
    print("")
    print("current_samples_line: {}".format(len(current_samples_line)))
    print("size(times): {}".format(len(times)))
    print("size(currentRequests): {}".format(len(devices[0]['curr_requests'])))
    print("size(currentMeasurements0): {}".format(
        len(devices[0]['curr_measurements'])))
    print("size(setGainsTimes): {}".format(len(setGainsTimes)))
    print("")

    for dev in devices:
        # Current Plot:
        print('Preparing plot 1')
        plt.figure(1)
        title = "Motor Current"
        plt.plot(times, dev['curr_requests'],
                 color='b', label='desired current')
        plt.plot(times, dev['curr_measurements'],
                 color='r', label='measured current')
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
        plt.plot(times, dev['pos_requests'], color='b', label='desired position')
        plt.plot(times, dev['pos_measurements'],
                 color='r', label='measured position')
        plt.xlabel("Time (s)")
        plt.ylabel("Encoder position")
        plt.title(title)
        plt.legend(loc='upper right')

    print('Showing plots')
    plt.show()
    sleep(0.1)

    printPlotExit()
    print('End of script, fxCloseAll()')
    fxCloseAll()

# Send FlexSEA commands and record their execution time.


def sendAndTimeCmds(t0, devices, cmds, motor_cmd, set_gains: bool):
    """
    t0: Timestamp for start of run. (Current time-t0) = Elapsed time
    initialPos0, initialPos1: Initial encoder angles for devId0, devId1. Used to provide offsets
            to encoder angle readings.
    current0, current1: Desired currents for devId0 and devId1
    position0, position1: Desired positions for devId0 and devId1
    motor_cmd: An enum defined in flexseapython.py. Allowed values:
            FxPosition, FxVoltage, FxCurrent, FxImpedance
    """
    global times                    # Elapsed time from start of run
    global currentRequests
    global currentMeasurements0     # For devId0
    global currentMeasurements1     # For devId1
    global positionRequests
    global positionMeasurements0  # For devId0
    global positionMeasurements1  # For devId1
    global readDeviceTimes          # Timing data for fxReadDevice()
    global sendMotorTimes           # Timing data for fxSendMotorCommand
    global setGainsTimes            # Timing data for fxSetGains()
    global data0                    # Contains state of ActPack0
    global data1                    # Contains state of ActPack1

    tstart = time()
    data0 = fxReadDevice(devId0)  # Get ActPackState
    readDeviceTimes.append(time() - tstart)
    if(device2):
        data1 = fxReadDevice(devId1)

    if set_gains:
        tstart = time()
        for i in range(2):
            fxSetGains(devId0, 300, 50, 0, 0, 0)
        setGainsTimes.append(time() - tstart)
        if(device2):
            fxSetGains(devId1, 300, 50, 0, 0, 0)
    else:
        setGainsTimes.append(0)

    if motor_cmd == FxCurrent:  # Set device(s) for current control
        tstart = time()
        fxSendMotorCommand(devId0, FxCurrent, current0)
        sendMotorTimes.append(time() - tstart)
        if(device2):
            fxSendMotorCommand(devId1, FxCurrent, current1)
            positionMeasurements1.append(data1.mot_ang)
        positionMeasurements0.append(data0.mot_ang)

    elif motor_cmd == FxPosition:  # Set device(s) for position control
        tstart = time()
        fxSendMotorCommand(devId0, FxPosition, position0)
        sendMotorTimes.append(time() - tstart)
        if(device2):
            fxSendMotorCommand(devId1, FxPosition, position1)
            positionMeasurements1.append(data1.mot_ang)
        positionMeasurements0.append(data0.mot_ang)

    else:  # Defensive code.  It should not execute!
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
