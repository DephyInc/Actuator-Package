# Installing on Raspberry Pi


## Prerequisites


The following script will:

* Update your system
* Install the linux USB libraries
* Install the `atlas` library, which is necessary for `numpy` to work
* Add your current user to the `dialout` group (needed for serial communication)

**NOTE**: You must reboot your machine after adding your user to the `dialout` group 
in order for the changes to take effect. Logging out and back in is not enough.


```bash
sudo apt update && sudo apt upgrade
sudo apt install libusb-1.0-0 libusb-1.0-0-dev
sudo apt install libatlas-base-dev
sudo usermod -a -G dialout "$USER"
```


### Python

`flexsea` requires `python >= 3.11`. As of this writing, there is no pre-compiled version
of 3.11 for the pi, which means you will have to build Python from source.

#### Installing from Source

The following script will:
* Download all of the dependencies for Python (this list is current as of Python 3.11.3.
If you are building a later version, it's possible that this list has changed. Please
see [this](https://devguide.python.org/getting-started/setup-building/#build-dependencies)
link for the most up to date dependencies)
* Download the Python source code
* Build, test, and install Python (this can take a while)

```bash
 # Python dependencies
 sudo apt install build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev

# Clone the python repo
git clone https://github.com/python/cpython.git
cd cypthon/

# Switch to the version you want to build
git checkout v3.11.3

# Build (change the prefix path to install to a different location)
mkdir -p $HOME/.local
./configure --enable-optimizations --prefix=$HOME/.local
make
make test
sudo make install
```

Now create a virtual environment:
```bash
mkdir -p $HOME/.venvs
# Replace $HOME/.local with the prefix path you used during configuration
$HOME/.local/bin/python3.11 -m venv $HOME/.venvs/dephy
source $HOME/.venvs/dephy/bin/activate
```

You will need to run the above `source` command each time you create a new terminal.


## Installing

There are two options to install `flexsea`:
* With `pip`

### Installing with Pip
```bash
python3 -m pip install flexsea
```

## Developing

To develop `flexsea`, we strongly recommend installing [Poetry](https://python-poetry.org/docs/):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Activate the development environment and install the dependencies for `flexsea`:
```bash
poetry shell
poetry install
```
