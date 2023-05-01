# FlexSEA


`flexsea` is a Python package for interacting with Dephy's wearable robotic devices.
It can be used for gathering data from a device or for writing your own controller.

## Installation

Please see [INSTALL.md](./INSTALL.md) for detailed installation instructions.


## Usage

### Demos

A good reference for what `flexsea` is capable of and how various tasks, such as
controlling the device's motor, can be accomplished, is the collection of demo scripts
that live in the `demos/` directory of the repository. There are currently six demos,
and they should be viewed in order, as each successive demo builds off of the information
presented in the previous one.


### API Overview

#### Importing and Instantiating
The central object in `flexsea` is the `Device` class. For most use cases, this is the
only aspect of `flexsea` that you will need to interact with directly. You can import
it into your code like so:

```python
from flexsea.device import Device
```

The constructor takes five keyword arguments:

```python
class Device(
    port: str="",
    baudRate: int=cfg.baudRate,
    cLibVersion: str=cfg.LTS,
    logLevel: int=4,
    loggingEnabled: bool=True
)
```

* `port`: The name of the serial port that the device is connected to. On Windows, this is typically something akin to `COM3` and on Linux it is usually something like `/dev/ttyACM0`. If you do not provide a value, `flexsea` will scan through all of the available serial ports, stopping at the first valid device that it finds. This means that this keyword is typically only useful if you have more than one device connected at once. However, if you are having trouble connecting to your device, the first thing you should try is specifying the port.
* `baudRate`: The baud rate used for communicating with the device. Most of Dephy's devices all use the same baud rate, which is set as the default value for you.
* `cLibVersion`: Must match your device's firmware, e.g., `9.1.0`. flexsea` is a wrapper around a pre-compiled C library that actually handles all of the heavy lifting of communicating with the device. This parameter allows you to specify the semantic version string of the version of this library that you would like to use. These libraries are stored in a public AWS S3 bucket. If you do not already have the version you specify installed, then `flexsea` will attempt to download it from this bucket for you. By default, the latest LTS version is selected for you.
* `logLevel`: Under the hood, the pre-compiled C library makes use of the [spdlog](https://github.com/gabime/spdlog) logging library. This parameter controls the verbosity of the logs, with `0` being the most verbose and `6` disabling logging all together.
* `loggingEnabled`: If set to `True` then both data and debug logs will be generated (unless `logLevel=6`). If `False`, then no logs are generated, regardless of the value of `logLevel`.

Typically, all you'll need to do to create an instance of the object is:

```python
device = Device(port=YOUR_PORT, cLibVersion=YOUR_VERSION)
```

#### Connecting and Streaming

Once instantiated, you need to establish a connection between the computer and the device. This is done via the `open` method:

```python
device.open()
```

Additionally, if you would like the device to send its data to the computer -- an action called *streaming* -- then you must invoke the `start_streaming` method:

```python
device.start_streaming(frequency)
```

where `frequency` is the rate (in Hertz) at which the device will send data.

**NOTE**: Currently, the maximum supported frequency is 1000Hz (over USB). If you are streaming over bluetooth, the maximum is 100Hz.


#### Reading and Printing

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


#### Controlling the Motor
```python
device.command_motor_current(current) # milliamps
device.command_motor_position(position) # motor ticks
device.command_motor_voltage(voltage) # millivolts
device.command_motor_impedance(position) # motor ticks
device.stop_motor()
device.set_gains(kp, ki, kd, k, b, ff) # See below
```

When setting the gains:

* `kp`: The proportional gain
* `ki`: The integral gain
* `kd`: The differential gain
* `k`: The stiffness gain for impedance control
* `b`: The damping gain for impedance control
* `ff`: The feed-forward gain


#### Device State

You can also introspect certain aspects of the device's state, depending on the firmware version you're running:

* `isOpen` : Indicates whether or not the computer and the device are connected
* `isStreaming`: Indicates whether or not the device is sending data
* `deviceName`: The name of the type of the device, e.g., "actpack"
* `deviceSide`: Either "left" or "right", if applicable; `None` otherwise. **Requires firmware >= v10.0.0**.
* `libsVersion`: The semantic version string of the pre-compiled C library being used. **Requires >= v10.0.0 of the pre-compiled C library**.
* `firmware`: The semantic version string of the firmware version
* `uvlo`: Used to both get and set the device's UVLO in millivolts


#### Cleaning Up

When finished commanding the device, it is good practice to call the `close` method:

```python
device.close()
```

Additionally, when done streaming, you can call the `stop_streaming` method:

```python
device.stop_streaming()
```

**NOTE**: `stop_streaming` is called automatically by `close`, and `close` is called automatically by the `Device` class' destructor, but it's still good practice to clean up manually.
