<div align="center">
    <img src="./assets/dephy_logo.svg">
</div>


FlexSEA is a Python package that provides an API for interacting with [Dephy's](https://dephy.com/) high-performance wearable robotics devices. The purpose of this API is twofold:

* Allow device users to extract valuable information and data from their devices
* Aid in the creation and evaluation of custom augmentation controllers


# Installation


Requirements:

* [Python 3.8+](https://www.python.org/downloads/) 

There are two ways you can install `flexsea`: via `pip` and from source. Regardless of which method you choose, it is **strongly** recommended that you install `flexsea` in a [virtual environment](https://docs.python.org/3/library/venv.html).

## Creating A Virtual Environment

While not necessary, it's a good idea to store all of your virtual environments in one place, as this makes them easier to manage. To this end, we'll first create a directory to hold all of our virtual environments. This directory will be hidden (though it need not be) and it will be called `venvs` (feel free to name it whatever you want, though)

> &#9888;&#65039; If on Windows, you should consider installing the [git for windows](https://gitforwindows.org/) bash terminal in order to execute these commands. Otherwise, you can use the file explorer and Python interpreter. 

```bash
mkdir ~/.venvs
```

Next, we'll create the virtual environment where we'll install `flexsea`. The name of this virtual environment will be `dephy` (feel free to call it whatever you wish, however).

```bash
python3 -m venv ~/.venvs/dephy
```

> &#9888;&#65039; On Linux, using Python 2.x requires the `python2` command and using Python 3.x requires the `python3` command. Windows makes no such distinction, having only the `python` command, so you should check that you're using the right version with `python --version` if on Windows.

The last step is to **activate** the virtual environment via the command

```bash
source ~/.venvs/dephy/bin/activate
```


## Installing With Pip

With your virtual environment activated, run:

```bash
pip3 install flexsea
```

> &#9888;&#65039; Linux employs a `pip2` command to go with `python2` and a `pip3` command to go with `python3`. Windows makes no such distiction, and only has a `pip` command.


## Installing From Source

Requirements:

* [Git](https://git-scm.com/downloads)


Instead of using `pip`, `flexsea` can be installed from source. This is really only necessary if you want access to the bleeding-edge or plan on modifying or developing the package.

To install from source, activate your virtual environment and run:

```bash
git clone https://github.com/DephyInc/Actuator-Package.git
cd Actuator-Package/Python/flexsea
pip3 install .
```

You can, of course, switch to the desired branch or tag before running `pip`.


## ST-Link USB Drivers

While not necessary to *install* `flexsea`, the ST-Link USB drivers are necessary in order to *use* `flexsea`. 

### Linux
On Linux, run:

```bash
sudo apt install libusb-1.0-0 libusb-1.0-0-dev
git clone https://github.com/stlink-org/stlink.git
cd stlink
make clean
make release
cd build/Release
sudo make install
```

### Windows
On Windows, download and install the [STM32 programmer](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-programmers/stm32cubeprog.html), which, as a part of the installation process, will prompt you to install the necessary drivers. The programmer is also used for flashing new firmware onto STM32 devices.


# Usage
`flexsea` has three modules: `device`, `fx_enums`, and `fx_utils`.

## Device

The core component of `flexsea` is the `Device` class, which lives in the `device` module:

```python
from flexsea.device import Device
```

Creating an instance of `Device` requires both a **port** (string) and a **baud rate** (integer):

```python
device = Device("/dev/ttyACM0", 230400)
```

Once instantiated, you can establish a connection to the physical device via the `open` method:

```python
device.open(streaming_frequency)
```

The connection can be severed via the `close` method:

```python
device.close()
```