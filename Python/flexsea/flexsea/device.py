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
    def __init__(self, port, baud_rate):
        self.port = port.encode("utf-8")
        self.baud_rate = baud_rate

        self.clib = fxu._load_clib()

        self.dev_id = None
        self.streaming_freq = 0
        self.logging_enabled = True

    # -----
    # destructor
    # -----
    def __del__(self):
        self.close()

    # -----
    # is_open
    # -----
    @property
    def is_open(self):
        return self.clib.fxIsOpen(self.dev_id)

    # -----
    # is_streaming
    # -----
    @property
    def is_streaming(self):
        return self.clib.fxIsStreaming(self.dev_id)

    # -----
    # libs_version
    # -----
    @property
    def libs_version(self):
        major = c.c_uint16(-1)
        minor = c.c_uint16(-1)
        patch = c.c_uint16(-1)

        retCode = self.clib.fxGetLibsVersion(c.byref(major), c.byref(minor), c.byref(patch))

        if retCode != fxe.FX_SUCCESS.value:
            print("Error, could not determine clibs version.")
            raise OSError

        print(f"{major.value}.{minor.value}.{patch.value}")

    # -----
    # open
    # -----
    def open(self, log_level=4, log_enabled=True):
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

                The file is formatted as a CSV file. The first line of the file will be
                headers for all columns. Each line after that will contain the data read
                from the device.

        Raises
        ------
        IOError:
                If we fail to open the device.
        """
        # Don't initialize more than once
        if self.is_open:
            return
        self.logging_enabled = log_enabled
        self.dev_id = self.clib.fxOpen(self.port, self.baud_rate, log_level)
        if self.dev_id == -1:
            raise IOError("Failed to open device")

        # NOTE: This sleep is so long because there's an issue that
        # occurs when trying to open multiple devices in rapid
        # succession that causes flexsea to crash
        sleep(1)
        self.app_type = self._get_app_type()

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

    # -----
    # start_streaming
    # -----
    def start_streaming(self, freq):
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

        if ret_code == fxe.FX_INVALID_DEVICE.value:
            raise ValueError("fxStartStreaming: invalid device ID")
        if ret_code == fxe.FX_FAILURE.value:
            raise RuntimeError("fxStartStreaming: stream failed")


        # NOTE: This sleep is so long because there's an issue that
        # occurs when trying to open multiple devices in rapid
        # succession that causes flexsea to crash
        sleep(1)
        self.get_device_type_name()
        self.get_device_side()
        self.get_data_labels()

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

        maxDataElements = self.clib.fxGetMaxDataElements()
        nFields = c.c_int()
        deviceData = (c.POINTER(c.c_uint32) * maxDataElements)()

        retCode = self.clib.fxReadDevice(self.dev_id, deviceData, c.by_ref(nFields))

        try:
            assert nFields.value == len(self.dataFields)
        except AssertionError:
            print("Error: Incorrect number of fields read.")
            raise AssertionError

        if retCode != fxe.FX_SUCCESS.value:
            print("Error: Could not read from device.")
            raise ValueError

        data = []

        for i in range(nFields.value):
            data.append(deviceData[i].value)

        deviceState = {key : value for (key, value) in zip(self.dataFields, data)}

        return deviceState

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

    # -----
    # uvlo
    # -----
    @property
    def uvlo(self):
        retCode = self.clib.fxRequestUVLO(self.dev_id)

        if retCode != fxe.FX_SUCCESS.value:
            print("Error, could not request firmware version.")
            raise IOError

        sleep(5)

        uvlo = self.clib.fxGetLastReceivedUVLO(self.dev_id)

        if uvlo == -1:
            print("Error, coult not get requested UVLO.")
            raise IOError

        return uvlo

    @uvlo.setter
    def uvlo(self, value):
        # value must be in millivolts
        retCode = self.clib.fxSetUVLO(self.dev_id, c.c_uint(value))

        if retCode != fxe.FX_SUCCESS.value:
            print("Error, could not set UVLO.")
            raise IOError

    # -----
    # imu_calibration
    # -----
    def imu_calibration(self):
        retCode = self.clib.fxSetImuCalibration(self.dev_id)

        if retCode != fxe.FX_SUCCESS.value:
            print("Error, could not calibrate imu.")
            raise IOError

    # -----
    # get_data_labels
    # -----
    def get_data_labels(self):
        maxFields = self.clib.fxGetMaxDataElements()
        maxFieldLength = self.clib.fxGetMaxDataLabelLength()
        nLabels = c.c_int()

        # Create types for holding labels
        labelType = c.c_char * maxFieldLength
        labelsType = c.POINTER(c.c_char) * maxFields

        # Allocate memory for the labels container
        labels = labelsType()
        for i in range(maxFields):
            labels[i] = labelType()

        retCode = self.clib.fxGetDataLabelsWrapper(self.dev_id, labels, c.by_ref(nLabels))

        if retCode != fxe.FX_SUCCESS.value:
            print("Error: Could not get device field labels.")
            raise ValueError

        # Convert the labels from chars to python strings
        self.dataFields = [""] * nLabels.value
        for i in range(nLabels.value):
            for j in range(maxFieldLength):
                self.dataFields[i] += labels[i][j].decode("utf9")
            self.dataFields[i].strip("\x00")

        for field in self.dataFields:
            setattr(self, field, None)

    # -----
    # get_device_type_name
    # -----
    def get_device_type_name(self):
        maxDeviceNameLength = self.clib.fxGetMaxDeviceNameLength()

        deviceName = (c.c_char * maxDeviceNameLength)()

        retCode = self.clib.fxGetDeviceTypeNameWrapper(self.dev_id, deviceName)

        if retCode != fxe.FX_SUCCESS.value:
            print("Error: Could not get device name.")
            raise ValueError

        self.deviceName = deviceName.value.decode("utf8")

    # -----
    # get_device_side
    # -----
    def get_device_side(self):
        maxDeviceNameLength = self.clib.fGetMaxDeviceNameLength()

        deviceSideName = (c.c_char * maxDeviceNameLength)()

        retCode = self.clib.fxGetDeviceSideNameWrapper(self.dev_id, deviceSideName)

        if retCode != fxe.FX_SUCCESS.value:
            print("Error: Could not get device side name.")
            raise ValueError

        self.side = deviceSideName.value.decode("utf8")
