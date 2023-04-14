import ctypes as c
import sys
from time import sleep
from typing import List

import semantic_version as sem

from . import enums as fxe
from . import utilities as fxu

# pylint: disable=too-many-lines


# ============================================
#                 DephyDevice
# ============================================
class DephyDevice:
    """
    Representation of one of Dephy's devices.
    """

    UNDEFINED = fxe.dephyDeviceErrorCodes["UNDEFINED"]
    SUCCESS = fxe.dephyDeviceErrorCodes["SUCCESS"]
    FAILURE = fxe.dephyDeviceErrorCodes["FAILURE"]
    INVALID_PARAM = fxe.dephyDeviceErrorCodes["INVALID_PARAM"]
    INVALID_DEVICE = fxe.dephyDeviceErrorCodes["INVALID_DEVICE"]
    NOT_STREAMING = fxe.dephyDeviceErrorCodes["NOT_STREAMING"]

    # -----
    # constructor
    # -----
    def __init__(
        self,
        port: str,
        baudRate: int,
        cLibVersion: str,
        logLevel: int,
        loggingEnabled: bool,
        libFile: str = "",
    ) -> None:
        self.port = port
        self.baudRate = baudRate
        self.cLibVersion = cLibVersion
        self.logLevel = logLevel
        self.loggingEnabled = loggingEnabled
        self.libFile = libFile

        self.fields: List = []
        self.deviceId: int = self.INVALID_DEVICE.value
        self._hasHabs: bool = False
        self._isChiral: bool = False
        self.streamingFrequency: int = 0
        self.heartbeatPeriod: int = 0
        self.useSafety: bool = False
        self._deviceName: str = ""
        self._deviceSide: str = ""
        self._closed: bool = True

        self._clib = fxu.load_clib(self.cLibVersion, libFile=self.libFile)

    # -----
    # destructor
    # -----
    def __del__(self) -> None:
        if not self._closed:
            self.close()

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

        if self._clib.get_device_name(self.deviceId, deviceName) != self.SUCCESS.value:
            raise RuntimeError("Could not get device name.")

        return deviceName.value.decode("utf8").lower()

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

        if self._clib.get_side(self.deviceId, deviceSide) != self.SUCCESS.value:
            raise RuntimeError("Could not get device side.")

        side = deviceSide.value.decode("utf8")

        # If side isn't applicable (for, e.g., an actpack), string is empty
        return side.lower() if side else "undefined"

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
        self._closed = False

    # -----
    # _open
    # -----
    def _open(self) -> None:
        if self.isOpen:
            return

        if not self.port:
            print("No port given. Searching...")
            self.port = fxu.find_port(self.baudRate, self.cLibVersion, self.libFile)
            if self.port:
                print(f"Found device at: {self.port}")
            else:
                raise IOError("Could not find a device.")

        port = self.port.encode("utf-8")
        self.deviceId = self._clib.open(port, self.baudRate, self.logLevel)

        if self.deviceId in (self.INVALID_DEVICE.value, -1):
            raise IOError("Failed to open device.")

    # -----
    # _setup
    # -----
    def _setup(self) -> None:
        givenVer = sem.Version(self.cLibVersion)
        libVer = sem.Version(self.libsVersion)

        try:
            assert givenVer == libVer
        except AssertionError as err:
            if givenVer.major == libVer.major:
                msg = f"Given lib version: `{givenVer}` doesn't match file lib "
                msg += f"version: `{libVer}`, but major versions match. Proceed[y|n]?"
                proceed = input(msg)
                if proceed != "y":
                    sys.exit(1)
            else:
                msg = f"{givenVer} doesn't match {libVer} (C lib version)"
                raise AssertionError(msg) from err

        self._deviceName = self.deviceName
        self._deviceSide = self.deviceSide

        if self._deviceName in fxe.hasHabs:
            self._hasHabs = True

        if self._deviceName in fxe.hasChirality:
            self._isChiral = True

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

        if retCode != self.SUCCESS.value:
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

        # https://code.activestate.com/lists/python-list/704158
        labels = (c.POINTER(c.c_char) * maxFields)()

        for i in range(maxFields):
            labels[i] = c.create_string_buffer(maxFieldLength)

        retCode = self._clib.get_fields(self.deviceId, labels, c.byref(nLabels))

        if retCode != self.SUCCESS.value:
            raise RuntimeError("Could not get device field labels.")

        # Convert the labels from chars to python strings
        fields = [""] * nLabels.value
        for i in range(nLabels.value):
            for j in range(maxFieldLength):
                fields[i] += labels[i][j].decode("utf8")
            fields[i] = fields[i].strip("\x00")

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
            self._clib.close(self.deviceId)

        # If close is called manually, when destructor is called during
        # garbage collection, isStreaming will raise a runtimeerror
        self._closed = True

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
                assert 50 <= hbp < self.streamingFrequency
            except AssertionError as err:
                msg = "Heartbeat period must be >= 50 and < frequency."
                raise ValueError(msg) from err

            retCode = self._clib.start_streaming_with_safety(
                self.deviceId, frequency, _log, self.heartbeatPeriod
            )

        else:
            retCode = self._clib.start_streaming(self.deviceId, frequency, _log)

        if retCode != self.SUCCESS.value:
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
        if self._clib.stop_streaming(self.deviceId) != self.SUCCESS.value:
            raise RuntimeError("Failed to stop streaming.")

    # -----
    # read
    # -----
    def read(self, allData: bool = False) -> dict | List[dict]:
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
        deviceData = (c.c_int32 * maxDataElements)()

        retCode = self._clib.read(
            self.deviceId, c.cast(deviceData, c.POINTER(c.c_int32)), c.byref(nFields)
        )

        if retCode != self.SUCCESS.value:
            raise RuntimeError("Could not read from device.")

        try:
            assert nFields.value == len(self.fields)
        except AssertionError as err:
            raise AssertionError("Incorrect number of fields read.") from err

        data = [deviceData[i] for i in range(nFields.value)]

        return dict(zip(self.fields, data))

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
        data = (c.POINTER(c.c_int32) * qs)()
        nElements = c.c_int()

        for i in range(qs):
            data[i] = (c.c_int32 * len(self.fields))()

        self._clib.read_all(self.deviceId, data, c.byref(nElements))

        try:
            assert nElements.value == len(self.fields)
        except AssertionError as err:
            raise AssertionError(
                "Different number of fields read than expected."
            ) from err

        allData = []

        for i in range(qs):
            singleTimeStepData = []
            for j in range(nElements.value):
                singleTimeStepData.append(data[i][j])
            allData.append(dict(zip(self.fields, singleTimeStepData)))

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
        # There is a bug where, sometimes, the gains aren't set, so we try multiple
        # times
        for _ in range(5):
            if self._clib.set_gains(devId, kp, ki, kd, k, b, ff) != self.SUCCESS.value:
                raise RuntimeError("Command failed")
            sleep(0.001)

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
        if (
            self._clib.send_motor_command(devId, controller, value)
            != self.SUCCESS.value
        ):
            raise RuntimeError("Could not command motor position.")

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
        if (
            self._clib.send_motor_command(devId, controller, value)
            != self.SUCCESS.value
        ):
            raise RuntimeError("Could not command motor current.")

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
        if (
            self._clib.send_motor_command(devId, controller, value)
            != self.SUCCESS.value
        ):
            raise RuntimeError("Could not command motor voltage.")

    # -----
    # command_motor_impedance
    # -----
    def command_motor_impedance(self, value: int) -> None:
        """
        Has the motor simulate a stretched from current position to
        the desired position using the damping gain b and stiffness
        gain k.

        Parameters
        ----------
        value : int
            Desired motor position in ticks.

        Raises
        ------
        RuntimeError:
            If the command failed.
        """
        devId = self.deviceId
        controller = fxe.controllers["impedance"]
        if (
            self._clib.send_motor_command(devId, controller, value)
            != self.SUCCESS.value
        ):
            raise RuntimeError("Could not command motor impedance.")

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
        if self._clib.send_motor_command(devId, controller, 0) != self.SUCCESS.value:
            raise RuntimeError("Could not stop motor.")

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

        if self._clib.find_poles(self.deviceId) != self.SUCCESS.value:
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
        targetCode = fxe.bootloaderTargets[target]

        returnCode = self._clib.activate_bootloader(self.deviceId, targetCode)

        if returnCode == self.INVALID_DEVICE.value:
            raise RuntimeError(f"Invalid device ID for: `{target}`.")
        if returnCode != self.SUCCESS.value:
            raise IOError

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
        if self._clib.is_bootloader_activated(self.deviceId) != self.SUCCESS.value:
            return False

        return True

    # -----
    # rigidVersion
    # -----
    @property
    def rigidVersion(self) -> str:
        raise RuntimeError("Devices don't currently know their own hardware version.")

    # -----
    # firmware
    # -----
    @property
    def firmware(self) -> dict:
        """
        Gets the fimware versions of device's MCUs.

        Raises
        ------
        RuntimeError:
            Command failed.

        Returns
        -------
        Dict
            A dictionary with the semantic version strings of manage,
            execute, and regulate's firmware. And habs, if applicable.
        """
        if self._clib.request_firmware_version(self.deviceId) != self.SUCCESS.value:
            raise RuntimeError("Command failed")

        sleep(5)

        fw = self._clib.get_last_received_firmware_version(self.deviceId)
        fwDict = {
            "mn": fxu.decode(fw.mn),
            "ex": fxu.decode(fw.ex),
            "re": fxu.decode(fw.re),
        }

        if self._hasHabs:
            fwDict["habs"] = fxu.decode(fw.habs)

        return fwDict

    # -----
    # print
    # -----
    def print(self, data: dict | None = None) -> None:
        """
        Reads the data from the device and then prints it to the screen.
        If data is given, we print that instead.
        """
        if data is None:
            data = self.read()
        for key, value in data.items():
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
        return self._clib.get_read_data_queue_size(self.deviceId)

    @queueSize.setter
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
        returnCode = self._clib.set_read_data_queue_size(self.deviceId, dataSize)

        if returnCode == self.INVALID_PARAM:
            raise ValueError(f"Invalid data_size: {dataSize}")
        if returnCode == self.FAILURE:
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
            activated = self.bootloaderActive

        return activated

    # -----
    # uvlo
    # -----
    @property
    def uvlo(self) -> int:
        """
        Gets the currently set UVLO.
        """
        if self._clib.request_uvlo(self.deviceId) != self.SUCCESS.value:
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
        if self._clib.set_uvlo(self.deviceId, value) != self.SUCCESS.value:
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

        if self._clib.calibrate_imu(self.deviceId) != self.SUCCESS.value:
            raise RuntimeError("Could not calibrate imu.")

    # -----
    # num_utts
    # -----
    @property
    def num_utts(self) -> int:
        """
        The number of available UTT values is saved as #define NUM_UTT_VALS
        in the C library, so we have this convenience wrapper to access it.
        """
        try:
            return self._clib.get_num_utts()
        except AttributeError:
            print(f"Error: api version: `{self.cLibVersion}` cannot call `num_utts`")
            sys.exit(1)

    # -----
    # set_all_utts
    # -----
    def set_all_utts(self, uttVals: List[int]) -> None:
        """
        Takes in a list of integer values and assigns each one to a UTT
        value.

        Parameters
        ----------
        uttVals : List[int]
            List of values, one for each UTT
        """
        numUtts = self.num_utts
        nVals = len(uttVals)

        try:
            assert nVals <= numUtts
        except AssertionError:
            print("Error: too many UTT values given.")
            sys.exit(1)

        data = (c.c_int * nVals)()

        for i in range(nVals):
            data[i] = c.c_int(uttVals[i])

        retCode = self._clib.set_utts(self.deviceId, data, nVals, c.c_byte(-1))

        if retCode != self.SUCCESS.value:
            print("Error: could not set UTT values.")
            sys.exit(1)

    # -----
    # set_utt
    # -----
    def set_utt(self, uttVal: int, index: int) -> None:
        """
        Sets the value of a single UTT.

        Parameters
        ----------
        uttVal : int
            The value the desired UTT will be set to

        index : int
            The array index for the desired UTT
        """
        numUtts = self.num_utts

        try:
            assert 0 <= index < numUtts
        except AssertionError:
            print("Error: invalid UTT index.")

        data = (c.c_int * numUtts)()

        data[index] = c.c_int(uttVal)

        retCode = self._clib.set_utts(self.deviceId, data, numUtts, c.c_byte(index))

        if retCode != self.SUCCESS.value:
            print("Error: could not set UTT value.")
            sys.exit(1)

    # -----
    # reset_utts
    # -----
    def reset_utts(self) -> None:
        """
        Resets all UTTs to their default values.
        """
        if self._clib.reset_utts(self.deviceId) != self.SUCCESS.value:
            print("Error: could not reset UTTs to their default values.")
            sys.exit(1)

    # -----
    # save_utts
    # -----
    def save_utts(self) -> None:
        """
        Saves the current UTT values to the device's internal memory so
        that they persist across power cycles.
        """
        if self._clib.save_utts(self.deviceId) != self.SUCCESS.value:
            print("Error: could not save UTTs.")
            sys.exit(1)

    # -----
    # read_utts
    # -----
    def read_utts(self) -> List[int]:
        """
        UTTs are not sent as a part of regular communication, so here we
        first request that the device send the UTTs to Mn, and then we
        read them.
        """
        if self._clib.request_utts(self.deviceId) != self.SUCCESS.value:
            print("Error: could not request UTTs.")
            sys.exit(1)
        # We have to sleep for a bit in order to allow the device time
        # to fulfill the request
        sleep(0.25)

        numUtts = self.num_utts
        data = (c.c_int * numUtts)()
        retCode = self._clib.get_last_received_utts(self.deviceId, data, numUtts)

        if retCode != self.SUCCESS.value:
            print("Error: could not read UTTs.")
            sys.exit(1)

        return [data[i] for i in range(numUtts)]

    # -----
    # hasHabs
    # -----
    @property
    def hasHabs(self) -> bool:
        if self._deviceName:
            return self._hasHabs
        raise RuntimeError("Must call open before checking hasHabs.")

    # -----
    # isChiral
    # -----
    @property
    def isChiral(self) -> bool:
        if self._deviceName:
            return self._isChiral
        raise RuntimeError("Must call open before checking isChiral.")
