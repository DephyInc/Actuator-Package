"""
General purpose utilities
"""
import fxEnums as en
import numpy as np
import os
import platform
from .dev_spec import AllDevices as fx_devs
import yaml


def is_win():
    """
    Returns true if the OS is windows
    """
    return 'win' in platform.system().lower()


def is_pi():
    """
    Returns true if the OS is running on an arm. Used to detect Raspberry pi
    """
    try:
        return os.uname().startswith('arm')
    except AttributeError:
        return False


def clear_terminal():
    """
    Clears the terminal - use before printing new values
    """
    os.system('cls' if is_win() else 'clear')


def print_plot_exit():
    """
    Prints plot exit message
    """
    if is_win():
        print('In Windows, press Ctrl+BREAK to exit. Ctrl+C may not work.')


def print_device(dev_id, app_type):
    """
    Print device type given ann Application type

    Parameters:
    dev_id (int): The device ID.
    app_type (int): application type.

    """
    if app_type == en.FX_ACT_PACK:
        print_act_pack(dev_id)
    elif app_type == en.FX_NET_MASTER:
        print_net_master(dev_id)
    elif app_type == en.FX_B_M_S:
        print_bms(dev_id)
    elif app_type == en.FX_EXO:
        print_exo(dev_id)
    else:
        raise RuntimeError('Unsupported application type: ', app_type)


def print_exo(exoState: fx_devs.ExoState):
    print('[ Printing Exo/ActPack Plus ]\n')
    print('State time:           ', exoState.state_time)
    print('Accel X:              ', exoState.accelx)
    print('Accel Y:              ', exoState.accely)
    print('Accel Z:              ', exoState.accelz)
    print('Gyro X:               ', exoState.gyrox)
    print('Gyro Y:               ', exoState.gyroy)
    print('Gyro Z:               ', exoState.gyroz)
    print('Motor angle:          ', exoState.mot_ang)
    print('Motor voltage (mV):   ', exoState.mot_volt)
    print('Motor current (mA):   ', exoState.mot_cur)
    print('Battery Current (mA): ', exoState.batt_volt)
    print('Battery Voltage (mV): ', exoState.batt_curr)
    print('Battery Temp (C):     ', exoState.temperature)
    print('genVar[0]:            ', exoState.genvar_0)
    print('genVar[1]:            ', exoState.genvar_1)
    print('genVar[2]:            ', exoState.genvar_2)
    print('genVar[3]:            ', exoState.genvar_3)
    print('genVar[4]:            ', exoState.genvar_4)
    print('genVar[5]:            ', exoState.genvar_5)
    print('genVar[6]:            ', exoState.genvar_6)
    print('genVar[7]:            ', exoState.genvar_7)
    print('genVar[8]:            ', exoState.genvar_8)
    print('genVar[9]:            ', exoState.genvar_9)
    print('Ankle angle:          ', exoState.ank_ang)
    print('Ankle velocity:       ', exoState.ank_vel)


def print_act_pack(actPackState: fx_devs.ActPackState):
    print('[ Printing Actpack ]\n')
    print('State time:           ', actPackState.state_time)
    print('Accel X:              ', actPackState.accelx)
    print('Accel Y:              ', actPackState.accely)
    print('Accel Z:              ', actPackState.accelz)
    print('Gyro X:               ', actPackState.gyrox)
    print('Gyro Y:               ', actPackState.gyroy)
    print('Gyro Z:               ', actPackState.gyroz)
    print('Motor angle:          ', actPackState.mot_ang)
    print('Motor voltage (mV):   ', actPackState.mot_volt)
    print('Battery Current (mA): ', actPackState.batt_curr)
    print('Battery Voltage (mV): ', actPackState.batt_volt)
    print('Battery Temp (C):     ', actPackState.temperature)


def print_net_master(netMasterState: fx_devs.NetMasterState):
    print('[ Printing NetMaster ]\n')
    print('State time:        ', netMasterState.state_time)
    print('genVar[0]:         ', netMasterState.genVar_0)
    print('genVar[1]:         ', netMasterState.genVar_1)
    print('genVar[2]:         ', netMasterState.genVar_2)
    print('genVar[3]:         ', netMasterState.genVar_3)
    print('Status:            ', netMasterState.status)
    print('NetNode0 - accelx: ', netMasterState.A_accelx, ', accely: ',
          netMasterState.A_accely, ' accelz: ', netMasterState.A_accelz)
    print('NetNode0 - gyrox:  ', netMasterState.A_gyrox, ', gyroy:  ',
          netMasterState.A_gyroy, ' gyroz:  ', netMasterState.A_gyroz)
    print('NetNode1 - accelx: ', netMasterState.B_accelx, ', accely: ',
          netMasterState.B_accely, ' accelz: ', netMasterState.B_accelz)
    print('NetNode1 - gyrox:  ', netMasterState.B_gyrox, ', gyroy:  ',
          netMasterState.B_gyroy, ' gyroz:  ', netMasterState.B_gyroz)
    print('NetNode2 - accelx: ', netMasterState.C_accelx, ', accely: ',
          netMasterState.C_accely, ' accelz: ', netMasterState.C_accelz)
    print('NetNode2 - gyrox:  ', netMasterState.C_gyrox, ', gyroy:  ',
          netMasterState.C_gyroy, ' gyroz:  ', netMasterState.C_gyroz)
    print('NetNode3 - accelx: ', netMasterState.D_accelx, ', accely: ',
          netMasterState.D_accely, ' accelz: ', netMasterState.D_accelz)
    print('NetNode3 - gyrox:  ', netMasterState.D_gyrox, ', gyroy:  ',
          netMasterState.D_gyroy, ' gyroz:  ', netMasterState.D_gyroz)
    print('NetNode4 - accelx: ', netMasterState.E_accelx, ', accely: ',
          netMasterState.E_accely, ' accelz: ', netMasterState.E_accelz)
    print('NetNode4 - gyrox:  ', netMasterState.E_gyrox, ', gyroy:  ',
          netMasterState.E_gyroy, ' gyroz:  ', netMasterState.E_gyroz)
    print('NetNode5 - accelx: ', netMasterState.F_accelx, ', accely: ',
          netMasterState.F_accely, ' accelz: ', netMasterState.F_accelz)
    print('NetNode5 - gyrox:  ', netMasterState.F_gyrox, ', gyroy:  ',
          netMasterState.F_gyroy, ' gyroz:  ', netMasterState.F_gyroz)
    print('NetNode6 - accelx: ', netMasterState.G_accelx, ', accely: ',
          netMasterState.G_accely, ' accelz: ', netMasterState.G_accelz)
    print('NetNode6 - gyrox:  ', netMasterState.G_gyrox, ', gyroy:  ',
          netMasterState.G_gyroy, ' gyroz:  ', netMasterState.G_gyroz)
    print('NetNode7 - accelx: ', netMasterState.H_accelx, ', accely: ',
          netMasterState.H_accely, ' accelz: ', netMasterState.H_accelz)
    print('NetNode7 - gyrox:  ', netMasterState.H_gyrox, ', gyroy:  ',
          netMasterState.H_gyroy, ' gyroz:  ', netMasterState.H_gyroz)


def print_bms(dev_id):
    """Print BMS info"""
    # TODO (CA): Implement this function
    print('Printing BMS information not implemented. Device {}'.format(dev_id))


def print_loop_count(count, total):
    """
    Convenience function for printing run counts
    """
    print('\nRun {} of {}'.format(count + 1, total))


def print_loop_count_and_time(count, total, elapsed_time):
    """
    Convenience function for printing run counts and elapsed time in s.
    """
    print('\nLoop {} of {} - Elapsed time: {}s'.format(
        count + 1, total, round(elapsed_time)))


def sin_generator(amplitude, freq, command_freq):
    """
    Generate a sine wave of a specific amplitude and frequency
    """
    num_samples = command_freq / freq
    print("number of samples is: ", int(num_samples))
    in_array = np.linspace(-np.pi, np.pi, int(num_samples))
    sin_vals = amplitude * np.sin(in_array)
    return sin_vals


def line_generator(mag, length, command_freq):
    """
    Generate a line with specific magnitude
    """
    num_samples = np.int32(length * command_freq)
    line_vals = [mag for i in range(num_samples)]
    return line_vals


def linear_interp(start, end, points):
    """
    Interpolates between two positions (A to B)
    """
    return np.linspace(start, end, points)


def load_ports_from_file(file_name):
    """
    Loads baud_rate and ports serial ports list from a yaml file.
    """
    try:
        with open(file_name, 'r') as com_file:
            vals = yaml.load(com_file, Loader=yaml.FullLoader)
            return vals['ports'], int(vals['baud_rate'])

    except IOError as err:
        print('Problem loading {}: {}'.format(file_name, err))
        print('Copy the ports_template.yaml to a file named ports.yaml'
              'Be sure to use the same format of baud rate on the first line,'
              'and com ports on preceding lines')
        raise err
    except ValueError as err:
        print('Problem with the yaml file syntax or values: {}', err)
        raise err
