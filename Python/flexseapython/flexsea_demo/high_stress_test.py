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

# Globals updated with every timestamp for plotting
TIMESTAMPS = list()  # Elapsed times since strart of run
CYCLE_STOP_TIMES = list()  # Timestamps for each loop end


def fxHighStressTest(port0, baudRate, port1='', commandFreq=1000,
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

    global TIMESTAMPS            # Elapsed times since strart of run
    global CYCLE_STOP_TIMES      # Timestamps for each loop end

    devices = list()
    devices.append({'port': port0})
    if port1:
        devices.append({'port': port1})

    print('Running high stress test with {} device'.format(len(devices)) +
          's' if len(devices) > 1 else '')

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
        print('Initial Position: {}'.format(dev['initial_pos']))

    # Generate control profiles
    print('Generating three Command tables...')
    position_samples = sinGenerator(
        positionAmplitude, positionFreq, commandFreq)
    current_samples = sinGenerator(currentAmplitude, currentFreq, commandFreq)
    current_samples_line = lineGenerator(0, 0.15, commandFreq)

    # Initialize lists

    start_time = time()  # Record start time of experiment
    cmd_count = 0
    try:
        for rep in range(0, numberOfLoops):
            printLoopCountAndTime(rep, numberOfLoops, time() - start_time)

            # Step 0: set position controller
            # -------------------------------
            print('Step 0: set position controller')

            sleep(delay_time)  # Important in loop 2+
            cmds = list()
            for dev in devices:
                if rep:  # Second or later iterations in loop
                    initial_cmd = {'cur': 0, 'pos': dev['data'].mot_ang}
                else:
                    initial_cmd = {'cur': 0, 'pos': dev['initial_pos']}
                cmds.append(initial_cmd)

            send_and_time_cmds(start_time, devices, cmds, FxPosition, True)

            # Step 1: go to initial position
            # -------------------------------
            if rep:  # Second or later iterations in loop
                print('Step 1: go to initial position')
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
                        send_and_time_cmds(start_time, devices,
                                           cmds, FxPosition, False)
                        cmd_count += 1
            else:
                # First time in loop
                print('Step 1: skipped, first round')

            # Step 2: position sine wave
            # --------------------------
            print('Step 2: track position sine wave')

            for sample in position_samples:
                cmds = [{'cur': 0, 'pos': sample + dev['initial_pos']}
                        for dev in devices]
                sleep(delay_time)
                send_and_time_cmds(start_time, devices,
                                   cmds, FxPosition, False)
                cmd_count += 1

            # Step 3: set current controller
            # -------------------------------
            print('Step 3: set current controller')
            cmds = [{'cur': 0, 'pos': 0} for dev in devices]
            send_and_time_cmds(start_time, devices, cmds, FxCurrent, True)

            # Step 4: current setpoint
            # --------------------------
            print('Step 4: track current sine wave')
            for sample in current_samples:
                sleep(delay_time)
                # We use more current on the "way back" to come back closer to
                # the staring point
                if sample > 0:  # Apply gain
                    sample = np.int64(currentAsymmetricG * sample)
                cmds = [{'cur': sample, 'pos': dev['initial_pos']}
                        for dev in devices]

                sleep(delay_time)
                send_and_time_cmds(start_time, devices, cmds, FxCurrent, False)
                cmd_count += 1

            # Step 5: short pause at 0 current to allow a slow-down
            # -----------------------------------------------------
            print('Step 5: motor slow-down, zero current')

            for sample in current_samples_line:
                cmds = [{'cur': sample, 'pos': dev['initial_pos']}
                        for dev in devices]
                sleep(delay_time)
                send_and_time_cmds(start_time, devices, cmds, FxCurrent, False)
                cmd_count += 1

            # Draw a line at the end of every loop
            CYCLE_STOP_TIMES.append(time() - start_time)

    except KeyboardInterrupt:
        print('Keypress detected. Exiting gracefully...')

    elapsed_time = time() - start_time

    # Disable the controller, send 0 PWM
    for dev in devices:
        fxSendMotorCommand(dev['id'], FxVoltage, 0)
    sleep(0.1)

    ######## Stats: #########
    print('')
    print('Final Stats:')
    print('------------')
    print('Number of commands sent: {}'.format(cmd_count))
    print('Total time (s): {}'.format(elapsed_time))
    print('Requested command frequency: {:.2f}'.format(commandFreq))
    assert (elapsed_time != 0), 'Elapsed time is 0.'
    print('Actual command frequency (Hz): {:.2f}'.format(
        cmd_count / elapsed_time))
    print('')
    print('current_samples_line: {}'.format(len(current_samples_line)))
    print('size(TIMESTAMPS): {}'.format(len(TIMESTAMPS)))
    print('size(currentRequests): {}'.format(len(devices[0]['curr_requests'])))
    print('size(currentMeasurements0): {}'.format(
        len(devices[0]['curr_measurements'])))
    print('size(SET_GAINS_TIMES): {}'.format(len(devices[0]['gains_times'])))
    print('')

    plot_data(devices)


def plot_data(devices):
    """
    Plots received data
    devices:  Dictionarty containing iinfor foir ach connected device.
    """
    global TIMESTAMPS            # Elapsed times since strart of run
    global CYCLE_STOP_TIMES      # Timestamps for each loop end

    figure_ind = 0
    for dev in devices:
        # Current Plot:
        figure_ind += 1
        print('Preparing plot {}'.format(figure_ind))
        plt.figure(figure_ind)
        title = 'Motor Current ({})'.format(dev['id'])
        plt.plot(TIMESTAMPS, dev['curr_requests'],
                 color='b', label='desired current')
        plt.plot(TIMESTAMPS, dev['curr_measurements'],
                 color='r', label='measured current')
        plt.xlabel('Time (s)')
        plt.ylabel('Motor current (mA)')
        plt.title(title)
        plt.legend(loc='upper right')

        # Draw a vertical line at the end of each loop
        for endpoints in CYCLE_STOP_TIMES:
            plt.axvline(x=endpoints, color='grey', linestyle='--')

        # Position Plot:
        figure_ind += 1
        print('Preparing plot {}'.format(figure_ind))
        plt.figure(figure_ind)
        title = 'Motor Position ({})'.format(dev['id'])
        plt.plot(TIMESTAMPS, dev['pos_requests'],
                 color='b', label='desired position')
        plt.plot(TIMESTAMPS, dev['pos_measurements'],
                 color='r', label='measured position')
        plt.xlabel('Time (s)')
        plt.ylabel('Encoder position')
        plt.title(title)
        plt.legend(loc='upper right')

        # Draw a vertical line at the end of each loop
        for endpoints in CYCLE_STOP_TIMES:
            plt.axvline(x=endpoints, color='grey', linestyle='--')

    print('Showing plots')
    plt.show()
    sleep(0.1)

    printPlotExit()
    fxCloseAll()
    print('Communication closed')


def send_and_time_cmds(start_time, devices, cmds, motor_cmd, set_gains: bool):
    """
    Send FlexSEA commands and record their execution time.
    start_time: Timestamp for start of run. (Current time-start_time) = Elapsed time
    devices:    Dictionary containing info on all connected devices
    cmds:       Dictionary containing position and current commands e.g. {pos: 0, curr: 0}
    motor_cmd:  An enum defined in flexseapython.py. Allowed values: FxPosition,, FxCurrent
    """
    global TIMESTAMPS  # Elapsed times from start of run

    assert (motor_cmd in [FxPosition, FxCurrent]
            ), 'Unexpected motor command, only FxPosition, FxCurrent allowed'

    for dev, cmd in zip(devices, cmds):
        tstart = time()
        dev['data'] = fxReadDevice(dev['id'])  # Get ActPackState
        dev['read_times'].append(time() - tstart)

        if set_gains:
            tstart = time()
            fxSetGains(dev['id'], 300, 50, 0, 0, 0)
            dev['gains_times'].append(time() - tstart)
        else:
            dev['gains_times'].append(0)

        # Select command value
        cmd_val = cmd['cur'] if motor_cmd == FxCurrent else cmd['pos']
        # Command motor
        tstart = time()
        fxSendMotorCommand(dev['id'], motor_cmd, cmd_val)
        dev['motor_times'].append(time() - tstart)
        dev['pos_measurements'].append(dev['data'].mot_ang)

        dev['curr_requests'].append(cmd['cur'])
        dev['curr_measurements'].append(dev['data'].mot_cur)

        dev['pos_requests'].append(cmd['pos'])

    TIMESTAMPS.append(time() - start_time)


if __name__ == '__main__':
    baud_rate = sys.argv[1]
    ports = sys.argv[2:3]
    try:
        fxHighStressTest(ports, baud_rate)
    except Exception as err:
        print('broke: {}'.format(err))
