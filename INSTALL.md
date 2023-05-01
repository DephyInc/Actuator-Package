# Prerequisites

## Ubuntu
First, update your system

```bash
sudo apt update && sudo apt upgrade
```

Then install the prerequisites 

```bash
sudo apt install git cmake build-essential
```

Then the following USB libraries

```bash
sudo apt install libusb-1.0-0 libusb-1.0-0-dev
```

The `stlink` tools:


```bash
git clone https://github.com/stlink-org/stlink.git 
cd stlink
make clean
make release
cd build/Release
sudo make install
```

Then install Python. `flexsea` requires `python >= 3.11`. You can either install a pre-compiled version from [here](https://www.python.org/downloads/)or run the following to build it from source

```bash
 # Python dependencies
 sudo apt-get install build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev

# Clone the python repo
git clone https://github.com/python/cpython.git 
cd cypthon/

# Switch to the version you want to build
git checkout v3.11.3 

# Build
./configure --enable-optimizations --prefix=/path/to/where/you/want/it/installed
make
make test 
sudo make install
```

You can then either add this location to your `$PATH` environment variable, alias it, or use it by invoking the full path.

Lastly, you need to add your user to the `dialout` group in order to interact with serial ports. Serial communication is how `flexsea` talks with the device.

```bash
sudo usermod -a -G dialout "$USER"
```

**NOTE**: In order for the group changes to take effect, you must reboot your system. Logging out and back in is not enough.

### Raspberry Pi
In addition to the above steps, if you're installing on a Raspberry Pi, you'll also need the atlas library in order for `numpy` (needed for the demos, not `flexsea` itself) to work correctly:

```bash
sudo apt install libatlas-base-dev
```

## Windows 

On Windows, you should first install [Git for Windows](https://git-scm.com/download/win). Make sure you download the version that matches your system (most likely 64 bit).

Next, you'll need to install [Python 3.11](https://www.python.org/downloads/windows/) **NOTE** Make sure you download the 64-bit version if you downloaded the 64-bit Git above and the 32-bit version if you installed the 32-bit Git above. **NOTE**: When going through the installation wizard, make sure you check the box that adds Python to your PATH.


# Installation
**NOTE**: These instructions use the `python3` executable. If you are on Windows, you
will need to replace `python3` -> `python`.

It is **strongly** recommended that you install `flexsea` in a [virtual environment](https://docs.python.org/3/library/venv.html).

```bash
mkdir ~/.venvs
python3 -m venv ~/.venvs/dephy
source ~/.venvs/dephy/bin/activate # On Windows: source ~/.venvs/dephy/Scripts/activate
```

**NOTE**: You'll need to either manually re-run the above `source` command each time you open a new terminal or you can add that command to your profile to have it execute automatically.

To leave a virtual environment:

```bash
deactivate
```


### Installing with Pip

```bash
python3 -m pip install flexsea
```


### From Source
```bash
git clone https://github.com/DephyInc/Actuator-Package.git
cd Actuator-Package/
git checkout v10.1.9 # Or the branch you want
python3 -m pip install .
```

### Development tools

To develop flexsea, we strongly recommend installing [Poetry](https://python-poetry.org/docs/):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Activate the development environment and install dependencies
```bash
poetry shell
poetry install
```
