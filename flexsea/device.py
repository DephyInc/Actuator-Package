import ctypes as c
import setuptools.version as ver
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
        self._version_check(cLibVersion)

        self.port = port
        self.baudRate = baudRate
        self.cLibVersion = cLibVersion
        self.logLevel = logLevel
        self.loggingEnabled = loggingEnabled

        self.fields: List = []
        self.deviceID: int = fxe.INVALID_DEVICE.value
        self.hasHabs: bool = False
        self.streamingFrequency: int = 0
        self.heartbeatPeriod: int = 0
        self.useSafety: bool = False
        self._deviceName: str = ""
        self._deviceSide: str = ""

        self._clib = fxu.load_clib(self.cLibVersion)

        try:
            assert self.cLibVersion == self.libs_version
        except AssertionError:
            raise AssertionError("Given and actual library versions don't match.")

    # -----
    # _version_check
    # -----
    def _version_check(self, using: str) -> None:
        inUse = ver.pkg_resources.parse_version(cLibVersion)
        cutoff = ver.pkg_resources.parse_version(cfg.legacyCutoff)

        if inUse < cutoff:
            msg = f"For versions of the pre-compiled C libraries < {cfg.legacyCutoff} "
            msg += "please use the `LegacyDevice` class."
            raise ValueError(msg)

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
    def __exit__(self, excType, excVal, excTb) -> None:
        if excType is not None:
            print(f"Exception: {excVal}")
            print(f"{excTb}")

    # -----
    # isOpen
    # -----
    @property
    def isOpen(self) -> bool:
        return self._clib.is_open(self.deviceId)

    # -----
    # isStreaming
    # -----
    @property
    def isStreaming(self) -> bool:
        return self._clib.is_streaming(self.deviceId)

    # -----
    # deviceName
    # -----
    @property
    def deviceName(self) -> str:
        """
        Queries the device for it's type name, e.g., `actpack`.

        Raises
        ------
        RuntimeError:
            If we cannot get the device's name.
        """
        if self._deviceName:
            return self._deviceName

        maxDeviceNameLength = self._clib.get_max_device_name_length()
        deviceName = (c.c_char * maxDeviceNameLength)()

        if self._clib.get_device_name(self.deviceId, deviceName) != fxe.SUCCESS.value:
            raise RuntimeError("Could not get device name.")

        return deviceName.value.decode("utf8")

    # -----
    # deviceSide
    # -----
    @property
    def deviceSide(self) -> str:
        """
        Queries the device for it's side name, e.g., `left`.

        Raises
        ------
        RuntimeError:
            If we cannot get the device's side.
        """
        if self._deviceSide:
            return self._deviceSide

        maxDeviceSideLength = self._clib.get_max_device_side_length()
        deviceSide = (c.c_char * maxDeviceSideLength)()

        if self._clib.get_side(self.deviceId, deviceSide) != fxe.SUCCESS.value:
            raise RuntimeError("Could not get device name.")

        side = deviceSide.value.decode("utf8")

        # If side isn't applicable (for, e.g., an actpack), string is empty
        return side if side else "undefined"

    # -----
    # open
    # -----
    def open(self) -> None:
        """
        Establish a connection with a device.

        Raises
        ------
        IOError:
            If we fail to open the device.
        """
        self._open()
        self._setup()

    # -----
    # _open
    # -----
    def _open(self) -> None:
        if self.isOpen:
            return

        port = self.port.encode("utf-8")
        self.deviceID = self._clib.open(port, self.baudRate, self.logLevel)

        if self.deviceID in (fxe.INVALID_DEVICE.value, -1):
            raise IOError("Failed to open device.")

    # -----
    # _setup
    # -----
    def _setup(self) -> None:
        try:
            assert self.cLibVersion == self.libsVersion
        except AssertionError:
            raise AssertionError("Given and actual library versions don't match.")

        self._deviceName = self.deviceName
        self._deviceSide = self.deviceSide

        if self._deviceName in fxe.hasHabs:
            self.hasHabs = True

        self.fields = self._get_fields()

    # -----
    # libsVersion
    # -----
    @property
    def libsVersion(self) -> str:
        """
        Gets the version of the precompiled C libraries being used.

        Raises
        ------
        RuntimeError:
            If we fail to get the version.
        """
        major = c.c_uint16(-1)
        minor = c.c_uint16(-1)
        patch = c.c_uint16(-1)

        retCode = self._clib.get_libs_version(
            c.byref(major), c.byref(minor), c.byref(patch)
        )

        if retCode != fxe.SUCCESS.value:
            raise RuntimeError("Could not determine clibs version.")

        return f"{major.value}.{minor.value}.{patch.value}"

    # -----
    # _get_fields
    # -----
    def _get_fields(self) -> List[str]:
        """
        Query the device for its available data fields.

        Raises
        ------
        RuntimeError
            If we fail to get the device's field names.
        """
        if self.fields:
            return self.fields

        maxFields = self._clib.get_max_data_elements()
        maxFieldLength = self._clib.get_max_field_name_length()
        nLabels = c.c_int()

        # Create types for holding labels
        labelType = c.c_char * maxFieldLength
        labelsType = c.POINTER(c.c_char) * maxFields

        # Allocate memory for the labels container
        labels = labelsType()
        for i in range(maxFields):
            labels[i] = labelType()

        retCode = self._clib.get_fields(self.deviceId, labels, c.by_ref(nLabels))

        if retCode != fxe.SUCCESS.value:
            raise RuntimeError("Could not get device field labels.")

        # Convert the labels from chars to python strings
        fields = [""] * nLabels.value
        for i in range(nLabels.value):
            for j in range(maxFieldLength):
                fields[i] += labels[i][j].decode("utf8")
            fields[i].strip("\x00")

        return fields

    # -----
    # close
    # -----
    def close(self) -> None:
        """
        Disconnect from a device.
        """
        if self.isStreaming:
            self.stop_streaming()

        if self.isOpen:
            self.stop_motor()
            self._clib.close(self.deviceID)

    # -----
    # start_streaming
    # -----
    def start_streaming(
        self, frequency: int, heartbeatPeriod: int = 50, useSafety: bool = False
    ) -> None:
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
            If the stream failed or if `open` hasn't been called.

        ValueError:
            If the heartbeatPeriod is invalid.
        """
        if self.isStreaming:
            print("Already streaming.")
            return

        if not self.isOpen:
            raise RuntimeError("Call `open` first.")

        self.streamingFrequency = frequency
        self.heartbeatPeriod = heartbeatPeriod
        self.useSafety = useSafety

        _log = 1 if self.loggingEnabled else 0

        if self.useSafety:
            hbp = self.heartbeatPeriod

            try:
                assert hbp >= 50 and hbp < self.streamingFrequency
            except AssertionError as err:
                msg = "Heartbeat period must be >= 50 and < frequency."
                raise ValueError(msg) from err

            retCode = self._clib.start_streaming_with_safety(
                self.deviceID, frequency, _log, self.heartbeatPeriod
            )

        else:
            retCode = self._clib.start_streaming(self.deviceID, frequency, _log)

        if retCode != fxe.SUCCESS.value:
            raise RuntimeError("Could not start stream.")

    # -----
    # stop_streaming
    # -----
    def stop_streaming(self) -> None:
        """
        Stop streaming data from a device.

        Raises
        ------
        RuntimeError:
            If the stream failed to stop.
        """
        if self._clib.stop_streaming(self.deviceID) != fxe.SUCCESS.value:
            raise RuntimeError("Failed to stop streaming.")

    # -----
    # read
    # -----
    def read(self, allData: bool = False) -> dict:
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

        Returns
        -------
        dict:
            Data read from device.
        """
        if not self.isStreaming:
            raise RuntimeError("Must call `start_streaming()` before reading data.")

        return self._read() if not allData else self._read_all()

    # -----
    # _read
    # -----
    def _read(self) -> dict:
        """
        The device returns a list of values. We then have to pair those values
        with their corresponding labels.

        Raises
        ------
        RuntimeError:
            If reading fails.

        AssertionError:
            If the number of fields and amount of data read differ.

        Returns
        -------
        dict:
            Label-value pairs read from the device.
        """
        maxDataElements = self._clib.get_max_data_elements()
        nFields = c.c_int()
        deviceData = (c.POINTER(c.c_uint32) * maxDataElements)()

        retCode = self._clib.read(self.deviceId, deviceData, c.by_ref(nFields))

        if retCode != fxe.SUCCESS.value:
            raise RuntimeError("Could not read from device.")

        try:
            assert nFields.value == len(self.fields)
        except AssertionError:
            raise AssertionError("Incorrect number of fields read.")

        data = [deviceData[i].value for i in range(nFields.value)]

        return {key: value for (key, value) in zip(self.fields, data)}

    # -----
    # _read_all
    # -----
    def _read_all(self) -> List[dict]:
        """
        Data from each timestep is stored in a queue on the device. Here
        we get the current size of that queue and then read from it.

        NOTE: Can the queue size change between getting the size and reading
        the data from it?

        Raises
        ------
        AssertionError:
            If the number of fields differs from what's expected.

        Returns
        -------
        List[dict]:
            Each element in the list is data from a particular timestep keyed
            by the field name.
        """
        qs = self.queueSize
        data = (c.POINTER(c.c_uint32) * qs)()
        nElements = c.c_int()

        for i in range(qs):
            data[i] = (c.c_uint32 * len(self.fields))()

        self._clib.read_all(self.deviceId, data, c.byref(nElements))

        try:
            assert nElements.value == len(self.fields)
        except AssertionError:
            raise AssertionError("Different number of fields read than expected.")

        allData = []

        for i in range(qs):
            singleTimeStepData = []
            for j in range(nElements.value):
                singleTimeStepData.append(data[i][j])
            allData.append({k: v for k, v in zip(self.fields, singleTimeStepData)})

        return allData

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
        RuntimeError:
            Command failed.
        """
        devId = self.deviceId
        if self._clib.set_gains(devID, kp, ki, kd, k, b, ff) != fxe.SUCCESS.value:
            raise RuntimeError("Command failed")

    # -----
    # command_motor_position
    # -----
    def command_motor_position(self, value: int) -> None:
        """
        Sets motor to given position.

        Parameters
        ----------
        value : int
            Desired motor position in encoder units.

        Raises
        ------
        RuntimeError:
            If the command failed.
        """
        devId = self.deviceId
        controller = fxe.controllers["position"]
        if self._clib.send_motor_command(devId, controller, value) != fxe.SUCCESS.value:
            raise RuntimeError("Coult not command motor position.")

    # -----
    # command_motor_current
    # -----
    def command_motor_current(self, value: int) -> None:
        """
        Sends the given current to the motor.

        Parameters
        ----------
        value : int
            Desired motor current in milli-Amps.

        Raises
        ------
        RuntimeError:
            If the command failed.
        """
        devId = self.deviceId
        controller = fxe.controllers["current"]
        if self._clib.send_motor_command(devId, controller, value) != fxe.SUCCESS.value:
            raise RuntimeError("Coult not command motor current.")

    # -----
    # command_motor_voltage
    # -----
    def command_motor_voltage(self, value: int) -> None:
        """
        Sets motor's voltage.

        Parameters
        ----------
        value : int
            Desired motor voltage in milli-volts.

        Raises
        ------
        RuntimeError:
            If the command failed.
        """
        devId = self.deviceId
        controller = fxe.controllers["voltage"]
        if self._clib.send_motor_command(devId, controller, value) != fxe.SUCCESS.value:
            raise RuntimeError("Coult not command motor voltage.")

    # -----
    # command_motor_impedance
    # -----
    def command_motor_impedance(self, value: int) -> None:
        """
        Sets motor's impedance.

        Parameters
        ----------
        value : int
            Desired motor impedance in milli-amps.

        Raises
        ------
        RuntimeError:
            If the command failed.
        """
        devId = self.deviceId
        controller = fxe.controllers["impedance"]
        if self._clib.send_motor_command(devId, controller, value) != fxe.SUCCESS.value:
            raise RuntimeError("Coult not command motor impedance.")

    # -----
    # stop_motor
    # -----
    def stop_motor(self):
        """
        Stops the motor.

        Raises
        ------
        RuntimeError:
            If the command failed.
        """
        devId = self.deviceId
        controller = fxe.controllers["none"]
        if self._clib.send_motor_command(devId, controller, 0) != fxe.SUCCESS.value:
            raise RuntimeError("Coult not stop motor.")

    # -----
    # find_poles
    # -----
    def find_poles(self) -> None:
        """
        DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING!

        Instructs the device to go through the pole-finding process.

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

        if self._clib.find_poles(self.deviceID) != fxe.SUCCESS.value:
            raise ValueError("Command failed")

        msg = "NOTE: Please wait for the process to complete. The motor will stop "
        msg += "moving when it is done. It usually takes 1-2 minutes to complete."
        print(msg)

        msg = "NOTE: Once the pole-finding procedure is completed, you must "
        msg += "power cylce the device for the changes to take effect."
        print(msg)

    # -----
    # activate_bootloader
    # -----
    def activate_bootloader(self, target: str) -> None:
        """
        Activates target bootloader.

        Parameters
        ----------
        target : str
            Bootloader target. Can be: mn, ex, re, or habs.

        Raises
        ------
        RuntimeError:
            Command failed.
        """
        target = fxe.bootloaderTargets[target]

        returnCode = self._clib.activate_bootloader(self.deviceID, target)

        if returnCode != fxe.SUCCESS.value:
            raise RuntimeError(f"Could not activate bootloader for: `{target}`.")

    # -----
    # bootloaderActive
    # -----
    @property
    def bootloaderActive(self) -> bool:
        """
        Get status of bootloader.

        Raises
        ------
        RunttimeError:
            Command failed.

        Returns
        -------
        bool
            `True` if bootloader is active and `False` otherwise.
        """
        if self._clib.is_bootloader_activated(self.deviceID) != fxe.SUCCESS.value:
            return False

        return True

    # -----
    # rigidVersion
    # -----
    @property
    def rigidVersion(self) -> str:
        raise NotImplementedError

    # -----
    # firmware
    # -----
    @property
    def firmware(self) -> List[str]:
        """
        Gets the fimware versions of device's MCUs.

        Raises
        ------
        RuntimeError:
            Command failed.

        Returns
        -------
        List
            A list with the semantic version strings of manage,
            execute, and regulate's firmware.
        """
        if self._clib.request_firmware_version(self.deviceID) != fxe.SUCCESS.value:
            raise RuntimeError("Command failed")

        sleep(5)

        fw = self._clib.get_last_received_firmware_version(self.deviceID)
        fwList = [fxu.decode(fw.mn), fxu.decode(fw.ex), fxu.decode(fw.re)]

        if self.hasHabs:
            fwList.append(fxu.decode(fw.habs))

        return fwList

    # -----
    # print
    # -----
    def print(self) -> None:
        """
        Reads the data from the device and then prints it to the screen.
        """
        for key, value in self.read().items():
            print(f"{key} : {value}")

    # -----
    # queueSize
    # -----
    @property
    def queueSize(self) -> int:
        """
        Get the maximum read data queue size of a device.

        Returns
        -------
        int:
            Maximum read data queue size of a device.
        """
        return self._clib.get_read_data_queue_size(self.deviceID)

    @queue_size.setter
    def queueSize(self, dataSize: int) -> None:
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

        RuntimeError:
            If the command failed.
        """
        returnCode = self._clib.set_read_data_queue_size(self.deviceID, dataSize)

        if returnCode == fxe.INVALID_PARAM:
            raise ValueError(f"Invalid data_size: {dataSize}")
        if returnCode == fxe.FAILURE:
            raise RuntimeError("Command failed")

    # -----
    # set_tunnel_mode
    # -----
    def set_tunnel_mode(self, target: str, timeout: int = 30) -> bool:
        """
        All communication goes through Manage, so we need to put it into
        tunnel mode in order to activate the other bootloaders. When bootloading
        Manage itself, this causes it to reboot in DFU mode.

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

            # Device gets disconnected briefly when Mn resets, so we wait
            sleep(1)
            timeout -= 1
            activated = self.bootloader_activated

        return activated

    # -----
    # uvlo
    # -----
    @property
    def uvlo(self) -> int:
        """
        Gets the currently set UVLO.
        """
        if self._clib.request_uvlo(self.deviceId) != fxe.SUCCESS.value:
            raise RuntimeError("Could not request firmware version.")

        # Let the device process the request
        sleep(5)

        uvlo = self._clib.read_uvlo(self.deviceId)

        if uvlo == -1:
            raise RuntimeError("Could not get requested UVLO.")

        return uvlo

    @uvlo.setter
    def uvlo(self, value: int) -> None:
        """
        Sets the UVLO value for the device. `value` needs to be in milli-volts.
        """
        if self._clib.set_uvlo(self.deviceId, value) != fxe.SUCCESS.value:
            raise RuntimeError("Could not set UVLO.")

    # -----
    # calibrate_imu
    # -----
    def calibrate_imu(self) -> None:
        """
        DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING!

        Instructs the device to go through the IMU calibration process.

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
            print("Aborting IMU calibration.")
            return

        if self.clib.calibrate_imu(self.deviceId) != fxe.SUCCESS.value:
            raise RuntimeError("Could not calibrate imu.")
