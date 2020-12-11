"""
Dephy's FlexSEA Python API
"""
import ctypes as c
import os
import sys
import platform
import fxEnums as en
from .dev_spec import AllDevices as fx_devs

# TODO (CA): make Flexsea devices into objets that can be instantiated and keep
# track of their state


class FlexSEA:
    """
    Implements FlexSEA Actuator Package API
    Device ID is an alphanumeric ID used to refer to a specific FlexSEA device.
    Device ID is returned by fxOpen upon establishing a connection with a
    FlexSEA device, and is used by most of the functions in this library to
    specify which device to run that function on.
    """

    def __init__(self):
        self.ids = list()
        self.c_lib = None
        self.load_c_libs()

    def load_c_libs(self):
        """Loads the library from the c lib"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lib_paths = list()
        if 'win' in platform.system().lower():
            # load proper library based on host architecture
            if platform.architecture()[0] == '32bit':
                path_base = os.path.join(dir_path, '../../libs/win32')
            else:
                path_base = os.path.join(dir_path, '../../libs/win64')
            lib_paths = [os.path.join(path_base, 'libfx_plan_stack.dll')]
            # Python 3.8+ requires location of all DLLs AND their dependencies
            # be explicitly stated. Provide location of DLLs that
            # libfx_plan_stack.dll depends on
            if sys.version_info.minor >= 8:
                os.add_dll_directory(os.path.join(dir_path, '../'))
        else:
            # Try to load the full linux lib first (that's x86_64), if that
            # fails, fall back to the raspberryPi lib.
            lib_paths = [
                os.path.join(dir_path, '../../libs/linux',
                             'libfx_plan_stack.so'),
                os.path.join(dir_path, '../../libs/raspberryPi',
                             'libfx_plan_stack.so'),
                os.path.join(dir_path, '../../libs/raspberryPi64',
                             'libfx_plan_stack.so'),
            ]

        loading_log_messages = list()
        for path in lib_paths:
            try:
                loading_log_messages.append('loading... ' + path)
                self.c_lib = c.cdll.LoadLibrary(path)
            except OSError as err:
                loading_log_messages.append(
                    'Problem loading the library\n {}\n'.format(err))
                print('\n'.join(loading_log_messages))
                raise err

        print('FlexSEA libraries loaded')

        # set arg types
        self.c_lib.fxOpen.argtypes = [c.c_char_p, c.c_uint, c.c_uint]
        self.c_lib.fxOpen.restype = c.c_int

        self.c_lib.fxIsOpen.argtypes = [c.c_uint]
        self.c_lib.fxIsOpen.restype = c.c_bool

        self.c_lib.fxClose.argtypes = [c.c_uint]
        self.c_lib.fxClose.restype = c.c_int

        self.c_lib.fxCloseAll.argtypes = []
        self.c_lib.fxCloseAll.resType = []

        self.c_lib.fxGetDeviceIds.argtypes = [c.POINTER(c.c_int), c.c_uint]

        self.c_lib.fxStartStreaming.argtypes = [c.c_uint, c.c_uint, c.c_bool]
        self.c_lib.fxStartStreaming.restype = c.c_int

        self.c_lib.fxStopStreaming.argtypes = [c.c_uint]
        self.c_lib.fxStopStreaming.restype = c.c_int

        self.c_lib.fxReadDevice.argtypes = [
            c.c_uint, c.POINTER(fx_devs.ActPackState)]
        self.c_lib.fxReadDevice.restype = c.c_int

        self.c_lib.fxReadDeviceAll.argtypes = [
            c.c_uint, c.POINTER(fx_devs.ActPackState), c.c_uint]
        self.c_lib.fxReadDeviceAll.restype = c.c_int

        self.c_lib.fxReadNetMasterDevice.argtypes = [
            c.c_uint, c.POINTER(fx_devs.NetMasterState)]
        self.c_lib.fxReadDevice.restype = c.c_int

        self.c_lib.fxReadNetMasterDeviceAll.argtypes = [
            c.c_uint, c.POINTER(fx_devs.NetMasterState), c.c_uint]
        self.c_lib.fxReadNetMasterDeviceAll.restype = c.c_int

        self.c_lib.fxSetReadDataQueueSize.argtypes = [c.c_uint, c.c_uint]
        self.c_lib.fxSetReadDataQueueSize.restype = c.c_uint

        self.c_lib.fxGetReadDataQueueSize.argtypes = [c.c_uint]
        self.c_lib.fxGetReadDataQueueSize.restype = c.c_int

        self.c_lib.fxSetGains.argtypes = [
            c.c_uint, c.c_uint, c.c_uint,
            c.c_uint, c.c_uint, c.c_uint, c.c_uint]
        self.c_lib.fxSetGains.restype = c.c_int

        self.c_lib.fxSendMotorCommand.argtypes = [c.c_uint, c.c_int, c.c_int]
        self.c_lib.fxSendMotorCommand.restype = c.c_int

        self.c_lib.fxGetAppType.argtypes = [c.c_uint]

    def open(self, port, baud_rate, log_level=4):
        """
        Establish a connection with a FlexSEA device.

        Parameters:
        portName (string): The name of the serial port to open (e.g. "COM3")

        baudRate (int): The baud rate used i.e. 115200, 230400, etc.

        logLevel (int): is the logging level for this device. 0 is most verbose and
        6 is the least verbose. Values greater than 6 are floored to 6.

        Raises:
        IOError if we fail to open the device.
        """
        dev_id = self.c_lib.fxOpen(port.encode('utf-8'), baud_rate, log_level)

        if dev_id == -1:
            raise IOError('Failed to open device')
        self.ids.append(dev_id)
        return dev_id

    def close(self, dev_id):
        """
        Disconnect from a FlexSEA device with the given device ID.

        Parameters:
        dev_id (int): The ID of the device to close

        Raises:
        ValueError if the device ID is invalid
        """
        self.ids.remove(dev_id)
        if self.c_lib.fxClose(dev_id) == en.FX_INVALID_DEVICE:
            raise ValueError('fxClose: invalid device ID')

    def close_all(self):
        """
        Disconnect from all FlexSEA devices
        """
        self.c_lib.fxCloseAll()

    def get_ids(self):
        """
        Get the device IDs of all connected FlexSEA devices.

        The device ID is used by the functions in this API to specify which
        FlexSEA device to communicate with.

        Returns:
        A list containing either valid device IDs or -1 (invalid device).
        """
        return self.ids

    def start_streaming(self, dev_id, freq, log_en):
        """
        Start streaming data from a FlexSEA device.

        Parameters:
        dev_id (int): The device ID

        freq (int): The desired frequency of communication

        log_en (bool): If true, all received data to is logged to a file.

        The name of the file is formed as follows:

        < FlexSEA model >_id< device ID >_< date and time >.csv

        for example:

        rigid_id3904_Tue_Nov_13_11_03_50_2018.csv

        The file is formatted as a CSV file. The first line of the file will be
        headers for all columns. Each line after that will contain the data read
        from the device.

        Raises:
        ValueError if the device ID is invalid
        RuntimeError if the stream failed
        """

        ret_code = self.c_lib.fxStartStreaming(
            dev_id, freq, 1 if log_en else 0)

        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError('fxStartStreaming: invalid device ID')
        if ret_code == FX_FAILURE:
            raise RuntimeError('fxStartStreaming: stream failed')

    def stop_streaming(self, dev_id):
        """
        Stop streaming data from a FlexSEA device.

        Parameters:
        dev_id (int): Is the device ID
        """
        ret_code = self.c_lib.fxStopStreaming(dev_id)
        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError('fxStopStreaming: invalid device ID')
        if ret_code == FX_FAILURE:
            raise RuntimeError('fxStopStreaming: stream failed')

    # TODO (CA): Check device is streaming in all read functions.
    def read_device(self, dev_id):
        """
        Read the most recent data from a streaming FlexSEA device stream.
        IMPORTANT! Must call fxStartStreaming before calling this.

        Parameters:
        dev_id (int): The device ID of the device to read from.

        Returns:
        deviceState: Contains the most recent data from the device

        Raises:
        ValueError if invalid device ID
        RuntimeError if no read data
        """
        # get the device type
        app_type = self.c_lib.fxGetAppType(dev_id)

        if app_type == en.FX_ACT_PACK:
            device_state = fx_devs.ActPackState()
            ret_code = self.c_lib.fxReadDevice(dev_id, c.byref(device_state))
        elif app_type == en.FX_NET_MASTER:
            device_state = fx_devs.NetMasterState()
            ret_code = self.c_lib.fxReadNetMasterDevice(
                dev_id, c.byref(device_state))
        elif app_type == en.FX_B_M_S:
            device_state = fx_devs.BMSState()
            ret_code = self.c_lib.fxReadBMSDevice(
                dev_id, c.byref(device_state))
        elif app_type == en.FX_EXO:
            device_state = fx_devs.ExoState()
            ret_code = self.c_lib.fxReadExoDevice(
                dev_id, c.byref(device_state))
        else:
            raise RuntimeError('Unsupported application type: ', app_type)

        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError(
                'fxReadDevice: invalid device ID: {}'.format(dev_id))
        if ret_code == en.FX_NOT_STREAMING:
            raise RuntimeError('fxReadDevice: no read data')
        if ret_code == en.FX_FAILURE:
            raise IOError('fxReadDevice: command failed')

        return device_state

    def read_exo_device(self, dev_id):
        """
        Read the most recent data from a streaming FlexSEA device stream.
        IMPORTANT! Must call fxStartStreaming before calling this.

        Parameters:
        dev_id (int): The device ID of the device to read from.

        Returns:
        (ExoState): Contains the most recent data from the device

        Raises:
        ValueError if invalid device ID
        RuntimeError if no read data
        """
        exo_state = fx_devs.ExoState()
        ret_code = self.c_lib.fxReadExoDevice(dev_id, c.byref(exo_state))

        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError(
                'fxReadDevice: invalid device ID: {}'.format(dev_id))
        if ret_code == en.FX_NOT_STREAMING:
            raise RuntimeError('fxReadDevice: no read data')

        return exo_state

    def read_device_all(self, dev_id, data_size):
        """
        Read all data from a streaming FlexSEA device stream.
        MUST call fxStartStreaming before calling this.

        Parameters:
        dev_id: Device ID of the device to read from.

        data_size: Size of readData.

        Raise:
        ValueError if invalid device ID

        Return:
        Actual number of entries read. You will probably need to use this number.
        """
        data = [fx_devs.ActPackState()] * data_size

        items_read = self.c_lib.fxReadDeviceAll(
            dev_id, c.byref(data), data_size)
        if items_read == -1:
            raise ValueError(
                'fxGetReadDataQueueSize: Invalid device ID: {}'.format(dev_id))
        return items_read

    def read_net_master_device_all(self, dev_id, data_size):
        """
        Read all data from a streaming FlexSEA NetMaster device stream.
        MUST call fxStartStreaming before calling this.

        Parameters:
        dev_id: Device ID of the device to read from.

        data_size: Size of readData.

        Raise:
        ValueError if invalid device ID

        Return:
        Actual number of entries read. You will probably need to use this number.
        """
        data = [fx_devs.NetMasterState()] * data_size

        items_read = self.c_lib.fxReadNetMasterDeviceAll(
            dev_id, c.byref(data), data_size)
        if items_read == -1:
            raise ValueError(
                'fxReadNetMasterDeviceAll: Invalid device ID {}'.format(
                    dev_id))
        return items_read

    def read_bms_device_all(self, dev_id, data_size):
        """
        Read all data from a streaming FlexSEA BMS device stream.
        MUST call fxStartStreaming before calling this.

        Parameters:
        dev_id: Device ID of the device to read from.

        data_size: Size of readData.

        Raise:
        ValueError if invalid device ID

        Return:
        Actual number of entries read. You will probably need to use this number.
        """
        data = [fx_devs.BMSState()] * data_size

        items_read = self.c_lib.fxReadNetMasterDeviceAll(
            dev_id, c.byref(data), data_size)
        if items_read == -1:
            raise ValueError('fxReadBMSDeviceAll: Invalid device ID')
        return items_read

    def set_read_data_queue_size(self, dev_id, data_size):
        """
        Set the maximum read data queue size of a device.

        Parameters:
        dev_id (int): The device ID: ID of the device to get the read data queue size from.

        data_size: Size to set the read data queue size to.

        Raises:
        FX_INVALID_DEVICE if invalid device.
        FX_INVALID_PARAM if size is invalid
        """
        ret_code = self.c_lib.fxSetReadDataQueueSize(dev_id, data_size)

        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError(
                'fxSetReadDataQueueSize: Invalid device ID: {}'.format(dev_id))
        if ret_code == en.FX_INVALID_PARAM:
            raise ValueError(
                'fxSetReadDataQueueSize: Invalid data_size: {}'.format(
                    data_size))
        if ret_code == en.FX_FAILURE:
            raise IOError('fxSetReadDataQueueSize: command failed')

    def get_read_data_queue_size(self, dev_id):
        """
        Get the maximum read data queue size of a device.

        Parameters:
        dev_id (int): The device ID: ID of the device to get the read data queue size from.

        Returns:
        Maximum read data queue size of a device.  -1 if invalid device ID.
        """

        ret_val = self.c_lib.fxGetReadDataQueueSize(dev_id)
        if ret_val == -1:
            raise ValueError(
                'fxGetReadDataQueueSize: Invalid device ID: {}'.format(dev_id))
        return ret_val

    def set_gains(self, dev_id, kp, ki, kd, k_val, b_val, ff):
        """
        Sets the gains used by PID controllers on the FlexSEA device.

        Parameters:
        dev_id (int): The device ID.

        kp (int): Proportional gain

        ki (int): Integral gain

        kd (int): Differential gain

        k_val (int): Stiffness (used in impedence control only)

        b_val (int): Damping (used in impedance control only)

        ff (int): Feed forward gain

        Raises:
        ValueError if the device ID is invalid
        """
        ret_code = self.c_lib.fxSetGains(dev_id, kp, ki, kd, k_val, b_val, ff)

        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError(
                'fxSetGains: invalid device ID: {}'.format(dev_id))
        if ret_code == en.FX_FAILURE:
            raise IOError('fxSetGains: command failed')

    def send_motor_command(self, dev_id, ctrl_mode, value):
        """
        Send a command to the device.

        Parameters:
        dev_id (int): The device ID.

        ctrl_mode (c_int): The control mode we will use to send this command.
        Possible values are: FxPosition, FxCurrent, FxVoltage, FxImpedence

        value (int): The value to use for the ctrl_mode.
        FxPosition - encoder value
        FxCurrent - current in mA
        FxVoltage - voltage in mV
        FxImpedence - current in mA

        Raises:
        ValueError if invalid device ID
        ValueError if invalid controlType
        """
        ret_code = self.c_lib.fxSendMotorCommand(
            dev_id, ctrl_mode, c.c_int(int(value)))

        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError(
                'fxSendMotorCommand: invalid device ID: {}'.format(dev_id))
        if ret_code == en.FX_FAILURE:
            raise IOError('fxSendMotorCommand failed.')
        if ret_code == en.FX_INVALID_PARAM:
            raise ValueError(
                'fxSendMotorCommand: Invalid control mode: {}'.format(
                    ctrl_mode))

    def get_app_type(self, dev_id):
        """
        Get the device application type

        Parameters:
        dev_id (int): The device ID.

        Returns:
        App Type (int)

        -1 if invalid
        0 if ActPack
        1 if Exo
        2 if NetMaster
        """
        return self.c_lib.fxGetAppType(dev_id)

    def find_poles(self, dev_id):
        """
        DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
        Find the motor poles

        Parameters:
        dev_id (int): The device ID.

        Returns:
        FX_INVALID_DEVICE if deviceId is invalid
        FxSuccess otherwise

        DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
        """
        ret_code = self.c_lib.fxFindPoles(dev_id)
        if ret_code == en.FX_INVALID_DEVICE:
            raise ValueError(
                'fxFindPoles: invalid device ID: {}'.format(dev_id))
        if ret_code == en.FX_FAILURE:
            raise ValueError('fxFindPoles: command failed')
