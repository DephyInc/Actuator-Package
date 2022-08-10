# Dephy FlexSEA Library

Use this library to work with Dephy's high performance actuators and exoskeletons.

More information at https://dephy.com/faster

## Usage

You can use the `flexsea` library in your code as follows:

```python
from flexsea.device import Device

device = Device(port, buad_rate)
device.open()
device.start_streaming(frequency)
```

See the sample scripts in `flexsea_demo` for reference in [this repo](https://github.com/DephyInc/Actuator-Package/tree/master/Python).

## Build Package

If you are developing this package (instead of using it for your own script). Follow these steps to build it.

This can be run in a virtual environement if needed.

```bash
# Install build dependencies
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools wheel twine
# Build package
python3 setup.py bdist_wheel
# this generates a .whl file that can be installed in your working venv
```

In your working virtual environment
```bash
# Install the generated package from the local file
python3 -m pip install dist/flexsea-5.0.0-py3-none-any.whl  #replace the version if needed
```

## Publish
Once the package is ready to publish and the version has been updated. Run this to upload it to PyPi to allow users to install it via `pip`.

See [these instructions](https://packaging.python.org/tutorials/packaging-projects/) in case you need to get a PyPi account or token.

### Test Upload
Upload to test server
```bash
python3 -m twine upload --repository testpypi dist/*
```
Install from test server
```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps flexsea
```

### Final upload
```bash
python3 -m twine upload dist/*
```

## Heartbeat
When the device is streaming data to the computer, the computer will routinely send
a special message, called a heartbeat, to the device. This message lets the device
know that the connection between it and the computer is still alive.

The frequency of these heartbeat messages can be specified when calling `start_streaming`:

```python
device = Device(port, baud_rate)
device.open()
device.start_streaming(frequency, heartbeat_period=100)
```

The time given for `heartbeat_period` is in **milliseconds**. One thing to note is that
if it's too fast, the message won't have time to properly send before the device shuts
off due to not receiving the message. It also must be smaller than the streaming
frequency. If no value is given for `heartbeat_period`, it defaults to 4 seconds.

The time that the device will wait without receiving a message before shutting off is
5 times `heartbeat_period` milliseconds.
