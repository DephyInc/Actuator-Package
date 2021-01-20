#!/usr/bin/env python3

"""
FlexSEA Read Only Demo
"""
import sys
from time import sleep
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex


def print_bms_state(fx, dev_id):
    """
    Read BMS info
    """
    bms_state = fx.read_bms_device_all(dev_id, 1)
    for i in range(9):
        print('Cell [{}] Voltage: {}'.format(i, bms_state.cellVoltage[i]))
    for i in range(3):
        print('Temperature [{}]: {}'.format(i, bms_state.temperature[i]))


def fx_read_only(fx, port, baud_rate, run_time=8, time_step=0.1):
    """
    Reads FlexSEA device and prins gathered data.
    """
    debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
    data_log = True          # False means no logs will be saved
    dev_id = fx.open(port, baud_rate, debug_logging_level)
    fx.start_streaming(dev_id, freq=100, log_en=data_log)
    app_type = fx.get_app_type(dev_id)

    if app_type.value == fxe.FX_ACT_PACK.value:
        print('\nYour device is an ActPack.\n')
        input("Press Enter to continue...")
    elif app_type.value == fxe.FX_NET_MASTER.value:
        print('\nYour device is a NetMaster.\n')
        input("Press Enter to continue...")
    elif app_type.value == fxe.FX_BMS.value:
        print('\nYour device is a BMS.\n')
        input("Press Enter to continue...")
    elif app_type.value == fxe.FX_EXO.value:
        print('\nYour device is an Exo or ActPack Plus.\n')
        input("Press Enter to continue...")
    else:
        raise RuntimeError(f'Unsupported application type: {app_type}')

    total_loop_count = int(run_time / time_step)
    for i in range(total_loop_count):
        fxu.print_loop_count(i, total_loop_count)
        sleep(time_step)
        fxu.clear_terminal()
        data = fx.read_device(dev_id)
        fxu.print_device(data, app_type)
    fx.close(dev_id)
    return True


def main():
    """
    Standalone execution
    """
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', metavar='P', type=str, nargs=1,
                        help='Your device serial port.')
    parser.add_argument('-b', '--baud', metavar='B', dest='baudrate', type=int,
                        default=230400, help='Serial communication baudrate.')
    args = parser.parse_args()

    fx_read_only(flex.FlexSEA(), args.port, args.baud)


if __name__ == '__main__':
    main()
