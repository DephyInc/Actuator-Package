import ctypes as c
from pathlib import Path
import sys
from time import sleep
from typing import List

from semantic_version import Version

import flexsea.utilities.constants as fxc
from flexsea.utilities.decorators import minimum_required_version
from flexsea.utilities.decorators import requires_device_not
from flexsea.utilities.decorators import requires_status
from flexsea.utilities.decorators import training_warn
from flexsea.utilities.decorators import validate
from flexsea.utilities.firmware import decode_firmware
from flexsea.utilities.firmware import validate_given_firmware_version
from flexsea.utilities.library import get_c_library
from flexsea.utilities.library import set_read_functions
from flexsea.utilities.specs import get_device_spec


# ============================================
#                    Device
# ============================================
class Device:
    """
    Representation of one of Dephy's devices. Serves as a way to
    send commands to -- and read data from -- a Dephy device.

    Communication is done through a COM port (either bluetooth or
    serial).

    This class is essentially a Python wrapper around lower-level
    C/C++ code that has been pre-compiled into a shared library.
    These library files are stored on S3 and downloaded lazily.
    They are referenced by a semantic version string specified in
    the ``firmwareVersion`` constructor argument.

    Available versions can be listed with
    :py:func:`flexsea.utilities.firmware.get_available_firmware_versions`

    Parameters
    ----------
    firmwareVersion : str
        Semantic version string of the firmware currently on Manage. Used
        to load the correct pre-compiled C library for communicating with
        the device. If the full version string, e.g., "10.7.0" is not
        given, e.g, "10" or "10.7", the string will be expanded to a
        full version string. If an exact match cannot be found, you
        will be prompted to use the latest version sharing your
        version's major version.

    port : str
        The name of the communication port the device is connected to.
        On Windows, this is usually something akin to ``COM3``. On
        Linux, it is usually something akin to ``/dev/ttyACM0``. On
        Windows, you can use the Device Manager to search for the port
        and on Linux you can use the ``ls`` command on ``/dev/ttyACM*``

    baudRate : int, optional
        The communication rate expected by the device in bauds. The
        default value is 230400, which is the current rate used by
        all Dephy devices.

    libFile : str, optional
        ``flexsea`` serves as a wrapper around pre-compiled C/C++
        libraries. Normally, these libraries are downloaded from S3,
        but in the event that you want to use a custom, local file,
        you can use this argument to specify the path to that file.

    logLevel : int, optional
        Describes the verbosity of the log files created by the
        device. Can be in the range [0,6], with 0 being the most
        verbose and 6 disabling logging.

    interactive : bool, optional
        There are certain scenarios where, if this is set to ``True``,
        you will be prompted for confirmation. If ``False``, you
        will not be prompted and the code will simply proceed.
        This mostly has to do with using a different library version
        than the one specified if an exact match for the specified
        version could not be found. The default value is ``True``.

    debug : bool, optional
        Controls the traceback level. If ``False`` (the default),
        then the traceback limit is set to 0. If ``True``, Python's
        default traceback limit is used.

    s3Timeout : int, optional
        Time, in seconds, spent trying to connect to S3 before an
        exception is raised.

    stopMotorOnDisconnect : bool, optional
        If ``True``, ``stop_motor`` is called by ``close`` (which, in
        turn, is called by the desctructor). If ``False``, ``stop_motor``
        is **not** called by ``close`` or the destructor. The default
        value is ``False``. This is useful for on-device controllers
        (controllers that are baked into the device firmware), so
        that, should the device become disconnected from the computer it
        is streaming data to, the controller will not suddenly shut off
        and cause the wearer to potentially fall. If this is ``True``, you
        must call ``stop_motor`` manually.

    Attributes
    ----------

    connected : bool
        If ``True``, a connection has been established with the device
        over the serial port.

    streaming : bool
        If ``True``, the device is currently sending data at the
        specified rate (:py:attr:`streamingFrequency`)

    port : str
        The value of ``port`` passed to the constructor.

    interactive : bool
        The value of ``interactive`` passed to the constructor.

    firmwareVersion : semantic_version.Version
        The value of ``firmwareVersion`` passed to the constructor.

    libFile : str
        The value of ``libFile`` passed to the constructor.

    baudRate : int
        The value of ``baudRate`` passed to the constructor.

    logLevel : int
        The value of ``logLevel`` passed to the constructor.

    heartbeat : int
        How frequently the device should check for a connection to
        the computer. See: :py:meth:`start_streaming`

    id : int
        The decimal id of the device.

    streamingFrequency : int
        The frequency (in Hz) at which the device is sending data. See:
        :py:meth:`start_streaming`

    bootloaderActive
    firmwareVersion
    uvlo
    hasHabs
    name
    side
    num_utts
    gains
    remaining_training_steps
    success
    failure
    invalidParam
    invalidDevice
    libVersion
    isLegacy


    Examples
    --------
    >>> Device("7.2.0", "COM3")

    >>> Device("10", "/dev/ttyACM0", logLevel=6, interactive=False)
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
        debug: bool = False,
        s3Timeout: int = 60,
        stopMotorOnDisconnect: bool = False,
    ) -> None:
        if not debug:
            sys.tracebacklimit = 0
        fxc.dephyPath.mkdir(parents=True, exist_ok=True)

        self.port: str = port
        self.interactive = interactive
        self._stopMotorOnDisconnect = stopMotorOnDisconnect

        self.firmwareVersion = validate_given_firmware_version(
            firmwareVersion, self.interactive, s3Timeout
        )

        if libFile:
            self.libFile = Path(libFile).expanduser().absolute()
            if not self.libFile.is_file():
                raise FileNotFoundError(f"Could not find library: {self.libFile}")
        else:
            self.libFile = None

        if baudRate <= 0:
            raise ValueError("Error: baud rate must be positive.")
        self.baudRate = baudRate

        if logLevel < 0 or logLevel > 6:
            raise ValueError("Log level must be in [0, 6].")
        self.logLevel = logLevel

        self.heartbeat: int = 0
        self.id: int = 0
        self.streamingFrequency: int = 0

        (self._clib, self.libFile) = get_c_library(
            self.firmwareVersion, self.libFile, s3Timeout
        )

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

        print(f"Using firmware version: {self.firmwareVersion}")
        print(f"Using library file: {self.libFile}")

    # -----
    # open
    # -----
    def open(self, bootloading: bool = False) -> None:
        """
        Establish a connection to a device.

        This is needed in order to send commands to the device and/or
        receive data from the device via serial communication through
        the COM port.

        Parameters
        ----------
        bootloading : bool (optional)
            This keyword is really onlymeant to be used by the
            bootloader and a user of ``flexsea`` should not have to use
            it at all.
            Starting with v12.0.0, a development version number was
            introduced. We can only connect to the device if both the
            firmware version (e.g., 12.0.0) and the development version
            (e.g., 2.0.0) match. If only the firmware version matches,
            we can connect to the device, but not send motor commands,
            only the bootloading command.
        """
        if self.connected:
            print("Already connected.")
            return

        port = self.port.encode("utf-8")

        if bootloading and self.firmwareVersion >= Version("12.0.0"):
            try:
                self.id = self._clib.fxOpenLimited(port)
            except AttributeError as err:
                msg = "Error, unable to connect to device. Your library is missing "
                msg += "the `fxOpenLimited` function."
                raise RuntimeError(msg) from err

        else:
            self.id = self._clib.fxOpen(port, self.baudRate, self.logLevel)

        if self.id in (self._INVALID_DEVICE.value, -1):
            raise RuntimeError("Failed to connect to device.")

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
        Severs connection with device. Does not stop the motor by
        default. To stop the motor on a call to ``close``,

        Will no longer be able to send commands or receive data.
        """
        if self.connected or self.streaming:
            if self._stopMotorOnDisconnect:
                self.stop_motor()
            # fxClose calls fxStopStreaming for us
            retCode = self._clib.fxClose(self.id)

            if retCode != self._SUCCESS.value:
                raise RuntimeError("Failed to close connection.")

    # -----
    # start_streaming
    # -----
    @requires_status("connected")
    def start_streaming(
        self, frequency: int, heartbeat: int = 0, useSafety: bool = False
    ) -> None:
        """
        Instructs the device to send data at the given ``frequency``.

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
            message before shutting itself off (five times ``heartbeat``).

        useSafety : bool, optional
            If ``True``, the device will stop the motor if it doesn't receive
            a heartbeat message in time.

        Raises
        ------
        ValueError
            If ``frequency`` or ``heartbeat`` are invalid.
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
    def stop_streaming(self) -> None:
        """
        Instructs the device to stop sending data.
        """
        retCode = self._clib.fxStopStreaming(self.id)

        if retCode != self._SUCCESS.value:
            raise RuntimeError("Failed to stop streaming.")

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
        returnCode = self._FAILURE
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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
        Activates the bootloader for ``target``.

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
            ``True`` if bootloader is active and ``False`` otherwise.
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
        Puts Manage into tunnel mode.

        All communication goes through Manage, so we need to put it into
        tunnel mode in order to activate the other bootloaders. When bootloading
        Manage itself, this causes it to reboot in DFU mode.

        If bootloading fails for any reason once tunnel mode has been set,
        the device is bricked and must be programmed manually. The exception
        to this rule is Habs.

        Parameters
        ----------
        target : str
            The name of the target to set. Can be: mn, ex, re, habs,
            bt121, or xbee.

        timeout : int, optional
            The number of seconds to wait for confirmation before failing.

        Returns
        -------
        activated : bool
            If ``True``, the bootloader was set successfully. If ``False`` then
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
        """
        Gets data from the data queue.

        Parameters
        ----------
        allData : bool, optional
            If ``False`` (the default), then only the most recent entry
            in the data queue is obtained. If ``True``, then all of the
            data entries in the queue are obtained.

        Returns
        -------
        dict, List[dict]
            If ``allData`` is ``False``, then a dictionary is returned.
            If ``allData`` is ``True``, then a list of dictionaries is
            returned. The dictionaries in each case are keyed by the
            names of the data fields and the values are the values of
            those fields. For firmware versions prior to ``10.0.0``,
            the fields are contained in a device specification file,
            which you can find in ``~/.dephy/legacy_device_spcs``.
            These spec files are downloaded lazily from AWS. For
            firmware versions >= ``10.0.0``, the fields are provided
            by the device itself, which means the list of fields is
            both device and firmware-version dependent.
        """
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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
    @requires_status("connected")
    def get_uvlo(self) -> int:
        """
        Gets the currently set UVLO.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
        """
        self._clib.fxRequestUVLO(self.id)
        sleep(5)
        return self._clib.fxGetLastReceivedUVLO(self.id)

    # -----
    # uvlo - setter
    # -----
    @validate
    def set_uvlo(self, value: int) -> int:
        """
        Sets the UVLO value for the device. `value` needs to be in milli-volts.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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
        """
        Returns whether or not the device has a Habsolute encoder.

        Returns
        -------
        bool
            ``True`` if the device has a Habsolute encoder and
            ``Faslse`` otherwise.
        """
        return self._hasHabs

    # -----
    # name
    # -----
    @property
    @requires_status("connected")
    def name(self) -> str:
        """
        Returns the human-friendly name of the device, e.g., actpack.

        Returns
        -------
        str
            The name of the device.
        """
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
        """
        Returns the chirality of the device.

        Returns
        -------
        str
            Can be 'left', 'right', 'none' (for no chirality), or
            'undefined' (for legacy devices that don't know their side
            information)
        """
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
    @requires_device_not("actpack")
    @minimum_required_version("9.1.0")
    @requires_status("connected")
    def num_utts(self) -> int:
        """
        The number of available UTT values is saved as #define NUM_UTT_VALS
        in the C library, so we have this convenience wrapper to access it.

        Returns
        -------
        int
            The number of User Testing Tweaks (UTTs)
        """
        if self.firmwareVersion.major == 9:
            return fxc.nUttsV9
        return self._clib.fxGetNumUtts()

    # -----
    # set_all_utts
    # -----
    @requires_device_not("actpack")
    @minimum_required_version("9.1.0")
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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
    @requires_device_not("actpack")
    @minimum_required_version("9.1.0")
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

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
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
    @requires_device_not("actpack")
    @minimum_required_version("9.1.0")
    @requires_status("connected")
    @validate
    def reset_utts(self) -> int:
        """
        Resets all UTTs to their default values.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
        """
        return self._clib.fxSetUTTsToDefault(self.id)

    # -----
    # save_utts
    # -----
    @requires_device_not("actpack")
    @minimum_required_version("9.1.0")
    @requires_status("connected")
    @validate
    def save_utts(self) -> int:
        """
        Saves the current UTT values to the device's internal memory so
        that they persist across power cycles.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`
        """
        return self._clib.fxSaveUTTToMemory(self.id)

    # -----
    # read_utts
    # -----
    @requires_device_not("actpack")
    @minimum_required_version("9.1.0")
    @requires_status("connected")
    def read_utts(self) -> List[int]:
        """
        UTTs are not sent as a part of regular communication, so here we
        first request that the device send the UTTs to Mn, and then we
        read them.

        Returns
        -------
        List[int]
            The current value of each UTT.
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

        Returns
        -------
        dict
            The names and values of each gain.
        """
        return self._gains

    # -----
    # start_training
    # -----
    @validate
    @requires_device_not("actpack")
    @requires_status("connected")
    def start_training(self) -> int:
        """
        Activates training mode.

        When in training mode, the user must take a certain number of
        steps. This allows the device to learn the user's gait and set
        the value of several parameters accordingly in order for the
        device to provide optimal augmentation.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`

        Notes
        -----
        Training mode is only available if the device is flashed with
        one of Dephy's controllers.
        """
        self._update_training_data()
        sleep(0.25)
        return self._clib.fxStartTraining(self.id)

    # -----
    # activate_single_user_mode
    # -----
    @validate
    @requires_device_not("actpack")
    @requires_status("connected")
    def activate_single_user_mode(self) -> int:
        """
        Puts the device into single-user mode.

        In this mode, training mode runs once and then the parameters
        are saved. This means that training mode will not re-activate
        if the device is power-cycled, so the same gait parameters will
        be used across sessions.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`

        Notes
        -----
        Training mode is only available if the device is flashed with
        one of Dephy's controllers.
        """
        self._update_training_data()
        sleep(0.25)
        return self._clib.fxUseSavedTraining(self.id)

    # -----
    # activate_multi_user_mode
    # -----
    @validate
    @requires_device_not("actpack")
    @requires_status("connected")
    def activate_multi_user_mode(self) -> int:
        """
        Puts the device into multi-user mode.

        This causes training mode to activate each time the device is
        power-cycled, so gait parameters do not persist across power
        cycles.

        Returns
        -------
        int
            Status code indicating success or failure.

        See Also
        --------
        :py:func:`success`
        :py:func:`failure`

        Notes
        -----
        Training mode is only available if the device is flashed with
        one of Dephy's controllers.
        """
        self._update_training_data()
        sleep(0.25)
        return self._clib.fxDoNotUseSaveTraining(self.id)

    # -----
    # remaining_training_steps
    # -----
    @property
    @requires_device_not("actpack")
    @requires_status("connected")
    def remaining_training_steps(self) -> int:
        """
        Returns the number of steps remaining before training is
        completed.

        Returns
        -------
        int
            The number of steps remaining before training is complete.

        Notes
        -----
        Training mode is only available if the device is flashed with
        one of Dephy's controllers.
        """
        self._update_training_data()
        # Give the device time to process the request and send the data
        sleep(0.25)
        stepsRemaining = c.c_int()
        retCode = self._clib.fxGetStepsRemaining(self.id, c.byref(stepsRemaining))
        if retCode != self._SUCCESS.value:
            raise RuntimeError(
                "Error: could not determine how many training steps remain."
            )
        return stepsRemaining.value

    # -----
    # get_training_user_mode
    # -----
    @requires_device_not("actpack")
    @requires_status("connected")
    def get_training_user_mode(self) -> str:
        """
        Returns the current mode the device is in: either single-user
        or multi-user.

        Returns
        -------
        str
            The device's current mode.

        See Also
        --------
        :py:meth:`activate_multi_user_mode`
        :py:meth:`activate_single_user_mode`

        Notes
        -----
        Training mode is only available if the device is flashed with
        one of Dephy's controllers.
        """
        self._update_training_data()
        sleep(1)

        singleUserMode = c.c_bool()

        retCode = self._clib.fxIsUsingSavedTrainingData(
            self.id, c.byref(singleUserMode)
        )

        if retCode != self._SUCCESS.value:
            raise RuntimeError("Error: could not determine training mode.")

        if singleUserMode.value:
            return "single"
        return "multi"

    # -----
    # get_training_state
    # -----
    @requires_device_not("actpack")
    @requires_status("connected")
    def get_training_state(self) -> str:
        """
        Returns the current status of training.

        Can be: ``loading``, ``in_progress``, ``done``,
        ``walk_training_in_progress``, or ``run_training_in_progress``.

        Returns
        -------
        str
            Status of training.

        Notes
        -----
        Training mode is only available if the device is flashed with
        one of Dephy's controllers.
        """
        self._update_training_data()
        # Give the device time to process the request and send the data
        sleep(0.25)
        trainingState = c.c_int()
        retCode = self._clib.fxGetTrainingState(self.id, c.byref(trainingState))
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Error: could not determine training state.")
        return fxc.training_states[trainingState.value]

    # -----
    # _update_training_data
    # -----
    @training_warn
    @validate
    def _update_training_data(self) -> None:
        return self._clib.fxUpdateTrainingData(self.id)

    # -----
    # success
    # -----
    @property
    def success(self) -> int:
        """
        The integer corresponding to a status code of success.

        Returns
        -------
        int
            The integer corresponding to a status code of success.
        """
        return self._SUCCESS.value

    # -----
    # failure
    # -----
    @property
    def failure(self) -> int:
        """
        The integer corresponding to a status code of failure.

        Returns
        -------
        int
            The integer corresponding to a status code of failure.
        """
        return self._FAILURE.value

    # -----
    # undefined
    # -----
    @property
    @minimum_required_version("10.0.0")
    def undefined(self) -> int:
        """
        The integer corresponding to a status code of undefined.

        Returns
        -------
        int
            The integer corresponding to a status code of undefined.
        """
        return self._UNDEFINED.value

    # -----
    # invalidParam
    # -----
    @property
    def invalidParam(self) -> int:
        """
        The integer corresponding to a status code of invalidParam.

        Returns
        -------
        int
            The integer corresponding to a status code of invalidParam.
        """
        return self._INVALID_PARAM.value

    # -----
    # invalidDevice
    # -----
    @property
    def invalidDevice(self) -> int:
        """
        The integer corresponding to a status code of invalidDevice.

        Returns
        -------
        int
            The integer corresponding to a status code of invalidDevice.
        """
        return self._INVALID_DEVICE.value

    # -----
    # isLegacy
    # -----
    @property
    def isLegacy(self) -> bool:
        """
        Whether or not the device is a legacy device.

        Returns
        -------
        bool
            Whether or not the device is a legacy device.
        """
        return self._isLegacy

    # -----
    # libVersion
    # -----
    @property
    def libVersion(self) -> str:
        """
        Version string of the currently loaded library.

        Returns
        -------
        str
            Version string of the currently loaded library.
        """
        return self._libVersion

    # -----
    # log files
    # -----

    @minimum_required_version("12.0.0")
    @requires_status("connected")
    def set_file_name(self, name) -> None:
        """
        Sets the name of the log file

        Parameters
        ----------
        name : string
            The desired name of the log file
        """
        return self._clib.fxSetDataLogName(name.encode("utf-8"), self.id)

    @minimum_required_version("12.0.0")
    @requires_status("connected")
    def set_file_size(self, size) -> None:
        """
        Sets the size of the log file

        Parameters
        ----------
        size: int
            The desired name of the log file
        """
        return self._clib.fxSetLogFileSize(size, self.id)

    @minimum_required_version("12.0.0")
    @requires_status("connected")
    def set_log_directory(self, path) -> None:
        """
        Sets the log directory

        Parameters
        ----------
        path: string
            The desired path for the log files
        """
        return self._clib.fxSetLogDirectory(path.encode("utf-8"), self.id)

    # -----
    # connected
    # -----
    @property
    def connected(self) -> bool:
        return self._clib.fxIsOpen(self.id)

    # -----
    # streaming
    # -----
    @property
    def streaming(self) -> bool:
        if self.connected:
            return self._clib.fxIsStreaming(self.id)
        return False

    # -----
    # request_re_config_settings
    # -----
    @minimum_required_version("13.0.0")
    @validate
    def _request_re_config_settings(self) -> int:
        return self._clib.fxRequestRegulateConfigSettings(self.id)

    # -----
    # battery_type
    # -----
    @minimum_required_version("13.0.0")
    def get_battery_type(self) -> str:
        self._request_re_config_settings()
        sleep(1)
        batteryType = c.c_int()
        retCode = self._clib.fxGetBatteryType(self.id, c.byref(batteryType))
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not read battery type.")
        return fxc.batteryTypes[batteryType.value]

    # -----
    # battery_type - setter
    # -----
    @minimum_required_version("13.0.0")
    @validate
    def set_battery_type(self, batteryType: int | c.c_int) -> None:
        if isinstance(batteryType, c.c_int):
            batteryType = batteryType.value
        if batteryType not in fxc.batteryTypes:
            raise ValueError(f"Error: invalid battery type {batteryType}")
        self._request_re_config_settings()
        sleep(1)
        batteryType = c.c_int(batteryType)
        return self._clib.fxSetBatteryType(self.id, batteryType)

    # -----
    # running_led_sequence
    # -----
    @minimum_required_version("13.0.0")
    def get_running_led_sequence(self) -> str:
        self._request_re_config_settings()
        sleep(1)
        ledSequence = c.c_int()
        retCode = self._clib.fxGetRunningLEDSequence(self.id, c.byref(ledSequence))
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not read running led sequence.")
        return fxc.ledSequences[ledSequence.value]

    # -----
    # init_led_sequence
    # -----
    @minimum_required_version("13.0.0")
    def get_init_led_sequence(self) -> str:
        self._request_re_config_settings()
        sleep(1)
        ledSequence = c.c_int()
        retCode = self._clib.fxGetInitLEDSequence(self.id, c.byref(ledSequence))
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not read init led sequence.")
        return fxc.ledSequences[ledSequence.value]

    # -----
    # init_led_sequence - setter
    # -----
    @minimum_required_version("13.0.0")
    @validate
    def set_init_led_sequence(self, ledSequence: int | c.c_int) -> None:
        if isinstance(ledSequence, c.c_int):
            ledSequence = ledSequence.value
        if ledSequence not in fxc.ledSequences:
            raise ValueError(f"Error: invalid led sequence {ledSequence}")
        self._request_re_config_settings()
        sleep(1)
        ledSequence = c.c_int(ledSequence)
        return self._clib.fxSetInitLEDSequence(self.id, ledSequence)

    # -----
    # shutoff_led_sequence
    # -----
    @minimum_required_version("13.0.0")
    def get_shutoff_led_sequence(self) -> str:
        self._request_re_config_settings()
        sleep(1)
        ledSequence = c.c_int()
        retCode = self._clib.fxGetShutoffLEDSequence(self.id, c.byref(ledSequence))
        if retCode != self._SUCCESS.value:
            raise RuntimeError("Could not read shutoff led sequence.")
        return fxc.ledSequences[ledSequence.value]

    # -----
    # shutoff_led_sequence - setter
    # -----
    @minimum_required_version("13.0.0")
    @validate
    def set_shutoff_led_sequence(self, ledSequence: int | c.c_int) -> None:
        if isinstance(ledSequence, c.c_int):
            ledSequence = ledSequence.value
        if ledSequence not in fxc.ledSequences:
            raise ValueError(f"Error: invalid ledSequence type {ledSequence}")
        self._request_re_config_settings()
        sleep(1)
        ledSequence = c.c_int(ledSequence)
        return self._clib.fxSetShutoffLEDSequence(self.id, ledSequence)
