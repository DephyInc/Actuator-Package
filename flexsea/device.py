import ctypes as c
from pathlib import Path
from time import sleep
from typing import List

from semantic_version import Version

import flexsea.utilities.constants as fxc
from flexsea.utilities.decorators import minimum_required_version
from flexsea.utilities.decorators import requires_status
from flexsea.utilities.decorators import validate
from flexsea.utilities.firmware import decode_firmware
from flexsea.utilities.firmware import validate_given_firmware_version
from flexsea.utilities.library import get_c_library
from flexsea.utilities.library import set_prototypes
from flexsea.utilities.library import set_read_functions
from flexsea.utilities.specs import get_device_spec


# ============================================
#                   Device
# ============================================
class Device:
    """
    Representation of one of Dephy's devices. Serves as a way to
    send commands to and read data from a Dephy device.
    """

    # -----
    # constructor
    # -----
    def __init__(
        self,
        firmwareVersion: str,
        port: str,
        baudRate: int = fxc.baudRate,
        libFile: str = "",
        logLevel: int = 4,
        interactive: bool = True,
    ) -> None:
        # These are first so destructor won't complain if setup fails
        # attributes
        self.connected: bool = False
        self.streaming: bool = False
        self.interactive = interactive

        self.port: str = port
        self.firmwareVersion: Version = validate_given_firmware_version(
            firmwareVersion, self.interactive
        )

        if libFile:
            self.libFile = Path(libFile).expanduser().absolute()
        else:
            self.libFile = None

        try:
            assert baudRate > 0
        except AssertionError as err:
            raise ValueError("Error: baud rate must be positive.") from err
        self.baudRate = baudRate

        try:
            assert 0 <= logLevel <= 6
        except AssertionError as err:
            raise ValueError("Log level must be in [0, 6].") from err
        self.logLevel = logLevel

        self.heartbeat: int = 0
        self.id: int = 0
        self.streamingFrequency: int = 0

        (clib, self.libFile) = get_c_library(self.firmwareVersion, self.libFile)
        self._clib = set_prototypes(clib, self.firmwareVersion)

        self._fields: List[str] | None = None
        self._gains: dict = {}
        self._hasHabs: bool | None = None
        self._name: str = ""
        self._side: str = ""
        self._state: c.Structure | None = None
        self._stateType: c.Structure | None = None

        if self.firmwareVersion < fxc.legacyCutoff:
            self._SUCCESS = c.c_int(0)
            self._FAILURE = c.c_int(1)
            self._INVALID_PARAM = c.c_int(2)
            self._INVALID_DEVICE = c.c_int(3)
            self._NOT_STREAMING = c.c_int(4)
            self._isLegacy = True
            self._libVersion = "undefined"

        else:
            self._UNDEFINED = c.c_int(0)
            self._SUCCESS = c.c_int(1)
            self._FAILURE = c.c_int(2)
            self._INVALID_PARAM = c.c_int(3)
            self._INVALID_DEVICE = c.c_int(4)
            self._NOT_STREAMING = c.c_int(5)
            self._isLegacy = False
            self._libVersion = self._get_lib_version()

        print(f"Firmware version: {self.firmwareVersion}\nLibrary: {self.libFile}")

    # -----
    # destructor
    # -----
    def __del__(self) -> None:
        self.close()

    # -----
    # open
    # -----
    def open(self) -> None:
        """
        Establish a connection to a device. This is needed in order
        to send commands to the device and/or receive data from the
        device.
        """
        if self.connected:
            print("Already connected.")
            return

        port = self.port.encode("utf-8")

        self.id = self._clib.fxOpen(port, self.baudRate, self.logLevel)

        if self.id in (self._INVALID_DEVICE.value, -1):
            raise RuntimeError("Failed to connect to device.")

        self.connected = True

        self._name = self.name
        self._side = self.side
        self._hasHabs = self._name not in fxc.noHabs

        self._get_info_for_reading()

    # -----
    # _get_info_for_reading
    # -----
    def _get_info_for_reading(self) -> None:
        if self._isLegacy:
            self._get_state()
        else:
            self._get_fields()
        self._clib = set_read_functions(
            self._clib, self._name, self._isLegacy, self._stateType
        )

    # -----
    # _get_state
    # -----
    def _get_state(self) -> None:
        stateSpec = get_device_spec(self._name, self.firmwareVersion)

        class LegacyDeviceState(c.Structure):
            _pack_ = 1
            _fields_ = [(k, getattr(c, v)) for k, v in stateSpec.items()]

        self._stateType = LegacyDeviceState
        self._state = LegacyDeviceState()

    # -----
    # _get_fields
    # -----
    def _get_fields(self) -> None:
        maxFields = self._clib.fxGetMaxDataElements()
        maxFieldLength = self._clib.fxGetMaxDataLabelLength()
        nLabels = c.c_int()

        # https://code.activestate.com/lists/python-list/704158
        labels = (c.POINTER(c.c_char) * maxFields)()

        for i in range(maxFields):
            labels[i] = c.create_string_buffer(maxFieldLength)

        retCode = self._clib.fxGetDataLabelsWrapper(self.id, labels, c.byref(nLabels))

        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not get device field labels.")

        # Convert the labels from chars to python strings
        fields = [""] * nLabels.value
        if self._fields is None:
            self._fields = []
        for i in range(nLabels.value):
            for j in range(maxFieldLength):
                fields[i] += labels[i][j].decode("utf8")
            fields[i] = fields[i].strip("\x00")
            self._fields.append(fields[i])

    # -----
    # close
    # -----
    def close(self) -> None:
        """
        Severs connection with device. Will no longer be able to send
        commands or receive data.
        """
        if self.streaming:
            self.stop_streaming()

        if self.connected:
            self.stop_motor()
            self._clib.fxClose(self.id)
            self.connected = False

    # -----
    # start_streaming
    # -----
    @requires_status("connected")
    def start_streaming(
        self, frequency: int, heartbeat: int = 0, useSafety: bool = False
    ) -> None:
        """
        Instructs the device to send us data at the given `frequency`.

        Parameters
        ----------
        frequency : int
            The number of times per second the device should send data

        heartbeat : int
            When streaming, the computer periodically sends a message to
            the device to let it know that the connection between them
            is still alive. These are called heartbeat messages. This
            variable specifies the amount of time (in milliseconds)
            between successive heartbeat messages. This is related to
            how long the device will wait without receiving a heartbeat
            message before shutting itself off (five times `heartbeat`).

        useSafety : bool
            If `True`, the device will stop the motor if it doesn't receive
            a heartbeat message in time.

        Raises
        ------
        ValueError
            If `frequency` or `heartbeat` are invalid.
        """
        if self.streaming:
            print("Already streaming.")
            return

        try:
            assert frequency > 0
        except AssertionError as err:
            raise ValueError("Frequency must be > 0.") from err

        self.streamingFrequency = frequency

        self.heartbeat = heartbeat

        if useSafety:
            self._stream_with_safety()
        else:
            self._stream_without_safety()

        self.streaming = True

    # -----
    # _stream_with_safety
    # -----
    @minimum_required_version("9.1.0")
    @validate
    def _stream_with_safety(self) -> int:
        try:
            assert fxc.minHeartbeat <= self.heartbeat < self.streamingFrequency
        except AssertionError as err:
            msg = f"Heartbeat must be in [{fxc.minHeartbeat}, frequency]"
            raise ValueError(msg) from err

        return self._clib.fxStartStreamingWithSafety(
            self.id, self.streamingFrequency, 1, self.heartbeat
        )

    # -----
    # _stream_without_safety
    # -----
    @validate
    def _stream_without_safety(self) -> int:
        return self._clib.fxStartStreaming(self.id, self.streamingFrequency, 1)

    # -----
    # stop_streaming
    # -----
    @requires_status("streaming")
    def stop_streaming(self) -> int:
        """
        Instructs the device to stop sending data.
        """
        retCode = self._clib.fxStopStreaming(self.id)

        if retCode != self._SUCCESS.value:
            raise RuntimeError("Failed to stop streaming.")

        self.streaming = False

    # -----
    # set_gains
    # -----
    @requires_status("connected")
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
        """
        # There is a bug either on the C side or in the firmware where,
        # sometimes, the gains aren't set, so we try multiple times
        for _ in range(5):
            returnCode = self._clib.fxSetGains(self.id, kp, ki, kd, k, b, ff)
            sleep(0.001)
        if returnCode != self._SUCCESS.value:
            raise RuntimeError("Failed to set gains.")
        self._gains = {"kp": kp, "ki": ki, "kd": kd, "k": k, "b": b, "ff": ff}

    # -----
    # command_motor_position
    # -----
    @requires_status("connected")
    @validate
    def command_motor_position(self, value: int) -> int:
        """
        Sets motor to given position.

        Parameters
        ----------
        value : int
            Desired motor position in encoder units.
        """
        controller = fxc.controllers["position"]
        return self._clib.fxSendMotorCommand(self.id, controller, value)

    # -----
    # command_motor_current
    # -----
    @requires_status("connected")
    @validate
    def command_motor_current(self, value: int) -> int:
        """
        Sends the given current to the motor.

        Parameters
        ----------
        value : int
            Desired motor current in milli-Amps.
        """
        controller = fxc.controllers["current"]
        return self._clib.fxSendMotorCommand(self.id, controller, value)

    # -----
    # command_motor_voltage
    # -----
    @requires_status("connected")
    @validate
    def command_motor_voltage(self, value: int) -> int:
        """
        Sets motor's voltage.

        Parameters
        ----------
        value : int
            Desired motor voltage in milli-volts.
        """
        controller = fxc.controllers["voltage"]
        return self._clib.fxSendMotorCommand(self.id, controller, value)

    # -----
    # command_motor_impedance
    # -----
    @requires_status("connected")
    @validate
    def command_motor_impedance(self, value: int) -> int:
        """
        Has the motor simulate a stretched from current position to
        the desired position using the damping gain b and stiffness
        gain k.

        Parameters
        ----------
        value : int
            Desired motor position in ticks.
        """
        controller = fxc.controllers["impedance"]
        return self._clib.fxSendMotorCommand(self.id, controller, value)

    # -----
    # stop_motor
    # -----
    @requires_status("connected")
    def stop_motor(self) -> int:
        """
        Stops the motor and resets the gains to zero.
        """
        controller = fxc.controllers["none"]
        retCode = self._clib.fxSendMotorCommand(self.id, controller, 0)
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Failed to stop motor.")
        self._gains = {"kp": 0, "ki": 0, "kd": 0, "k": 0, "b": 0, "ff": 0}
        return retCode

    # -----
    # activate_bootloader
    # -----
    @requires_status("connected")
    def activate_bootloader(self, target: str) -> None:
        """
        Activates the bootloader for `target`.

        Parameters
        ----------
        target : str
            Bootloader target. Can be: mn, ex, re, or habs.
        """
        # We deliberately aren't using @validate here because we need
        # access to the IOError in `set_tunnen_mode`
        targetCode = fxc.bootloaderTargets[target]
        retVal = self._clib.fxActivateBootloader(self.id, targetCode)

        if retVal == self._INVALID_DEVICE.value:
            raise RuntimeError(f"Invalid device ID for: `{target}`.")
        if retVal != self._SUCCESS.value:
            raise IOError

    # -----
    # bootloaderActive
    # -----
    @property
    @requires_status("connected")
    def bootloaderActive(self) -> bool:
        """
        Returns whether or not the bootloader is active or not.

        Returns
        -------
        bool
            `True` if bootloader is active and `False` otherwise.
        """
        returnCode = self._clib.fxIsBootloaderActivated(self.id)
        if returnCode != self._SUCCESS.value:
            return False
        return True

    # -----
    # set_tunnel_mode
    # -----
    @requires_status("connected")
    def set_tunnel_mode(self, target: str, timeout: int = 30) -> bool:
        """
        All communication goes through Manage, so we need to put it into
        tunnel mode in order to activate the other bootloaders. When bootloading
        Manage itself, this causes it to reboot in DFU mode.

        If bootloading fails for any reason once tunnel mode has been set,
        the device is bricked and must be programmed manually. The exception
        to this rule is Habs.

        Parameters
        ----------
        target : str
            The name of the target to set (abbreviated).

        timeout : int
            The number of seconds to wait for confirmation before failing.

        Returns
        -------
        activated : bool
            If `True`, the bootloader was set successfully. If `False` then
            something went wrong.
        """
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
    # firmware_version
    # -----
    @property
    @requires_status("connected")
    def firmware_version(self) -> dict:
        """
        Gets the fimware versions of device's MCUs.

        Returns
        -------
        Dict
            A dictionary with the semantic version strings of manage,
            execute, and regulate's firmware. And habs, if applicable.
        """
        self._clib.fxRequestFirmwareVersion(self.id)

        sleep(5)

        fw = self._clib.fxGetLastReceivedFirmwareVersion(self.id)

        fwDict = {
            "mn": decode_firmware(fw.mn),
            "ex": decode_firmware(fw.ex),
            "re": decode_firmware(fw.re),
        }

        if self._hasHabs:
            fwDict["habs"] = decode_firmware(fw.habs)

        return fwDict

    # -----
    # print
    # -----
    @requires_status("streaming")
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
    # read
    # -----
    @requires_status("streaming")
    def read(self, allData: bool = False) -> dict | List[dict]:
        if allData:
            if self._isLegacy:
                return self._read_all_legacy()
            return self._read_all()
        if self._isLegacy:
            return self._read_legacy()
        return self._read()

    # -----
    # _read_all_legacy
    # -----
    def _read_all_legacy(self) -> List[dict]:
        qs = self._clib.fxGetReadDataQueueSize(self.id)
        data = (self._stateType * qs)()
        allData = []

        nRead = self._clib.read_all(self.id, data, qs)

        for i in range(nRead):
            # pylint: disable-next=protected-access
            allData.append({f[0]: getattr(data[i], f[0]) for f in data[i]._fields_})

        return allData

    # -----
    # _read_all
    # -----
    def _read_all(self) -> List[dict]:
        qs = self._clib.fxGetReadDataQueueSize(self.id)
        data = (c.POINTER(c.c_int32) * qs)()
        nElements = c.c_int()

        for i in range(qs):
            data[i] = (c.c_int32 * len(self._fields))()

        self._clib.read_all(self.id, data, c.byref(nElements))

        try:
            assert nElements.value == len(self._fields)
        except AssertionError as err:
            print("Different number of fields read than expected.")
            raise err

        allData = []

        for i in range(qs):
            singleTimeStepData = []
            for j in range(nElements.value):
                singleTimeStepData.append(data[i][j])
            allData.append(dict(zip(self._fields, singleTimeStepData)))

        return allData

    # -----
    # _read_legacy
    # -----
    def _read_legacy(self) -> dict:
        if self._clib.read(self.id, c.byref(self._state)) != self._SUCCESS.value:
            raise RuntimeError("Error: read command failed.")
        # pylint: disable-next=protected-access
        return {f[0]: getattr(self._state, f[0]) for f in self._state._fields_}

    # -----
    # _read
    # -----
    def _read(self) -> dict:
        maxDataElements = self._clib.fxGetMaxDataElements()
        nFields = c.c_int()
        deviceData = (c.c_int32 * maxDataElements)()

        retCode = self._clib.read(self.id, deviceData, c.byref(nFields))

        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not read from device.")

        try:
            assert nFields.value == len(self._fields)
        except AssertionError as err:
            print("Incorrect number of fields read.")
            raise err

        data = [deviceData[i] for i in range(nFields.value)]

        return dict(zip(self._fields, data))

    # -----
    # find_poles
    # -----
    @requires_status("connected")
    @validate
    def find_poles(self) -> int:
        """
        Instructs the device to go through the pole-finding process to
        align the motor correctly.
        """
        if not self.interactive:
            userInput = input(
                "WARNING: You should not use this function unless you know what "
                "you are doing!\nProceed?[y/n] "
            )

            if userInput != "y":
                print("Aborting pole finding.")
                return self._FAILURE.value

        msg = "NOTE: Please wait for the process to complete. The motor will stop "
        msg += "moving when it is done. It usually takes 1-2 minutes to complete."
        msg += "NOTE: Once the pole-finding procedure is completed, you must "
        msg += "power cylce the device for the changes to take effect."
        print(msg)

        return self._clib.fxFindPoles(self.id)

    # -----
    # uvlo - getter
    # -----
    @property
    @requires_status("connected")
    def uvlo(self) -> int:
        """
        Gets the currently set UVLO.
        """
        self._clib.fxRequestUVLO(self.id)
        sleep(5)
        return self._clib.fxGetLastReceivedUVLO(self.id)

    # -----
    # uvlo - setter
    # -----
    @uvlo.setter
    @validate
    def uvlo(self, value: int) -> int:
        """
        Sets the UVLO value for the device. `value` needs to be in milli-volts.
        """
        return self._clib.fxSetUVLO(self.id, value)

    # -----
    # calibrate_imu
    # -----
    @requires_status("connected")
    @validate
    def calibrate_imu(self) -> int:
        """
        Instructs the device to go through the IMU calibration process.
        """
        if not self.interactive:
            userInput = input(
                "WARNING: You should not use this function unless you know what "
                "you are doing!\nProceed?[y/n] "
            )

            if userInput != "y":
                print("Aborting IMU calibration.")
                return self._FAILURE.value

        return self._clib.fxSetImuCalibration(self.id)

    # -----
    # hasHabs
    # -----
    @property
    @requires_status("connected")
    def hasHabs(self) -> bool:
        return self._hasHabs

    # -----
    # name
    # -----
    @property
    @requires_status("connected")
    def name(self) -> str:
        if self._name:
            return self._name
        if self._isLegacy:
            self._name = self._get_legacy_name()
        else:
            self._name = self._get_name()
        return self._name

    # -----
    # _get_name
    # -----
    def _get_name(self) -> str:
        maxDeviceNameLength = self._clib.fxGetMaxDeviceNameLength()
        deviceName = (c.c_char * maxDeviceNameLength)()

        retCode = self._clib.fxGetDeviceTypeNameWrapper(self.id, deviceName)
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not get device name.")

        return deviceName.value.decode("utf8").lower()

    # -----
    # _get_legacy_name
    # -----
    def _get_legacy_name(self) -> str:
        deviceTypeCode = self._clib.fxGetAppType(self.id)

        try:
            devName = fxc.deviceNames[deviceTypeCode]
        except KeyError as err:
            raise RuntimeError("Could not get device name.") from err

        return devName

    # -----
    # side
    # -----
    @property
    @requires_status("connected")
    def side(self) -> str:
        if self._side:
            return self._side
        if self._isLegacy:
            return "undefined"
        maxDeviceSideLength = self._clib.fxGetMaxDeviceSideNameLength()
        deviceSide = (c.c_char * maxDeviceSideLength)()

        retCode = self._clib.fxGetDeviceSideNameWrapper(self.id, deviceSide)
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not get device side.")

        side = deviceSide.value.decode("utf8")

        # If side isn't applicable (for, e.g., an actpack), string is empty
        self._side = side.lower() if side else "undefined"
        return self._side

    # -----
    # _get_lib_version
    # -----
    @minimum_required_version("10.0.0")
    def _get_lib_version(self) -> Version:
        major = c.c_uint16()
        minor = c.c_uint16()
        patch = c.c_uint16()

        returnCode = self._clib.fxGetLibsVersion(
            c.byref(major), c.byref(minor), c.byref(patch)
        )

        if returnCode != self._SUCCESS.value:
            raise RuntimeError("Could not determine c library version.")

        return Version(f"{major.value}.{minor.value}.{patch.value}")

    # -----
    # num_utts
    # -----
    @property
    @minimum_required_version("10.0.0")
    @requires_status("connected")
    def num_utts(self) -> int:
        """
        The number of available UTT values is saved as #define NUM_UTT_VALS
        in the C library, so we have this convenience wrapper to access it.
        """
        return self._clib.fxGetNumUtts()

    # -----
    # set_all_utts
    # -----
    @minimum_required_version("10.0.0")
    @requires_status("connected")
    @validate
    def set_all_utts(self, uttVals: List[int]) -> int:
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
        except AssertionError as err:
            raise ValueError("Error: too many UTT values given.") from err

        data = (c.c_int * nVals)()

        for i in range(nVals):
            data[i] = c.c_int(uttVals[i])

        return self._clib.fxSetUTT(self.id, data, nVals, c.c_byte(-1))

    # -----
    # set_utt
    # -----
    @minimum_required_version("10.0.0")
    @requires_status("connected")
    @validate
    def set_utt(self, uttVal: int, index: int) -> int:
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

        return self._clib.fxSetUTT(self.id, data, numUtts, c.c_byte(index))

    # -----
    # reset_utts
    # -----
    @minimum_required_version("10.0.0")
    @requires_status("connected")
    @validate
    def reset_utts(self) -> int:
        """
        Resets all UTTs to their default values.
        """
        return self._clib.fxSetUTTsToDefault(self.id)

    # -----
    # save_utts
    # -----
    @minimum_required_version("10.0.0")
    @requires_status("connected")
    @validate
    def save_utts(self) -> int:
        """
        Saves the current UTT values to the device's internal memory so
        that they persist across power cycles.
        """
        return self._clib.fxSaveUTTToMemory(self.id)

    # -----
    # read_utts
    # -----
    @minimum_required_version("10.0.0")
    @requires_status("connected")
    def read_utts(self) -> List[int]:
        """
        UTTs are not sent as a part of regular communication, so here we
        first request that the device send the UTTs to Mn, and then we
        read them.
        """
        if self._clib.fxRequestUTT(self.id) != self._SUCCESS.value:
            raise RuntimeError("Error: could not request UTTs.")
        # We have to sleep for a bit in order to allow the device time
        # to fulfill the request
        sleep(0.25)

        numUtts = self.num_utts
        data = (c.c_int * numUtts)()
        retCode = self._clib.fxGetLastReceivedUTT(self.id, data, numUtts)

        if retCode != self._SUCCESS.value:
            raise RuntimeError("Error: could not read UTTs.")

        return [data[i] for i in range(numUtts)]

    # -----
    # gains
    # -----
    @property
    def gains(self) -> dict:
        """
        Returns the currently set gains.
        """
        return self._gains
