# Quickstart


## Instantiating
The central object in `flexsea` is the `Device` class. For most use cases, this is the
only aspect of `flexsea` that you will need to interact with directly. You can import
it into your code like so:

```python
from flexsea.device import Device
```

The constructor takes six arguments:

```python
class Device(
    firmwareVersion: str,
    port: str,
    baudRate: int=cfg.baudRate,
    libFile: str="",
    logLevel: int=4,
    interactive: bool=True
)
```

See the [api documentation](./api.md) for more details.

Typically, all you'll need to do to create an instance of the object is:

```python
device = Device(port=YOUR_PORT, firmwareVersion=YOUR_VERSION)
```

On Windows, `YOUR_PORT` will typically be something along the lines of `COM3`. You can 
determine which port your device is on by navigating to the Device Manager -> Ports (COM & LPT).

On Linux (Ubuntu and Raspberry Pi), the port will typically be something along the lines of 
`/dev/ttyACM0`. You can check by using `ls /dev/ttyACM*` before connecting the device's USB 
cable and then after connecting the device's USB cable. The port will be the difference between 
the two outputs.

The value of `YOUR_VERSION` should be either the full semantic version string of the 
firmware that's currently on your device or the major version of the firmware that's 
on your device, e.g., "10.5.0" or "10".

To see what versions are available, you can do:
```python
from flexsea.utilities.firmware import get_available_firmware_versions

get_available_firmware_versions()
```

## Connecting and Streaming

Once instantiated, you need to establish a connection between the computer and the device. This is done via the `open` method:

```python
device.open()
```

Additionally, if you would like the device to send its data to the computer -- an action called *streaming* -- then you must invoke the `start_streaming` method:

```python
device.start_streaming(frequency)
```

where `frequency` is the rate (in Hertz) at which the device will send data.

**NOTE**: The maximum supported frequency is 1000Hz (over USB). If you are streaming over bluetooth, the maximum is 100Hz.


## Reading and Printing

If you are streaming, you can get the most recent device data from the `read` method:

```python
data = device.read()
```

Where `data` is a dictionary. The available fields depend on the type of device as well as the firmware version. If you have not read from the device in a while, you can get all of the data that's currently in the device's internal queue by using the `allData` keyword:

```python
allData = device.read(allData=True)
```

In this case, the return value `allData` will be a list of dictionaries, one for each time stamp.

To conveniently display the most recent data:

```python
device.print()
```

`print` takes an optional keyword argument called `data`, which should be a dictionary returned by `read`. This lets you display data that was read at some arbitrary point in the past.


## Logging

Logging is enabled by default, and the verbosity of the logs is controlled by the `logLevel`
argument in the `Device` constructor. The allowed values are integers [0,6], with 0 
being the most verbose and 6 disabling logging.

There are two kinds of logs: debug logs and data logs.

Debug logs are saved in a directory called `DebugLog` in the directory from which
`flexsea` is being run. The files contained inside are generally only useful if you are 
trying to troubleshoot an issue, as they contain information related to communication
procedures and motor command messages.

Data logs are saved in a directory called `DataLog` in the directory from which
`flexsea` is being run. The files contained inside are csv files with all of the data
streamed by the device to the computer during your run. If your session was long (or 
streaming rate high) your data will be broken up into several different files in order 
to prevent any one file from getting too large. Only the first file will have the 
column headings.


## Controlling the Motor
```python
device.command_motor_current(current) # milliamps
device.command_motor_position(position) # motor ticks
device.command_motor_voltage(voltage) # millivolts
device.command_motor_impedance(position) # motor ticks
device.stop_motor()
device.set_gains(kp, ki, kd, k, b, ff) # See below
```

**NOTE**: The `stop_motor` method resets all of the gains to 0 as a safety precaution.

When setting the gains:

* `kp`: The proportional gain
* `ki`: The integral gain
* `kd`: The differential gain
* `k`: The stiffness gain for impedance control
* `b`: The damping gain for impedance control
* `ff`: The feed-forward gain


## Device State

You can also introspect certain aspects of the device's state, depending on the firmware version you're running:

* `connected` : Indicates whether or not the computer and the device are connected
* `streaming`: Indicates whether or not the device is sending data
* `name`: The name of the type of the device, e.g., "actpack"
* `side`: Either "left" or "right", if applicable; `None` otherwise. **Requires firmware >= v10.0.0**.
* `uvlo`: Used to both get and set the device's UVLO in millivolts
* `gains`: The currently set gains
* `utts`: The currently set UTT values (see [here](./api.md))
* `hasHabs`: Whether or not the current device has a habsolute encoder


## Cleaning Up

When finished commanding the device, it is good practice to call the `close` method:

```python
device.close()
```

Additionally, when done streaming, you can call the `stop_streaming` method:

```python
device.stop_streaming()
```

**NOTE**: `stop_streaming` is called automatically by `close`, and `close` is called automatically by the `Device` class' destructor, but it's still good practice to clean up manually.
