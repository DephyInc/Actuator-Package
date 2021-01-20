#!/usr/bin/env python3
"""
FlexSEA devices Python demo
"""

import os
import sys
from signal import signal, SIGINT
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea_demo.readonly import fx_read_only

# from flexsea_demo.opencontrol import fxOpenControl
# from flexsea_demo.currentcontrol import fxCurrentControl
# from flexsea_demo.positioncontrol import fxPositionControl
# from flexsea_demo.high_speed_test import fxHighSpeedTest
# from flexsea_demo.high_stress_test import fxHighStressTest
# from flexsea_demo.two_devices_positioncontrol import fxTwoDevicePositionControl
# from flexsea_demo.impedancecontrol import fxImpedanceControl
# from flexsea_demo.two_devices_leaderfollower import fxLeaderFollower
# from flexsea_demo.twopositioncontrol import fxTwoPositionControl

if ((sys.version_info[0] == 3) and (sys.version_info[1] == 8)):
    if fxu.is_win():  # Need for WebAgg server to work in Python 3.8
        print('Detected Python 3.8')
        print('Detected: {}'.format(sys.platform))
        import asyncio

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def sig_handler(*unused):
    """
    Handle program exit via SIGINT
    """
    return sys.exit('\nCTRL-C or SIGINT detected\nExiting ...')


def fx_run_find_poles(port, baud_rate):
    """
    Find motor poles
    """
    fx = flex.FlexSEA()
    dev_id = fx.open(port, baud_rate, 0)
    if fx.find_poles(dev_id) == fxe.FX_INVALID_DEVICE:
        raise ValueError('fxFindPoles: invalid device ID')


# List of available experiments.
# Format is: functionName, text string, min number of devices, max devices
EXPERIMENTS = [
    (fx_read_only, 'Read Only', 1, 1),
    # (fxOpenControl, 'Open Control', 1, 1),
    # (fxCurrentControl, 'Current Control', 1, 1),
    # (fxPositionControl, 'Position Control', 1, 1),
    # (fxImpedanceControl, 'Impedance Control', 1, 1),
    # (fx_run_find_poles, 'Find Poles', 1, 1),
    # (fxTwoPositionControl, 'Two Positions Control', 1, 1),
    # (fxHighSpeedTest, 'High Speed Test', 1, 4),
    # (fxHighStressTest, 'High Stress Test', 1, 2),
    # (fxTwoDevicePositionControl, 'Two Devices Position Control', 2, 2),
    # (fxLeaderFollower, 'Two Devices Leader Follower Control', 2, 2)
]

MAX_EXPERIMENT = len(EXPERIMENTS) - 1
MAX_EXPERIMENT_STR = str(MAX_EXPERIMENT)
IDX_TWO_DEV_POS_CTRL = 9
IDX_LDR_FLWR = 10


def print_experiments():
    """
    Print list of available experiments
    """
    count = 0
    print('>>> Actuator Package Python Demo Scripts <<<')
    for exp in EXPERIMENTS:
        print('[{}] {}'.format(count, exp[1]))
        count += 1


def print_usage(prog_name: str):
    """
    Some error occurred. Print help message and exit.
    """
    # TODO (CA): use argparse for all arguments and usage
    print('\nUsage:\tPython {} [experiment_number (1 - {}) connected_devices (1 - N)]'.format(
        prog_name, len(EXPERIMENTS)))
    print('\t"connected_devices" ONLY required for specific experiments\n' +
          '\tOther experiments use [1] device by default.\n')


def get_exp_ind(argv):
    """
    Obtain experiment number from argument list or by prompting user
    """
    if len(argv) > 1:
        # Get it from the command line argument list
        exp_ind = argv[1]
    else:
        # Or prompt the user for it
        exp_ind = input('Choose experiment number [q to quit]: ')
        if exp_ind.lower() == 'q':
            sys.exit(0)
    # Make sure it's valid and in range:
    if not exp_ind.isdecimal():  # Filter out letters
        sys.exit(
            'Please choose an experiment between [0 - {} ]'.format(
                len(EXPERIMENTS) - 1))
    exp_ind = int(exp_ind)  # Make sure is a int and not a string
    if exp_ind not in range(len(EXPERIMENTS)):
        sys.exit(
            'Please choose an experiment between [0 - {} ]'.format(
                len(EXPERIMENTS) - 1))
    return exp_ind


def get_dev_num(argv, exp_ind):
    """
    Obtain number of devices from argument list or by prompting user
    """
    dev_range = range(EXPERIMENTS[exp_ind][2], EXPERIMENTS[exp_ind][3] + 1)

    # Only one valid option
    if len(dev_range) == 1:
        return EXPERIMENTS[exp_ind][2]

    print('Max number of devices for this experiment: {}'.format(
        EXPERIMENTS[exp_ind][3]))
    # Get it from the command line argument list
    if len(argv) > 2:
        dev_num = argv[2]
    # Or prompt the user for it
    else:
        dev_num = input('Enter connected devices [or q to quit]: ')
        if dev_num.lower() == 'q':
            sys.exit(0)

    # Make sure it's valid and in range:
    if not dev_num.isdecimal():  # Filter out letters
        sys.exit('Please enter number')

    dev_num = int(dev_num)  # Make sure is a int and not a string
    # And make sure it's in range
    if dev_num in dev_range:
        return dev_num

    sys.exit('Please choose a number of device between {} and {}'.format(
        EXPERIMENTS[exp_ind][2], EXPERIMENTS[exp_ind][3]))


def main(argv):
    """
    Interactive menu for experiment selection and running
    """
    signal(SIGINT, sig_handler)  # Handle Ctrl-C or SIGINT
    fxu.print_logo()

    # Handles command line arguments and experiment setup
    if len(argv) <= 3:
        print_experiments()
        exp_ind = get_exp_ind(argv)
        dev_num = get_dev_num(argv, exp_ind)
    else:
        print_usage(argv[0])
        sys.exit('\nToo many command line arguments provided.')

    print('\nRunning Experiment [{}] with [{}] connected device{}.'.format(
        exp_ind, dev_num, 's' if dev_num > 1 else ''))

    port_cfg_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'ports.yaml')
    ports, baud_rate = fxu.load_ports_from_file(port_cfg_path)
    print('Using ports:\t{}'.format(ports))
    print('Using baud rate:\t{}'.format(baud_rate))

    # TODO (CA): add support for n ports
    # Call selected demo script:
    try:
        if dev_num == 1:
            EXPERIMENTS[exp_ind][0](flex.FlexSEA(), ports[0], baud_rate)
        elif dev_num == 2:
            EXPERIMENTS[exp_ind][0](
                flex.FlexSEA(), ports[0], baud_rate, ports[1])
        else:
            raise RuntimeError('Unsupported number of devices.')
    except Exception as err:
        print('Problem encountered when running the demo: {}'.format(err))
        sys.exit(err)

    print('\nExiting {} normally...\n'.format(argv[0]))
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
