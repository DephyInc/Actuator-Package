### constructor
```python
__init__(
    self,
    firmwareVersion: str,
    port: str,
    baudRate: int = fxc.baudRate,
    libFile: str = "",
    logLevel: int = 4,
    interactive: bool = True,
) -> None
```

Instantiates the `Device` class.

#### Parameters 
`firmwareVersion` : `str` 
    The semantic version string of the firmware currently on Manage, e.g., "9.1.0". You can also pass just a major version, e.g., "9", and `flexsea` will find and use the latest version within that major version for you.

`port` : `str` 
    The name of the serial communication port the device is connected to. On Windows this is usually something along the lines of `COM3` and on linux it is usually something along the lines of `/dev/ttyACM0`.

`baudRate` : `int` 
    The baud rate for communicating with the device. You should ideally never have to change this manually.

`libFile` : `str` 
    Manually specify the C library to use for communicating with the device. This overrides `firmwareVersion`. Most users will never need this option.

`logLevel` : `int` 
    An integer from [0,6]. 0 Is the most verbose and 6 disables logging

`interactive` : `bool` 
    If `True`, `flexsea` will occasionally prompt you to answer a question or confirm information. If you don't want this, you can set it to `False`


### open
```python
open(self) -> None
```

Establishes a connection to a device. This is needed in order
to send commands to the device and/or receive data from the
device.


### close
```python
close(self) -> None
```

Severs connection with device. Will no longer be able to send
commands or receive data.


### start streaming
```python
def start_streaming(
    self, frequency: int, heartbeat: int = 0, useSafety: bool = False
) -> None
```

Instructs the device to send us data at the given `frequency`.

#### Parameters
`frequency` : `int`
    The number of times per second the device should send data

`heartbeat : `int``
    When streaming, the computer periodically sends a message to
    the device to let it know that the connection between them
    is still alive. These are called heartbeat messages. This
    variable specifies the amount of time (in milliseconds)
    between successive heartbeat messages. This is related to
    how long the device will wait without receiving a heartbeat
    message before shutting itself off (five times `heartbeat`).

`useSafety` : `bool`
    If `True`, the device will stop the motor if it doesn't receive
    a heartbeat message in time.

#### Raises
`ValueError`
    If `frequency` or `heartbeat` are invalid.


### stop streaming
```python
def stop_streaming(self) -> int
```

Instructs the device to stop sending data.


### set gains
```python
def set_gains(self, kp: int, ki: int, kd: int, k: int, b: int, ff: int) -> None
```

Sets the gains used by PID controllers on the device.

#### Parameters
`kp` : `int`
    Proportional gain.

`ki` : `int`
    Integral gain.

`kd` : `int`
    Differential gain.

`k` : `int`
    Stiffness (used in impedence control only).

`b` : `int`
    Damping (used in impedance control only).

`ff` : `int`
    Feed forward gain.


### command motor position
```python
def command_motor_position(self, value: int) -> int
```

Sets motor to given position.

#### Parameters
`value` : `int`
    Desired motor position in encoder units.


### command motor current
```python
def command_motor_current(self, value: int) -> int
```

Sends the given current to the motor.

#### Parameters
`value` : `int`
    Desired motor current in milli-Amps.


### command motor voltage
```python
def command_motor_voltage(self, value: int) -> int
```

Sets motor's voltage.

#### Parameters
`value` : `int`
    Desired motor voltage in milli-volts.


### command motor impedance
```python
def command_motor_impedance(self, value: int) -> int
```

Has the motor simulate a stretched from current position to
the desired position using the damping gain b and stiffness
gain k.

#### Parameters
`value` : `int`
    Desired motor position in ticks.


### stop motor
```python
def stop_motor(self) -> int
```

Stops the motor and resets the gains to zero.


### activate bootloader
```python
def activate_bootloader(self, target: str) -> None
```

Activates the bootloader for `target`.

#### Parameters
`target` : `str`
    Bootloader target. Can be: mn, ex, re, or habs.


### bootloaderActive
```python
def bootloaderActive(self) -> bool
```

Returns whether or not the bootloader is active or not.

#### Returns
`bool`
    `True` if bootloader is active and `False` otherwise.


### set tunnel mode
```python
def set_tunnel_mode(self, target: str, timeout: int = 30) -> bool
```

All communication goes through Manage, so we need to put it into
tunnel mode in order to activate the other bootloaders. When bootloading
Manage itself, this causes it to reboot in DFU mode.

If bootloading fails for any reason once tunnel mode has been set,
the device is bricked and must be programmed manually. The exception
to this rule is Habs.

#### Parameters
`target` : `str`
    The name of the target to set (abbreviated).

`timeout` : `int`
    The number of seconds to wait for confirmation before failing.

#### Returns
`activated` : `bool`
    If `True`, the bootloader was set successfully. If `False` then
    something went wrong.


### firmware version
```python
def firmware_version(self) -> dict
```

Gets the fimware versions of device's MCUs.

#### Returns
`Dict`
    A dictionary with the semantic version strings of manage,
    execute, and regulate's firmware. And habs, if applicable.


### print
```python
def print(self, data: dict | None = None) -> None
```

Reads the data from the device and then prints it to the screen.
If data is given, we print that instead.


### read
python```
def read(self, allData: bool = False) -> dict | List[dict]
```

Instructs the device to send its queued data to the computer.

#### Parameters
`allData` : `bool`
    If `False`, only the most recent data is obtained from the device. If `True`, then all of the queued data is read from the device.

#### Returns 
`dict`
    If `allData=False`. The exact fields contained in the dictionary depend on the device type and the firmware version.

`List[dict]`
    If `allData=True`. This is a list of dictionaries as described above.


### find poles
```python
def find_poles(self) -> int
```

Instructs the device to go through the pole-finding process to
align the motor correctly.


### uvlo
```python
@property
def uvlo(self) -> int
```
Gets the currently set UVLO. You can also use this as a setter to change the UVLO.


### calibrate imu
```python
def calibrate_imu(self) -> int
```

Instructs the device to go through the IMU calibration process.


### hasHabs
```python
@property
def hasHabs(self) -> bool
```

Returns whether or not the current device is equipped with a habsolute encoder
by default.

#### Returns
`bool`
    Whether or not the current device has a habsolute encoder by default.


### name
```python
@property
def name(self) -> str
```

Returns the name of the current device, e.g., "actpack".

#### Returns
`str`
    The name of the current device.


### side
```python
@property
def side(self) -> str
```

If the device has chirality, this property returns whether the current device is
a left or right device. If the device is not chiral or does not have a side defined,
it returns 'undefined'.

#### Returns
`str`
Either 'left', 'right', or 'undefined'.


### num utts
```python
@property
@minimum_required_version("10.0.0")
def num_utts(self) -> int
```

The number of available UTT values is saved as #define NUM_UTT_VALS
in the C library, so we have this convenience wrapper to access it, since
`ctypes` cannot read macros.

#### Returns
`int`
The number of UTTs that can be set.


### set all utts
```python
@minimum_required_version("10.0.0")
def set_all_utts(self, uttVals: List[int]) -> int
```

Takes in a list of integer values and assigns each one to a UTT
value.

#### Parameters
`uttVals` : `List[int]`
    List of values, one for each UTT

#### Returns
`int`
An integer indicating whether or not the call was successful. See `self._SUCCESS` and
`self._FAILURE`.


### set utt
```python
@minimum_required_version("10.0.0")
def set_utt(self, uttVal: int, index: int) -> int
```

Sets the value of a single UTT.

#### Parameters
`uttVal` : `int`
    The value the desired UTT will be set to

`index` : `int`
    The array index for the desired UTT

#### Returns
`int`
An integer indicating whether or not the call was successful. See `self._SUCCESS` and
`self._FAILURE`.


### reset utts
```python
@minimum_required_version("10.0.0")
def reset_utts(self) -> int
```

Resets all UTTs to their default values.

#### Returns
`int`
An integer indicating whether or not the call was successful. See `self._SUCCESS` and
`self._FAILURE`.


### save utts
```python
@minimum_required_version("10.0.0")
def save_utts(self) -> int
```

Saves the current UTT values to the device's internal memory so
that they persist across power cycles.

#### Returns
`int`
An integer indicating whether or not the call was successful. See `self._SUCCESS` and
`self._FAILURE`.


### read utts
```python
@minimum_required_version("10.0.0")
def read_utts(self) -> List[int]
```

UTTs are not sent as a part of regular communication, so here we
first request that the device send the UTTs to Mn, and then we
read them.

#### Returns
`int`
An integer indicating whether or not the call was successful. See `self._SUCCESS` and
`self._FAILURE`.


### gains
```python
@property
def gains(self) -> dict
```

Returns the currently set gains.

#### Returns
`dict`
A dictionary of the currently set gains.
