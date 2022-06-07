"""
General purpose utilities
"""
import ctypes as c
import os
import platform

import numpy as np
import yaml

from . import fx_enums as fxe
from .dev_spec import AllDevices as fx_devs


# ============================================
#                 print_logo
# ============================================
def print_logo():
    """
    print cool logo.
    """
    logo_str = """
	▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
	██░▄▄▀██░▄▄▄██░▄▄░██░██░██░███░██
	██░██░██░▄▄▄██░▀▀░██░▄▄░██▄▀▀▀▄██
	██░▀▀░██░▀▀▀██░█████░██░████░████
	▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n\t          Beyond Nature™
	"""
    try:
        print(logo_str)
    except UnicodeEncodeError:
        print("\tDephy\n\tBeyond Nature (TM)")


# ============================================
#                   is_win
# ============================================
def is_win():
    """
    Returns true if the OS is windows
    """
    return "win" in platform.system().lower()


# ============================================
#                    is_pi
# ============================================
def is_pi():
    """
    Returns true if the OS is running on an arm. Used to detect Raspberry pi
    """
    try:
        return os.uname().machine.startswith("arm")
    except AttributeError:
        return False


# ============================================
#                   is_pi64
# ============================================
def is_pi64():
    """
    Returns true if the OS is running on an Ubuntu 64 for Arm. Used to detect Raspberry pi aarch64
    """
    try:
        return os.uname().machine.startswith("aarch64")
    except AttributeError:
        return False


# ============================================
#                    decode
# ============================================
def decode(val):
    """
    Returns decoded version number formatted as x.y.z
    """
    major = minor = bug = 0

    if val > 0:
        while val % 2 == 0:
            major += 1
            val /= 2

        while val % 3 == 0:
            minor += 1
            val /= 3

        while val % 5 == 0:
            bug += 1
            val /= 5

    return f"{major}.{minor}.{bug}"


# ============================================
#                clear_terminal
# ============================================
def clear_terminal():
    """
    Clears the terminal - use before printing new values
    """
    os.system("cls" if is_win() else "clear")


# ============================================
#               print_plot_exit
# ============================================
def print_plot_exit():
    """
    Prints plot exit message
    """
    if is_win():
        print("In Windows, press Ctrl+Break to exit. Ctrl+C may not work.")


# ============================================
#                 print_device
# ============================================
def print_device(dev_id, app_type):
    """
    Print device type given ann Application type

    Parameters:
    dev_id (int): The device ID.
    app_type (int): application type.
    """
    # NOTE: We could just loop over state._fields_ instead of having
    # all of thse different print functions:
    # for f in state._fields_: print(f"{f[0]}: {getattr(state, f[0])})
    if app_type.value == fxe.FX_ACT_PACK.value:
        print_act_pack(dev_id)
    elif app_type.value == fxe.FX_NET_MASTER.value:
        print_net_master(dev_id)
    elif app_type.value == fxe.FX_BMS.value:
        print_bms(dev_id)
    elif app_type.value == fxe.FX_EB5X.value:
        print_eb5x(dev_id)
    elif app_type.value == fxe.FX_MD.value:
        print_md(dev_id)
    else:
        raise RuntimeError("Unsupported application type: ", app_type)


# ============================================
#                 print_eb5x
# ============================================
def print_eb5x(eb5x_state: fx_devs.EB5xState):
    """
    Print eb5x info
    """
    print("[ Printing EB5x/ActPack Plus ]\n")
    print("State time:           ", eb5x_state.state_time)
    print("Accel X:              ", eb5x_state.accelx)
    print("Accel Y:              ", eb5x_state.accely)
    print("Accel Z:              ", eb5x_state.accelz)
    print("Gyro X:               ", eb5x_state.gyrox)
    print("Gyro Y:               ", eb5x_state.gyroy)
    print("Gyro Z:               ", eb5x_state.gyroz)
    print("Motor angle:          ", eb5x_state.mot_ang)
    print("Motor voltage (mV):   ", eb5x_state.mot_volt)
    print("Motor current (mA):   ", eb5x_state.mot_cur)
    print("Battery Current (mA): ", eb5x_state.batt_volt)
    print("Battery Voltage (mV): ", eb5x_state.batt_curr)
    print("Battery Temp (C):     ", eb5x_state.temperature)
    print("genVar[0]:            ", eb5x_state.genvar_0)
    print("genVar[1]:            ", eb5x_state.genvar_1)
    print("genVar[2]:            ", eb5x_state.genvar_2)
    print("genVar[3]:            ", eb5x_state.genvar_3)
    print("genVar[4]:            ", eb5x_state.genvar_4)
    print("genVar[5]:            ", eb5x_state.genvar_5)
    print("genVar[6]:            ", eb5x_state.genvar_6)
    print("genVar[7]:            ", eb5x_state.genvar_7)
    print("genVar[8]:            ", eb5x_state.genvar_8)
    print("genVar[9]:            ", eb5x_state.genvar_9)
    print("Ankle angle:          ", eb5x_state.ank_ang)
    print("Ankle velocity:       ", eb5x_state.ank_vel)


# ============================================
#                   print_md
# ============================================
def print_md(md10_state: fx_devs.MD10State):
    """
    Print md info
    """
    print("[ Printing Medical Device ]\n")
    print("State time:           ", md10_state.state_time)
    print("Accel X:              ", md10_state.accelx)
    print("Accel Y:              ", md10_state.accely)
    print("Accel Z:              ", md10_state.accelz)
    print("Gyro X:               ", md10_state.gyrox)
    print("Gyro Y:               ", md10_state.gyroy)
    print("Gyro Z:               ", md10_state.gyroz)
    print("Motor angle:          ", md10_state.mot_ang)
    print("Motor voltage (mV):   ", md10_state.mot_volt)
    print("Motor current (mA):   ", md10_state.mot_cur)
    print("Battery Current (mA): ", md10_state.batt_volt)
    print("Battery Voltage (mV): ", md10_state.batt_curr)
    print("Battery Temp (C):     ", md10_state.temperature)
    print("genVar[0]:            ", md10_state.genvar_0)
    print("genVar[1]:            ", md10_state.genvar_1)
    print("genVar[2]:            ", md10_state.genvar_2)
    print("genVar[3]:            ", md10_state.genvar_3)
    print("genVar[4]:            ", md10_state.genvar_4)
    print("genVar[5]:            ", md10_state.genvar_5)
    print("genVar[6]:            ", md10_state.genvar_6)
    print("genVar[7]:            ", md10_state.genvar_7)
    print("genVar[8]:            ", md10_state.genvar_8)
    print("genVar[9]:            ", md10_state.genvar_9)
    print("Ankle angle:          ", md10_state.ank_ang)
    print("Ankle velocity:       ", md10_state.ank_vel)


# ============================================
#               print_act_pack
# ============================================
def print_act_pack(act_pack_state: fx_devs.ActPackState):
    """
    Print ActPack info
    """
    print("[ Printing ActPack ]\n")
    print("State time:           ", act_pack_state.state_time)
    print("Accel X:              ", act_pack_state.accelx)
    print("Accel Y:              ", act_pack_state.accely)
    print("Accel Z:              ", act_pack_state.accelz)
    print("Gyro X:               ", act_pack_state.gyrox)
    print("Gyro Y:               ", act_pack_state.gyroy)
    print("Gyro Z:               ", act_pack_state.gyroz)
    print("Motor angle:          ", act_pack_state.mot_ang)
    print("Motor voltage (mV):   ", act_pack_state.mot_volt)
    print("Battery Current (mA): ", act_pack_state.batt_curr)
    print("Battery Voltage (mV): ", act_pack_state.batt_volt)
    print("Battery Temp (C):     ", act_pack_state.temperature)


# ============================================
#               print_net_master
# ============================================
def print_net_master(net_master_state: fx_devs.NetMasterState):
    """
    Print net master info
    """
    print("[ Printing NetMaster ]\n")
    print("State time:        ", net_master_state.state_time)
    print("genVar[0]:         ", net_master_state.genVar_0)
    print("genVar[1]:         ", net_master_state.genVar_1)
    print("genVar[2]:         ", net_master_state.genVar_2)
    print("genVar[3]:         ", net_master_state.genVar_3)
    print("Status:            ", net_master_state.status)
    print(
        "NetNode0 - accelx: ",
        net_master_state.A_accelx,
        ", accely: ",
        net_master_state.A_accely,
        " accelz: ",
        net_master_state.A_accelz,
    )
    print(
        "NetNode0 - gyrox:  ",
        net_master_state.A_gyrox,
        ", gyroy:  ",
        net_master_state.A_gyroy,
        " gyroz:  ",
        net_master_state.A_gyroz,
    )
    print(
        "NetNode1 - accelx: ",
        net_master_state.B_accelx,
        ", accely: ",
        net_master_state.B_accely,
        " accelz: ",
        net_master_state.B_accelz,
    )
    print(
        "NetNode1 - gyrox:  ",
        net_master_state.B_gyrox,
        ", gyroy:  ",
        net_master_state.B_gyroy,
        " gyroz:  ",
        net_master_state.B_gyroz,
    )
    print(
        "NetNode2 - accelx: ",
        net_master_state.C_accelx,
        ", accely: ",
        net_master_state.C_accely,
        " accelz: ",
        net_master_state.C_accelz,
    )
    print(
        "NetNode2 - gyrox:  ",
        net_master_state.C_gyrox,
        ", gyroy:  ",
        net_master_state.C_gyroy,
        " gyroz:  ",
        net_master_state.C_gyroz,
    )
    print(
        "NetNode3 - accelx: ",
        net_master_state.D_accelx,
        ", accely: ",
        net_master_state.D_accely,
        " accelz: ",
        net_master_state.D_accelz,
    )
    print(
        "NetNode3 - gyrox:  ",
        net_master_state.D_gyrox,
        ", gyroy:  ",
        net_master_state.D_gyroy,
        " gyroz:  ",
        net_master_state.D_gyroz,
    )
    print(
        "NetNode4 - accelx: ",
        net_master_state.E_accelx,
        ", accely: ",
        net_master_state.E_accely,
        " accelz: ",
        net_master_state.E_accelz,
    )
    print(
        "NetNode4 - gyrox:  ",
        net_master_state.E_gyrox,
        ", gyroy:  ",
        net_master_state.E_gyroy,
        " gyroz:  ",
        net_master_state.E_gyroz,
    )
    print(
        "NetNode5 - accelx: ",
        net_master_state.F_accelx,
        ", accely: ",
        net_master_state.F_accely,
        " accelz: ",
        net_master_state.F_accelz,
    )
    print(
        "NetNode5 - gyrox:  ",
        net_master_state.F_gyrox,
        ", gyroy:  ",
        net_master_state.F_gyroy,
        " gyroz:  ",
        net_master_state.F_gyroz,
    )
    print(
        "NetNode6 - accelx: ",
        net_master_state.G_accelx,
        ", accely: ",
        net_master_state.G_accely,
        " accelz: ",
        net_master_state.G_accelz,
    )
    print(
        "NetNode6 - gyrox:  ",
        net_master_state.G_gyrox,
        ", gyroy:  ",
        net_master_state.G_gyroy,
        " gyroz:  ",
        net_master_state.G_gyroz,
    )
    print(
        "NetNode7 - accelx: ",
        net_master_state.H_accelx,
        ", accely: ",
        net_master_state.H_accely,
        " accelz: ",
        net_master_state.H_accelz,
    )
    print(
        "NetNode7 - gyrox:  ",
        net_master_state.H_gyrox,
        ", gyroy:  ",
        net_master_state.H_gyroy,
        " gyroz:  ",
        net_master_state.H_gyroz,
    )


# ============================================
#                 print_bms
# ============================================
def print_bms(dev_id):
    """Print BMS info"""
    # TODO (CA): Implement this function
    print(f"Printing BMS information not implemented. Device {dev_id}")


# ============================================
#              print_loop_count
# ============================================
def print_loop_count(count, total):
    """
    Convenience function for printing run counts
    """
    print(f"\nRun {count + 1} of {total}")


# ============================================
#         print_loop_count_and_time
# ============================================
def print_loop_count_and_time(count, total, elapsed_time):
    """
    Convenience function for printing run counts and elapsed time in s.
    """
    print(f"\nLoop {count + 1} of {total} - Elapsed time: {round(elapsed_time)}s")


# ============================================
#                sin_generator
# ============================================
def sin_generator(amplitude, freq, command_freq):
    """
    Generate a sine wave of a specific amplitude and frequency
    """
    num_samples = command_freq / freq
    print(f"number of samples is: {int(num_samples)}")
    in_array = np.linspace(-np.pi, np.pi, int(num_samples))
    sin_vals = amplitude * np.sin(in_array)
    return sin_vals


# ============================================
#               line_generator
# ============================================
def line_generator(mag, length, command_freq):
    """
    Generate a line with specific magnitude
    """
    num_samples = np.int32(length * command_freq)
    line_vals = [mag for i in range(num_samples)]
    return line_vals


# ============================================
#                linear_interp
# ============================================
def linear_interp(start, end, points):
    """
    Interpolates between two positions (A to B)
    """
    return np.linspace(start, end, points)


# ============================================
#            load_ports_from_file
# ============================================
def load_ports_from_file(file_name):
    """
    Loads baud_rate and ports serial ports list from a yaml file.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as com_file:
            vals = yaml.load(com_file, Loader=yaml.FullLoader)
            return vals["ports"], int(vals["baud_rate"])

    except IOError as err:
        print(f"Problem loading {file_name}: {err}")
        print(
            "Copy the ports_template.yaml to a file named ports.yaml"
            "Be sure to use the same format of baud rate on the first line,"
            "and com ports on preceding lines"
        )
        raise err
    except ValueError as err:
        print(f"Problem with the yaml file syntax or values: {err}")
        raise err


# ============================================
#                  _get_os
# ============================================
def _get_os() -> str:
    """
    Determines which operating system we're running on.

    Returns
    -------
    str:
            The name of the operating system. Matches the directory inside
            `libs` containing the c libraries appropriate for that OS.
    """
    # Windows
    if "win" in platform.system().lower():
        # 32 bit
        if platform.architecture()[0] == "32bit":
            operating_system = "win32"
        # 64 bit
        else:
            operating_system = "win64"
    # Pi - 32 bit
    elif os.uname().machine.startswith("arm"):
        operating_system = "raspberryPi"
    # Pi - 64 bit
    elif os.uname().machine.startswith("aarch64"):
        operating_system = "raspberryPi64"
    # This check is specifically after the pi check because the pi also
    # returns 'Linux' from platform.system()
    elif "linux" in platform.system().lower():
        operating_system = "linux"
    else:
        raise OSError("Unknown operating system!")
    return operating_system


# ============================================
#                  _add_dlls
# ============================================
def _add_dlls(lib_path: str) -> None:
    """
    Explicitly adds the appropriate directories to the `PATH` on Windows.

    Parameters
    ----------
    lib_path : str
            The full path to the directory containing the Windows
            precompiled libraries.
    """
    for extra_path in os.environ["PATH"].split(";"):
        if os.path.exists(extra_path) and "mingw" in extra_path:
            os.add_dll_directory(extra_path)
    os.add_dll_directory(lib_path)


# ============================================
#             _set_data_types
# ============================================
def _set_data_types(clib: c.CDLL) -> c.CDLL:
    """
    Defines the function prototypes.

    Parameters
    ----------
    clib : c.CDLL
            The Python object interfacing with the C libraries we're
            setting the prototypes for.

    Returns
    -------
    clib : c.CDLL
            The Python object interfacing with the C libraries for which
            we've set the prototypes.
    """
    clib.fxOpen.argtypes = [c.c_char_p, c.c_uint, c.c_uint]
    clib.fxOpen.restype = c.c_int

    clib.fxIsOpen.argtypes = [c.c_uint]
    clib.fxIsOpen.restype = c.c_bool

    clib.fxClose.argtypes = [c.c_uint]
    clib.fxClose.restype = c.c_int

    clib.fxCloseAll.argtypes = []
    clib.fxCloseAll.resType = []

    clib.fxGetDeviceIds.argtypes = [c.POINTER(c.c_int), c.c_uint]

    clib.fxStartStreaming.argtypes = [c.c_uint, c.c_uint, c.c_bool]
    clib.fxStartStreaming.restype = c.c_int

    clib.fxStopStreaming.argtypes = [c.c_uint]
    clib.fxStopStreaming.restype = c.c_int

    clib.fxReadDevice.argtypes = [c.c_uint, c.POINTER(fx_devs.ActPackState)]
    clib.fxReadDevice.restype = c.c_int

    clib.fxReadDeviceAll.argtypes = [
        c.c_uint,
        c.POINTER(fx_devs.ActPackState),
        c.c_uint,
    ]
    clib.fxReadDeviceAll.restype = c.c_int

    clib.fxReadMdDeviceAll.argtypes = [
        c.c_uint,
        c.POINTER(fx_devs.MD10State),
        c.c_uint,
    ]
    clib.fxReadMdDeviceAll.restype = c.c_int
    clib.fxReadMdDevice.argtypes = [c.c_uint, c.POINTER(fx_devs.MD10State)]
    clib.fxReadMdDeviceAll.restype = c.c_int

    clib.fxReadNetMasterDevice.argtypes = [c.c_uint, c.POINTER(fx_devs.NetMasterState)]
    clib.fxReadDevice.restype = c.c_int

    clib.fxReadNetMasterDeviceAll.argtypes = [
        c.c_uint,
        c.POINTER(fx_devs.NetMasterState),
        c.c_uint,
    ]
    clib.fxReadNetMasterDeviceAll.restype = c.c_int

    clib.fxSetReadDataQueueSize.argtypes = [c.c_uint, c.c_uint]
    clib.fxSetReadDataQueueSize.restype = c.c_uint

    clib.fxGetReadDataQueueSize.argtypes = [c.c_uint]
    clib.fxGetReadDataQueueSize.restype = c.c_int

    clib.fxSetGains.argtypes = [
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
        c.c_uint,
    ]
    clib.fxSetGains.restype = c.c_int

    clib.fxSendMotorCommand.argtypes = [c.c_uint, c.c_int, c.c_int]
    clib.fxSendMotorCommand.restype = c.c_int

    clib.fxGetAppType.argtypes = [c.c_uint]

    clib.fxActivateBootloader.argtypes = [c.c_uint, c.c_uint8]
    clib.fxActivateBootloader.restype = c.c_int

    clib.fxIsBootloaderActivated.argtypes = [c.c_uint]
    clib.fxIsBootloaderActivated.restype = c.c_int

    clib.fxRequestFirmwareVersion.argtypes = [c.c_uint]
    clib.fxRequestFirmwareVersion.restype = c.c_int

    clib.fxGetLastReceivedFirmwareVersion.argtypes = [c.c_uint]
    clib.fxGetLastReceivedFirmwareVersion.restype = fxe.FW

    return clib


# ============================================
#                 _load_clib
# ============================================
def _load_clib() -> c.CDLL:
    """
    Uses `ctypes` to load the appropriate C libraries depending on the
    OS.

    Raises
    ------
    OSError:
            Raised if the precompiled libraries fail to load.

    Returns
    -------
    clib : ctypes.cdll.CDLL
            The Python object from which we can call the flexsea C
            functions.
    """
    nix_lib = "libfx_plan_stack.so"
    win_lib = "libfx_plan_stack.dll"
    libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs")
    os.environ["PATH"] += libs_path

    operating_system = _get_os()
    lib_path = os.path.join(libs_path, operating_system)

    if "win" in operating_system:
        try:
            _add_dlls(lib_path)
            clib = c.cdll.LoadLibrary(os.path.join(lib_path, win_lib))
        except OSError as err:
            msg = f"\n[!] Error loading the {win_lib} precompiled libraries.\n"
            msg += (
                "The most likely cause is a mismatch between the Python, pip and shell "
                "architectures.\n"
            )
            msg += "To solve this, ensure all three are either 32 or 64 bit.\n"
            msg += "Keep different versions isolated by virtual environments.\n"
            msg += "For additional help, follow the installation instructions here: "
            msg += "https://github.com/DephyInc/Actuator-Package\n"
            msg += "--------------------------------------------\n\n"
            msg += f"Detailed error message for debugging:\n{err}\n"
            print(msg)
    else:
        clib = c.cdll.LoadLibrary(os.path.join(lib_path, nix_lib))

    return _set_data_types(clib)
