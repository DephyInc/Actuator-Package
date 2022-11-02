import ctypes as c
from time import sleep
from typing import List

from . import fx_enums as fxe
from . import fx_utils as fxu


# ============================================
#                   Device
# ============================================
class Device:
    """
    Contains and manages the information and state of Dephy's devices.
    """

    # -----
    # constructor
    # -----
    def __init__(self, port: str, baud_rate: int, libsVersion: str = "") -> None:
        self.port = port.encode("utf-8")
        self.baud_rate = baud_rate
        self.libsVersion = libsVersion if libsVersion else "7.2.0"

        self.dev_id = None
        self.app_type = None
        self.controller = None
        self.initial_pos = None
        self.streaming_freq = 0
        self.is_streaming = False
        self.is_open = False
        self.logging_enabled = True
        self.device_state = None
        self.hasHabs = True
        self.deviceType = None

        self.clib = fxu._load_clib(self.libsVersion)

    # -----
    # destructor
    # -----
    def __del__(self) -> None:
        self.close()

    # -----
    # open
    # -----
    def open(self, log_level: int=4, log_enabled: bool=True) -> None:
        """
        Establish a connection with a FlexSEA device.

        Parameters
        ----------
        log_level : int
            The logging level for this device. 0 is most verbose and
            6 is the least verbose. Values greater than 6 are floored to 6.

        log_enabled : bool
            If `True`, all received data is logged to a file.

            The file naming convention is:

            < FlexSEA model >_id< device ID >_< date and time >.csv

            for example:

            rigid_id3904_Tue_Nov_13_11_03_50_2018.csv

            The file is formatted as a CSV file. The first line of the
            file will be headers for all columns. Each line after that
            will contain the data read from the device.

        Raises
        ------
        IOError:
            If we fail to open the device.
        """
        if self.is_open:
            return

        self.logging_enabled = log_enabled
        self.dev_id = self.clib.fxOpen(self.port, self.baud_rate, log_level)
        if self.dev_id == -1:
            raise IOError("Failed to open device")
        self.is_open = True

        # NOTE: This sleep is so long because there's an issue that
        # occurs when trying to open multiple devices in rapid
        # succession that causes flexsea to crash
        sleep(1)
        self.app_type = self._get_app_type()
        if self.app_type == fxe.INVALID_APP:
            raise ValueError("Invalid app type.")

        try:
            self.deviceType = fxe.deviceTypes[self.app_type]
        except KeyError:
            raise KeyError("No device name for given app_type.")

        if self.app_type == fxe.ACT_PACK:
            self.hasHabs = False

        try:
            self.device_state = fxe.device_state_dicts[self.app_type]
        except KeyError:
            raise KeyError("Unrecognized app type.")

    # -----
    # close
    # -----
    def close(self) -> None:
        """
        Disconnect from a FlexSEA device.

        Raises
        ------
        ValueError:
            If the device ID is invalid.
        """
        if self.is_streaming:
            self.streaming_freq = 0
            self.stop_streaming()
        if self.is_open:
            if self.clib.fxClose(self.dev_id) == fxe.INVALID_DEVICE:
                raise ValueError("fxClose: invalid device ID")
            self.is_open = False

    # -----
    # start_streaming
    # -----
    def start_streaming(self, freq: int) -> None:
        """
        Start streaming data from a FlexSEA device.

        Parameters
        ----------
        freq : int
            The desired frequency of communication.

        Raises
        ------
        ValueError:
            If the device ID is invalid.

        RuntimeError:
            If the stream failed.
        """
        if self.is_streaming:
            print("Already streaming. Cannot start new stream.")
            return

        if not self.is_open:
            print("Device connection not established. Call `open` first.")
            return

        self.streaming_freq = freq

        _log = 1 if self.logging_enabled else 0
        ret_code = self.clib.fxStartStreaming(self.dev_id, freq, _log)

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError("fxStartStreaming: invalid device ID")
        elif ret_code == fxe.FAILURE:
            raise RuntimeError("fxStartStreaming: stream failed")

        self.is_streaming = True

        # NOTE: This sleep is so long because there's an issue that
        # occurs when trying to open multiple devices in rapid
        # succession that causes flexsea to crash
        sleep(1)
        self.initial_pos = self.pos

    # -----
    # stop_streaming
    # -----
    def stop_streaming(self) -> None:
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
        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError("fxStopStreaming: invalid device ID")
        if ret_code == fxe.FAILURE:
            raise RuntimeError("fxStopStreaming: stream failed")
        self.is_streaming = False

    # -----
    # read
    # -----
    def read(self) -> c.Structure:
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
        deviceState : c.Structure
                Contains the most recent data from the device.
        """
        if not self.is_streaming:
            raise RuntimeError("Must call `open()` and `start_streaming()` before trying to read data.")

        if self.app_type == fxe.ACT_PACK:
            ret_code = self.clib.fxReadDevice(self.dev_id, c.byref(self.device_state))

        elif self.app_type == fxe.NET_MASTER:
            ret_code = self.clib.fxReadNetMasterDevice(
                self.dev_id, c.byref(self.device_state)
            )

        elif self.app_type == fxe.BMS:
            ret_code = self.clib.fxReadBMSDevice(self.dev_id, c.byref(self.device_state))

        elif self.app_type == fxe.EB5X:
            ret_code = self.clib.fxReadExoDevice(self.dev_id, c.byref(self.device_state))

        elif self.app_type == fxe.MD:
            ret_code = self.clib.fxReadMdDevice(self.dev_id, c.byref(self.device_state))

        # Unknown
        else:
            raise RuntimeError(f"Unsupported application type: {self.app_type}")

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"fxReadDevice: invalid device ID: {self.dev_id}")
        elif ret_code == fxe.NOT_STREAMING:
            raise RuntimeError("fxReadDevice: no read data")
        elif ret_code == fxe.FAILURE:
            raise IOError("fxReadDevice: command failed")

        return self.device_state

    # -----
    # set_gains
    # -----
    def set_gains(self, kp: int, ki: int, kd: int, k: int, b: int, ff: int) -> None:
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

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FX_FAILURE:
            raise IOError("Command failed")

    # -----
    # send_motor_command
    # -----
    def send_motor_command(self, ctrl_mode: int, value: int) -> None:
        """
        Send a command to the device.

        Parameters
        ----------
        ctrl_mode : int
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
        ret_code = self.clib.fxSendMotorCommand(self.dev_id, ctrl_mode, value)

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FAILURE:
            raise IOError("Command failed.")
        if ret_code == fxe.INVALID_PARAM:
            raise ValueError(f"Invalid control mode: {ctrl_mode}")


    # -----
    # find_poles
    # -----
    def find_poles(self) -> None:
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
        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        if ret_code == fxe.FAILURE:
            raise ValueError("Command failed")

    # -----
    # activate_bootloader
    # -----
    def activate_bootloader(self, target: str) -> None:
        """
        Activate target bootloader.

        Parameters
        ----------
        target : str
            Bootloader target.

        Raises
        ------
        ValueError:
            Invalid device id.

        IOError:
            Command failed.
        """
        try:
            target = fxe.bootloader_targets[target]
        except KeyError:
            raise KeyError(f"Unknown target: {target}")

        ret_code = self.clib.fxActivateBootloader(self.dev_id, target)

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"Invalid device ID {self.dev_id}")
        if ret_code == fxe.FAILURE:
            raise IOError("Command failed")

    # -----
    # is_bootloader_activated
    # -----
    def is_bootloader_activated(self) -> int:
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
        int
            Gives the value of the status. See fxEnums.py.
        """
        ret_code = self.clib.fxIsBootloaderActivated(self.dev_id)

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"Invalid device ID {self.dev_id}")
        if ret_code == fxe.FAILURE:
            raise IOError("Command failed")

        return ret_code

    # -----
    # get_firmware
    # -----
    def get_firmware(self) -> List:
        """
        Gets fimwareversion of device's MCUs.

        Raises
        ------
        ValueError:
            Invalid device id.

        IOError:
            Command failed.

        Returns
        -------
        List 
            A list with the semantic version strings of manage,
            execute, and regulate's firmware.
        """
        ret_code = self.clib.fxRequestFirmwareVersion(self.dev_id)

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError("Invalid device ID")
        if ret_code == fxe.FX_FAILURE.value:
            raise IOError("Command failed")

        sleep(5)

        fw = self.clib.fxGetLastReceivedFirmwareVersion(self.dev_id)

        mn_fw = fxu.decode(fw.Mn)
        ex_fw = fxu.decode(fw.Ex)
        re_fw = fxu.decode(fw.Re)

        return [mn_fw, ex_fw, re_fw]

    # -----
    # pos
    # -----
    @property
    def pos(self) -> int:
        """
        Returns the current position of the device.

        Returns
        -------
        int
            The current position of the motor in ticks.
        """
        return self.read().mot_ang

    # -----
    # rigidVersion
    # -----
    @property
    def rigidVersion(self) -> str:
        """
        Returns the device's rigid (board) version, e.g., 4.1.
        """
        return self.read().rigid

    # -----
    # print
    # -----
    def print(self, data=None) -> None:
        """
        Reads the data from the device and then prints it to the screen.
        """
        if not data:
            data = self.read()
        for field in self.device_state._fields_:
            print(f"{field[0]}: {getattr(self.device_state, field[0])}")

    # -----
    # _get_app_type
    # -----
    def _get_app_type(self) -> int:
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
        return self.clib.fxGetAppType(self.dev_id)

    # -----
    # read_data_queue_size
    # -----
    @property
    def read_data_queue_size(self) -> int:
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
    def read_data_queue_size(self, data_size) -> None:
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

        if ret_code == fxe.INVALID_DEVICE:
            raise ValueError(f"Invalid device ID: {self.dev_id}")
        elif ret_code == fxe.INVALID_PARAM:
            raise ValueError(f"Invalid data_size: {data_size}")
        elif ret_code == fxe.FAILURE:
            raise IOError("Command failed")
