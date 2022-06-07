"""
Dephy's FlexSEA Python API
"""
import ctypes as c
from time import sleep

from .dev_spec import AllDevices as fxd
from . import fx_enums as fxe
from . import fx_utils as fxu


# ============================================
#                   Device
# ============================================
# pylint: disable=R0902
class Device:
    """
    Contains and manages the information and state of Dephy's devices.
    """

    # -----
    # constructor
    # -----
    def __init__(self, port, baud_rate, **kwargs):
        self.port = port
        self.baud_rate = baud_rate
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.clib = fxu._load_clib()

        self.dev_id = None
        self.app_type = None
        self.controller_type = None
        self.controller = None
        self.initial_pos = None
        self.streaming_freq = 0
        self.is_streaming = False
        self.is_open = False

    # -----
    # destructor
    # -----
    def __del__(self):
        self.close()

    # -----
    # open
    # -----
    def open(self, freq, log_level=4, log_enabled=True):
        """
        Establish a connection with a FlexSEA device.

        Parameters
        ----------
        freq : int
                The desired frequency of communication.

        log_level : int
                The logging level for this device. 0 is most verbose and
                6 is the least verbose. Values greater than 6 are floored to 6.

        log_enabled : bool
                If `True`, all received data is logged to a file.

        Raises
        ------
        IOError:
                If we fail to open the device.

        RuntimeError:
           If the stream failed.
        """
        # Don't initialize more than once
        if self.is_open:
            return
        self.streaming_freq = freq
        self.dev_id = self.clib.fxOpen(
            self.port.encode("utf-8"), self.baud_rate, log_level
        )
        if self.dev_id == -1:
            raise IOError("Failed to open device")
        self.is_open = True
        self._start_streaming(self.streaming_freq, log_enabled)

        # NOTE: This sleep is so long because there's an issue that
        # occurs when trying to open multiple devices in rapid
        # succession that causes flexsea to crash
        sleep(1)
        self.app_type = self._get_app_type()
        self.initial_pos = self.get_pos()

    # -----
    # close
    # -----
    def close(self):
        """
        Disconnect from a FlexSEA device.

        Raises
        ------
        ValueError:
                If the device ID is invalid.
        """
        if self.is_streaming:
            self.streaming_freq = 0
            self._stop_streaming()
        if self.is_open:
            if self.clib.fxClose(self.dev_id) == fxe.FX_INVALID_DEVICE.value:
                raise ValueError("fxClose: invalid device ID")
            self.is_open = False

    # -----
    # _start_streaming
    # -----
    def _start_streaming(self, freq, log_en):
        """
        Start streaming data from a FlexSEA device.

        Parameters
        ----------
        freq : int
                The desired frequency of communication.

        log_en : bool
                If `True`, all received data to is logged to a file.
                The name of the file is formed as follows:

                < FlexSEA model >_id< device ID >_< date and time >.csv

                for example:

                rigid_id3904_Tue_Nov_13_11_03_50_2018.csv

                The file is formatted as a CSV file. The first line of the file will be
                headers for all columns. Each line after that will contain the data read
                from the device.

        Raises
        ------
        ValueError:
                If the device ID is invalid.

        RuntimeError:
                If the stream failed.
        """
        ret_code = self.clib.fxStartStreaming(self.dev_id, freq, 1 if log_en else 0)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError("fxStartStreaming: invalid device ID")
        if ret_code == fxe.FX_FAILURE.value:
            raise RuntimeError("fxStartStreaming: stream failed")
        self.is_streaming = True

    # -----
    # _stop_streaming
    # -----
    def _stop_streaming(self):
        """
        Stop streaming data from a FlexSEA device.

        Raises
        ------
        ValueError:
                If the device ID is invalid.

        RuntimeError:
                If the stream failed.
        """
        ret_code = self.clib.fxStopStreaming(self.dev_id)
        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError("fxStopStreaming: invalid device ID")
        if ret_code == fxe.FX_FAILURE.value:
            raise RuntimeError("fxStopStreaming: stream failed")
        self.is_streaming = False

    # -----
    # read
    # -----
    def read(self):
        """
        Read the most recent data from a streaming FlexSEA device stream.

        Raises
        ------
        ValueError:
                If invalid device ID.

        RuntimeError:
                If no read data.

        IOError:
                Command failed.

        Returns
        -------
        deviceState : List
                Contains the most recent data from the device.
        """
        if not self.is_streaming:
            raise RuntimeError("Must call `open()` before trying to read data.")

        # Actpack
        if self.app_type.value == fxe.FX_ACT_PACK.value:
            device_state = fxd.ActPackState()
            ret_code = self.clib.fxReadDevice(self.dev_id, c.byref(device_state))

        # Net master
        elif self.app_type.value == fxe.FX_NET_MASTER.value:
            device_state = fxd.NetMasterState()
            ret_code = self.clib.fxReadNetMasterDevice(
                self.dev_id, c.byref(device_state)
            )

        # BMS
        elif self.app_type.value == fxe.FX_BMS.value:
            device_state = fxd.BMSState()
            ret_code = self.clib.fxReadBMSDevice(self.dev_id, c.byref(device_state))

        # EB5X
        elif self.app_type.value == fxe.FX_EB5X.value:
            device_state = fxd.EB5xState()
            ret_code = self.clib.fxReadExoDevice(self.dev_id, c.byref(device_state))

        # MD
        elif self.app_type.value == fxe.FX_MD.value:
            device_state = fxd.MD10State()
            ret_code = self.clib.fxReadMdDevice(self.dev_id, c.byref(device_state))

        # Unknown
        else:
            raise RuntimeError(f"Unsupported application type: {self.app_type}")

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"fxReadDevice: invalid device ID: {self.dev_id}")
        if ret_code == fxe.FX_NOT_STREAMING.value:
            raise RuntimeError("fxReadDevice: no read data")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("fxReadDevice: command failed")

        return device_state

    # -----
    # read_all
    # -----
    def read_all(self, data_size):
        """
        Read all data from a streaming FlexSEA device stream.

        Parameters
        ----------
        data_size : int
                Size of readData.

        Raises
        ------
        RuntimeError:
                Unsupported app type.

        ValueError:
                If invalid device ID.

        Returns
        -------
        int:
                Actual number of entries read. You will probably need to use this number.
        """
        if not self.app_type:
            raise RuntimeError("Must call `open()` before trying to read data.")

        # Actpack
        if self.app_type.value == fxe.FX_ACT_PACK.value:
            data = [fxd.ActPackState()] * data_size
            n_read = self.clib.fxReadDeviceAll(self.dev_id, c.byref(data), data_size)

        # Net master
        elif self.app_type.value == fxe.FX_NET_MASTER.value:
            data = [fxd.NetMasterState()] * data_size
            n_read = self.clib.fxReadNetMasterDeviceAll(
                self.dev_id, c.byref(data), data_size
            )

        # BMS
        elif self.app_type.value == fxe.FX_BMS.value:
            data = [fxd.BMSState()] * data_size
            n_read = self.clib.fxReadBMSDeviceAll(self.dev_id, c.byref(data), data_size)

        # Unknown
        else:
            raise RuntimeError(f"Unsupported application type: {self.app_type}")

        if n_read == -1:
            raise ValueError(f"Invalid device ID: {self.dev_id}")

        return n_read

    # -----
    # read_data_queue_size
    # -----
    @property
    def read_data_queue_size(self):
        """
        Get the maximum read data queue size of a device.

        Raises
        ------
        ValueError:
                If invalid device id.

        Returns
        -------
        int:
                Maximum read data queue size of a device.
        """

        max_size = self.clib.fxGetReadDataQueueSize(self.dev_id)
        if max_size == -1:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        return max_size

    @read_data_queue_size.setter
    def read_data_queue_size(self, data_size):
        """
        Sets the maximum read data queue size of a device.

        Parameters
        ----------
        data_size : int
                Size to set the read data queue size to.

        Raises
        ------
        ValueError:
                If either device id or data size are invalid.

        IOError:
                If the command failed.
        """
        ret_code = self.clib.fxSetReadDataQueueSize(self.dev_id, data_size)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FX_INVALID_PARAM.value:
            raise ValueError(f"Invalid data_size: {data_size}")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed")

    # -----
    # set_gains
    # -----
    # pylint: disable=C0103,R0913
    def set_gains(self, kp, ki, kd, k, b, ff):
        """
        Sets the gains used by PID controllers on the FlexSEA device.

        Parameters
        ----------
        kp : int
                Proportional gain.

        ki : int
                Integral gain.

        kd : int
                Differential gain.

        k : int
                Stiffness (used in impedence control only).

        b : int
                Damping (used in impedance control only).

        ff : int
                Feed forward gain.

        Raises
        ------
        ValueError:
                If the device ID is invalid.

        IOError:
                Command failed.
        """
        ret_code = self.clib.fxSetGains(self.dev_id, kp, ki, kd, k, b, ff)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed")

    # -----
    # send_motor_command
    # -----
    def send_motor_command(self, ctrl_mode, value):
        """
        Send a command to the device.

        Parameters
        ----------
        ctrl_mode : c_int
                The control mode we will use to send this command.
                Possible values are: FxPosition, FxCurrent, FxVoltage, FxImpedence

        value : int
                The value to use for the ctrl_mode.
                FxPosition - encoder value
                FxCurrent - current in mA
                FxVoltage - voltage in mV
                FxImpedence - current in mA

        Raises
        ------
        ValueError:
                If invalid device ID or invalid control type.

        IOError:
                Command failed.
        """
        ret_code = self.clib.fxSendMotorCommand(
            self.dev_id, ctrl_mode, c.c_int(int(value))
        )

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed.")
        if ret_code == fxe.FX_INVALID_PARAM.value:
            raise ValueError(f"Invalid control mode: {ctrl_mode}")

    # -----
    # _get_app_type
    # -----
    def _get_app_type(self):
        """
        Get the device application type.

        Returns
        -------
        int:
                -1 : invalid
                0 : ActPack
                1 : Exo
                2 : MD
                3 : NetMaster
        """
        return c.c_int(self.clib.fxGetAppType(self.dev_id))

    # -----
    # find_poles
    # -----
    def find_poles(self):
        """
        DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
        Finds the motor poles.

        Raises
        ------
        ValueError:
                Invalid device id or if the command failed.
        """
        user_input = input(
            "WARNING: You should not use this function unless you know what "
            "you are doing!\nProceed?[y/n] "
        )
        if user_input != "y":
            print("Aborting pole finding.")
            return
        ret_code = self.clib.fxFindPoles(self.dev_id)
        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FX_FAILURE.value:
            raise ValueError("Command failed")

    # -----
    # activate_bootloader
    # -----
    def activate_bootloader(self, target):
        """
        Activate target bootloader.

        Parameters
        ----------
        target : int
                Bootloader target.

        Raises
        ------
        ValueError:
                Invalid device id.

        IOError:
                Command failed.
        """
        ret_code = self.clib.fxActivateBootloader(self.dev_id, target)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"Invalid device ID {self.dev_id}")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed")

    # -----
    # is_bootloader_activated
    # -----
    def is_bootloader_activated(self):
        """
        Get status of bootloader.

        Raises
        ------
        ValueError:
                Invalid device id.

        IOError:
                Command failed.

        Returns
        -------
        c.c_int
                A `c_int` giving the `enum` value of the status. See fxEnums.py.
        """
        ret_code = self.clib.fxIsBootloaderActivated(self.dev_id)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError(f"Invalid device ID {self.dev_id}")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed")

        return ret_code

    # -----
    # request_firmware_version
    # -----
    def request_firmware_version(self):
        """
        Request version of on board MCUs.

        Raises
        ------
        ValueError:
                Invalid device id.

        IOError:
                Command failed.

        Returns
        -------
        c.c_int
                A `c_int` giving the `enum` value of the status. See fxEnums.py.
        """
        ret_code = self.clib.fxRequestFirmwareVersion(self.dev_id)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError("Invalid device ID")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed")

        return ret_code

    # -----
    # get_last_received_firmware_version
    # -----
    def get_last_received_firmware_version(self):
        """
        Request version of on board MCUs.

        Returns
        -------
        c.c_int
                A `c_int` giving the `enum` value of the status. See fxEnums.py.
        """
        return self.clib.fxGetLastReceivedFirmwareVersion(self.dev_id)

    # -----
    # set_controller
    # -----
    def set_controller(self, controller_type):
        """
        Sets the device's controller.
        """
        self.controller_type = controller_type
        if self.controller_type == fxe.HSS_CURRENT:
            self.controller = fxe.FX_CURRENT
        elif self.controller_type == fxe.HSS_POSITION:
            self.controller = fxe.FX_POSITION

    # -----
    # get_pos
    # -----
    def get_pos(self):
        """
        Returns the current position of the device.
        """
        return self.read().mot_ang

    # -----
    # print
    # -----
    def print(self, data=None):
        """
        Reads the data from the device and then prints it to the screen.
        """
        if not data:
            data = self.read()
        fxu.print_device(data, self.app_type)
