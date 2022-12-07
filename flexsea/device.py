import ctypes as c
from time import sleep
from typing import List
from typing import Self

from . import config as cfg
from . import enums as fxe
from . import utilities as fxu
from .specs.api_spec import apiSpec


# ============================================
#                   Device
# ============================================
class Device:
    """
    Representation of one of Dephy's devices.
    """

    # -----
    # constructor
    # -----
    def __init__(
        self,
        port: str,
        baudRate: int,
        cLibVersion: str = cfg.LTS,
        logLevel: int = 4,
        loggingEnabled: bool = True,
    ) -> None:
        self.port = port
        self.baudRate = baudRate
        self.cLibVersion = cLibVersion
        self.logLevel = logLevel
        self.loggingEnabled = loggingEnabled

        self._state: dict = {}
        self.deviceID: int = fxe.INVALID_DEVICE
        self.deviceName: str = ""
        self.hasHabs: bool = False
        self.isOpen: bool = False
        self.isStreaming: bool = False
        self.loggingEnabled: bool = False
        self.logLevel: int = 0
        self.streamingFrequency: int = 0
        self.heartbeatPeriod : int = 0
        self.useSafety : bool = False

        self._clib = fxu.load_clib(self.cLibVersion)

    # -----
    # destructor
    # -----
    def __del__(self) -> None:
        self.close()

    # -----
    # __enter__
    # -----
    def __enter__(self, stream: bool = False, frequency: int = 0) -> Self:
        self.open()

        if stream and frequency > 0:
            self.start_streaming(frequency)

        return self

    # -----
    # __exit__
    # -----
    def __exit__(
        self,
        excType,
        excVal,
        excTb,
    ) -> None:
        if excType is not None:
            print(f"Exception: {excVal}")
            print(f"{excTb}")

    # -----
    # open
    # -----
    def open(self) -> None:
        """
        Establish a connection with a device. If `self.loggingEnabled`
        is `True`, then the file naming convention is:

            <model>_id<device ID>_<date and time>.csv

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
        if self.isOpen:
            return

        port = self.port.encode("utf-8")

        self.deviceID = self._clib.open(port, self.baudRate, self.logLevel)

        if self.deviceID in (fxe.INVALID_DEVICE, -1):
            raise IOError("Failed to open device.")

        self.isOpen = True

        # NOTE: This sleep is so long because there's an issue that
        # occurs when trying to open multiple devices in rapid
        # succession that causes flexsea to crash
        sleep(1)
        deviceTypeValue = self._clib.get_device_type_value(self.deviceID)

        self.deviceName = fxe.deviceNames[deviceTypeValue]

        if self.deviceName in fxe.hasHabs:
            self.hasHabs = True

        self._state = fxe.deviceStateDicts[self.deviceName]

        # The read function is set here and not with other c functions
        # because we need the device name, which we can't get without
        # calling open, for which we need the c library loaded
        rf = apiSpec[self.cLibVersion]["read_functions"][self.deviceName]

        for key in ("", "all_"):
            func = getattr(self._clib, rf[key + "name"])
            func.argtypes = rf[key + "argTypes"]
            func.restype = rf[key + "returnType"]
            setattr(self._clib, key + "read", func)

    # -----
    # close
    # -----
    def close(self) -> None:
        """
        Disconnect from a device.

        Raises
        ------
        ValueError:
            If the device ID is invalid.
        """
        if self.isStreaming:
            self.stop_streaming()

        if self.isOpen:
            self._clib.close(self.deviceID)
            self.isOpen = False

    # -----
    # start_streaming
    # -----
    def start_streaming(self, frequency: int, heartbeatPeriod: int=50, useSafety: bool=False) -> None:
        """
        Start streaming data from a device.

        Parameters
        ----------
        frequency : int
            The desired frequency of communication.

        heartbeatPeriod : int
            When streaming, the computer periodically sends a message to
            the device to let it know that the connection between them
            is still alive. These are called heartbeat messages. This
            variable specifies the amount of time (in milliseconds)
            between successive heartbeat messages. This is related to
            how long the device will wait without receiving a heartbeat
            before shutting itself off (five times `heartbeatPeriod`).

        useSafety : bool
            If True, the device will shut itself off if it doesn't
            receive a heartbeat message from the computer within the
            allotted time (five times `heartbeatPeriod`). If False,
            the device will not shut itself off, just stop streaming,
            if a heartbeat isn't received.

        Raises
        ------
        RuntimeError:
            If the stream failed.
        """
        if self.isStreaming:
            print("Already streaming.")
            return

        if not self.isOpen:
            print("Device connection not established. Call `open` first.")
            return

        self.streamingFrequency = frequency
        self.heartbeatPeriod = heartbeatPeriod
        self.useSafety = useSafety

        _log = 1 if self.loggingEnabled else 0

        if self.useSafety:
            if not hasattr(self._clib, "start_streaming_with_safety"):
                msg = "Error: the disconnect shutoff safety requires cLibVersion >= 9.1"
                raise ValueError(msg) 

            hbp = self.heartbeatPeriod
            try:
                assert hbp >= 50 and hbp < self.streamingFrequency
            except AssertionError as err:
                msg = "Heartbeat period must be >= 50 and < frequency."
                raise ValueError(msg) from err

            retCode = self._clib.start_streaming_with_safety(self.deviceID, frequency, _log, self.heartbeatPeriod)

        else:
            retCode = self._clib.start_streaming(self.deviceID, frequency, _log)

        if retCode == fxe.FAILURE:
            raise RuntimeError("Error: could not start stream.")

        self.isStreaming = True

    # -----
    # stop_streaming
    # -----
    def stop_streaming(self) -> None:
        """
        Stop streaming data from a device.

        Raises
        ------
        RuntimeError:
            If the stream failed.
        """
        self.streamingFrequency = 0

        if self._clib.stop_streaming(self.deviceID) == fxe.FAILURE:
            raise RuntimeError("Error: failed to stop streaming.")

        self.isStreaming = False

    # -----
    # read
    # -----
    def read(self, allData: bool = False) -> c.Structure:
        """
        Reads data from a streaming device.

        Parameters
        ----------
        allData : bool
            If `True`, read the entire queue. If `False`, read only the
            most recent data.

        Raises
        ------
        RuntimeError:
            If not streaming.

        IOError:
            Command failed.

        Returns
        -------
        deviceState : c.Structure
                Contains the most recent data from the device.
        """
        if not self.isStreaming:
            raise RuntimeError(
                "Must call `open()` and `start_streaming()` before trying to read data."
            )

        if allData:
            returnCode = self._clib.all_read(
                self.deviceID, c.byref(self._state), self.queue_size
            )

        else:
            returnCode = self._clib.read(self.deviceID, c.byref(self._state))

        if returnCode == fxe.FAILURE:
            raise IOError("Error: read command failed.")

        return self._state

    # -----
    # set_gains
    # -----
    def set_gains(self, kp: int, ki: int, kd: int, k: int, b: int, ff: int) -> None:
        """
        Sets the gains used by PID controllers on the device.

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
        IOError:
            Command failed.
        """
        if self._clib.set_gains(self.deviceID, kp, ki, kd, k, b, ff) == fxe.FAILURE:
            raise IOError("Command failed")

    # -----
    # send_motor_command
    # -----
    def send_motor_command(self, ctrlMode: str, value: int) -> None:
        """
        Send a command to the device.

        Parameters
        ----------
        ctrlMode : str
            The control mode we will use to send this command.
            Possible values are:
                * position
                * current
                * voltage
                * impedence
                * none
                * custom
                * meas_res
                * stalk

        value : int
            The value to use for the control mode. Has different units
            depending on the control mode:

                position : encoder value
                current : current in mA
                voltage : voltage in mV
                impedence : current in mA
                none : N/A. Stops the motor
                custom : whatever you've defined it to be

        Raises
        ------
        ValueError:
            If invalid device ID or invalid control type.

        IOError:
            Command failed.
        """
        controller = c.c_int(fxe.controllers[ctrlMode])
        returnCode = fxe.FAILURE
        returnCode = self._clib.send_motor_command(self.deviceID, controller, c.c_int(int(value)))

        if returnCode == fxe.FAILURE:
            raise IOError("Command failed.")
        if returnCode == fxe.INVALID_PARAM:
            raise ValueError(f"Invalid control mode: {ctrlMode}")

    # -----
    # find_poles
    # -----
    def find_poles(self) -> None:
        """
        DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING!

     the motor poles.

        Raises
        ------
        ValueError:
            If the command failed.
        """
        userInput = input(
            "WARNING: You should not use this function unless you know what "
            "you are doing!\nProceed?[y/n] "
        )

        if userInput != "y":
            print("Aborting pole finding.")
            return

        if self._clib.find_poles(self.deviceID) == fxe.FAILURE:
            raise ValueError("Command failed")

    # -----
    # activate_bootloader
    # -----
    def activate_bootloader(self, target: str) -> None:
        """
        Activates target bootloader.

        Parameters
        ----------
        target : str
            Bootloader target.

        Raises
        ------
        IOError:
            Command failed.
        """
        target = fxe.bootloaderTargets[target]

        returnCode = self._clib.activate_bootloader(self.deviceID, target)

        if returnCode == fxe.FAILURE or returnCode == fxe.INVALID_DEVICE:
            raise IOError

    # -----
    # bootloader_activated
    # -----
    @property
    def bootloader_activated(self) -> bool:
        """
        Get status of bootloader.

        Raises
        ------
        IOError:
            Command failed.

        Returns
        -------
        int
            Gives the value of the status. See fxEnums.py.
        """
        returnCode = self._clib.is_bootloader_activated(self.deviceID)

        if returnCode == fxe.FAILURE or returnCode == fxe.INVALID_DEVICE:
            return False

        return True

    # -----
    # rigidVersion
    # -----
    @property
    def rigidVersion(self) -> str:
        pass

    # -----
    # firmware
    # -----
    @property
    def firmware(self) -> List[str]:
        """
        Gets the fimware versions of device's MCUs.

        Raises
        ------
        IOError:
            Command failed.

        Returns
        -------
        List
            A list with the semantic version strings of manage,
            execute, and regulate's firmware.
        """
        returnCode = self._clib.request_firmware_version(self.deviceID)

        if returnCode == fxe.FAILURE:
            raise IOError("Command failed")

        sleep(5)

        fw = self._clib.get_last_received_firmware_version(self.deviceID)

        fwList = [
            fxu.decode(fw.mn),
            fxu.decode(fw.ex),
            fxu.decode(fw.re),
        ]

        if self.hasHabs:
            fwList.append(fxu.decode(fw.habs))

        return fwList

    # -----
    # print
    # -----
    def print(self, data=None) -> None:
        """
        Reads the data from the device and then prints it to the screen.
        """
        if not data:
            data = self.read()
        for field in self._state._fields_:
            print(f"{field[0]}: {getattr(self._state, field[0])}")

    # -----
    # queue_size
    # -----
    @property
    def queue_size(self) -> int:
        """
        Get the maximum read data queue size of a device.

        Returns
        -------
        int:
            Maximum read data queue size of a device.
        """
        return self._clib.get_read_data_queue_size(self.deviceID)

    @queue_size.setter
    def queue_size(self, dataSize: int) -> None:
        """
        Sets the maximum read data queue size of a device.

        Parameters
        ----------
        dataSize : int
            Size to set the read data queue size to.

        Raises
        ------
        ValueError:
            If data size is invalid.

        IOError:
            If the command failed.
        """
        returnCode = self._clib.set_read_data_queue_size(self.deviceID, dataSize)

        if returnCode == fxe.INVALID_PARAM:
            raise ValueError(f"Invalid data_size: {dataSize}")
        if returnCode == fxe.FAILURE:
            raise IOError("Command failed")

    # -----
    # set_tunnel_mode
    # -----
    def set_tunnel_mode(self, target: str, timeout: int=30) -> bool:
        """
        Activate the bootloader in `target` and wait until either it's active
        or `timeout` seconds have passed.

        Parameters
        ----------
        target : str
            The name of the target to set (abbreviated).

        timeout : int
            The number of seconds to wait for confirmation before failing.

        Raises
        ------
        IOError
            If the device cannot be opened.

        OSError
            If cannot load the pre-compiled C libraries needed for communication.

        RuntimeError
            If the application type isn't recognized.

        Returns
        -------
        result : bool
            If `True`, the bootloader was set successfully. If `False` then
            something went wrong.
        """
        if not self.isOpen:
            raise IOError("Error: device must be open before setting tunnel mode.")

        activated = False

        while timeout > 0 and not activated:
            if timeout % 5 == 0:
                try:
                    self.activate_bootloader(target)
                except IOError:
                    pass

            sleep(0.1)

            # This function call is here and not in the while condition
            # because the device gets disconnected briefly as a part of
            # activating the bootloader, so we need a longer delay between
            # checks
            activated = self.bootloader_activated

            sleep(1)
            timeout -= 1

        return activated 
