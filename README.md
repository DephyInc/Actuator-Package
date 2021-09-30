# Actuator-Package

The Dephy Actuator Package is a turn-key solution for people who want to test FlexSEA's capabilities or quickly design a prosthetic limb. The Package consists of a custom brushless motor integrated with a FlexSEA-Rigid circuit and a minimalist enclosure, pre-loaded embedded software, and a full suite of high-level software and test scripts.

## Important: Compatibility

⚠️ Not using compatible firmware will result in segmentation faults or unexpected behavior.

Make sure the Actuator Package repository or flexsea Python package major version matches the major version of the ActPack firmware. This is in accordance with [semantic versioning](https://semver.org/).

For instance, the flexsea package 6.0.3 is compatible with firmware 6.0 but not with firmware 5.1.

## Scripts

The fx_plan_stack API is a suite of functions that configure and control FlexSEA devices. See the [full documentation](#UPDATE_THIS) for more information.

The repo contains the FlexSEA-Rigid Actuator Package library `flexsea` and sample programs for C/C++, Python, MATLAB and SIMULINK. These scripts are accompanied by and are dependent on pre-compiled libraries for Windows (.dll) or Linux(.so).

## Install Python

### Linux

Run this script to install the python dependencies before running the python scripts
```bash
./install_python_deps.sh
```

If choose to install Python manyually, make sure to add the current user to the `dialout` group so it can access serial ports.

```bash
sudo usermod -a -G dialout "$USER"
```

### Windows 10

1. On Windows, download [Python 3.9](https://www.python.org/downloads/) and install it.
2. Note which architecture you download (32 or 64 bits) and use the matching [git shell](https://git-scm.com/download/win).
3. Install [MinGW](https://sourceforge.net/projects/mingw-w64/) select the matching the matchin arhcitecture in the installer. Make sure MinGW gets added to your Path variable.

Then, install the required Python environment using using ___PowerShell___ or __gitbash__:

### Install FlexSEA Library

```bash
# Define your own virtual environment
# this is not required but it helps keeping your environment clean
#	In Windows:
	python -m pip install --upgrade pip
	python -m pip install virtualenv
	python -m virtualenv actpack --python=python3.9
#	In Linux and RasberryPi systems:
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	python3 -m virtualenv actpack --python=/usr/bin/python3.9
	sudo apt install libc6 libgcc-s1 -y
# Activate your virtualenv
#	On Windows (PowerShell):
	actpack/Scripts/activate.ps1
#	On other shells:
	actpack/bin/activate
# Once the environment is activated, install the package
#	On Windows:
	python -m pip install --upgrade pip
	python -m pip install flexsea
#	On Other OS:
	python3 -m pip install --upgrade pip
	python3 -m pip install flexsea

# Run your script that uses flexsea
# Once you want to stop using the flexsea library and go back to the regular shell
deactivate
```
> Please Note to use the right symlink to `python` or `python3` in all the above commands based on your OS that you are running this on.<br>

If you're using the [fish shell](https://fishshell.com/), use this command to activate the virtualenv: `. actpack/bin/activate.fish`

If `flexsea` is already installed and you need to upgrade it, run this:
```bash
#activate your virtual environment if desired as shown above
#	On a Windows system:
	python -m pip install --upgrade flexsea
#	On other OS:
	python3 -m pip install --upgrade flexsea
```

#### Removal
To uninstall `flexsea` from your computer, run this:
```bash
#	On a Windows system:
	python -m pip uninstall flexsea
#	On other OS:
	python3 -m pip uninstall flexsea
```

## Getting Started

### ActPack

Use this information to set up your ActPack, power it and update its firmware.:

[General information about the Dephy Actuator Package](http://dephy.com/wiki/flexsea/doku.php?id=dephyactpack)

### Get the demo scripts

Download the latest release as a [zip file](https://github.com/DephyInc/Actuator-Package/archive/refs/heads/master.zip)

Alternatively, use git to clone the repository:

```bash
$ git clone https://github.com/DephyInc/Actuator-Package.git
$ cd Actuator_Package
```

### Configuring Demo Scripts

All scripts can be run on their own. Use `--help` to see the required command line arguments.

For your convenience, `run_demos.py` displays a menu of all available scripts.

`run_demos.py` uses `ports.yaml` to configure the ports used to communicate with the ActPacks.

You'll need to modify `ports.yaml` to suit your needs. By default, this files contains the most common Windows configuration along with examples for other platforms.

To use it, uncomment and/or modify the lines you need. Below is an example of that file used on Windows, with one port (`COM3`).

```yaml
# ports.yaml
#
# Adjust the baudrate if needed and uncomment or edit the port list.
#
# Note that commented-out lines start with a "#"
# Also the ports list has dashes "-" before the values to signify a list
#
# See the sample ports values below depending on your platform
baud_rate: 230400
ports:
# Windows
	- COM3
	# - COM4
# Ubuntu WSL
	# - /dev/ttyS3
	# - /dev/ttyS4
# Native Linux (e.g. Ubuntu or Raspbian)
	# - /dev/ttyACM0
	# - /dev/ttyACM1
```

Once you modify your copy of `ports.yaml`, use the following command to prevent git from tracking the changes.

```bash
$ git update-index --assume-unchanged Python/flexsea_demo/ports.yaml
```

### Getting Started
The latest instructions for working with the Actuatory Package and sample programs are located on Dephy's Wiki:

[General information about the Dephy Actuator Package](http://dephy.com/wiki/flexsea/doku.php?id=dephyactpack)

[Information about the scripts](http://dephy.com/wiki/flexsea/doku.php?id=scripts)


### Running Demo Scripts

#### Using The Interactive Menu

1. Plug the device in and turn it ON
2. From a terminal, run the `Actuator-Package/Python/flexsea_demo/run_demos.py` script
```bash
$ cd Python/flexsea_demo
$ ./run_demos.py
```
3. Notice the menu that displays
```bash
(actpack) ubuntu@PC:~/Actuator-Package/Python/flexsea_demo $ ./run_demos.py

	▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
	██░▄▄▀██░▄▄▄██░▄▄░██░██░██░███░██
	██░██░██░▄▄▄██░▀▀░██░▄▄░██▄▀▀▀▄██
	██░▀▀░██░▀▀▀██░█████░██░████░████
	▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
			Beyond Nature™

STOP!
Read our important safety information at https://dephy.com/start/
before running the scripts for the first time.

Actuator Package Demo Scripts:
------------------------------
[0] Read Only
[1] Open Control
[2] Current Control
[3] Position Control
[4] Impedance Control
[5] Two Positions Control
[6] High Speed Test
[7] High Stress Test
[8] Two Devices Position Control
[9] Two Devices Leader Follower Control

Advanced Utilities:
------------------------------
[10] Bootloader Check
[11] Find Poles

Choose experiment number [q to quit]:
```
4. Enter the experiment number. Be careful, most of them will make the motor move!

Alternatively, the `run_demos.py` script accepts command line arguments. The first argument is the experiment number, and the second (optional) is the number of devices.

Calling Read Only directly (default = 1 device):
```bash
$ ./run_demos.py 0
```
Two Devices Leader Follower is #9, it uses 2 devices. To launch it with one command:
```bash
$ ./run_demos.py 9 2
```

#### Launching the Demos Directly
All scripts can be run individually by calling them and passing arguments. Use –help to see usage information. See the example below using `high_speed_test.py`.

```bash
$ ./high_speed_test.py --help
usage: high_speed_test.py [-h] [-b B] Ports [Ports ...]

FlexSEA High Speed Test

positional arguments:
	Ports           Your devices' serial ports.

optional arguments:
	-h, --help      show this help message and exit
	-b B, --baud B  Serial communication baud rate.
```

If your ActPAck is on port `COM3` you can run the script depicted above like this:

```bash
$ ./high_speed_test.py COM3
```

With more than one ActPAck (e.g. in `COM3` and `COM4`):

```bash
$ ./high_speed_test.py COM3 COM4
```

### Install Githooks

If you're planning to contribute to this repository, run this to install the autoformatting and syntax checks.

```bash
$ ./install_hooks.sh
```

To run the checks manually, run this command:
```bash
$ pre-commit run --all-files
```

See more info on [pre-commit syntax](https://pre-commit.com).

### Documentation

To generate the automatic documentation for this repository, run the command below:
```bash
$ cd docs
$ doxygen doxyfile.in
```

Then open the generated files:
```bash
sensible-browser html/index.html
```

## Troubleshooting

* On Windows, if flexsea can't install, or it can't load the libraries, make sure only once version of git and Python are installed as specified ins the installation section.
* If your device has never had poles configured, you should run “find poles” from the demo script before trying other demos. This is not typical!
* The leading cause of segmentation faults is a Device Spec mismatch between the embedded system and the scripts. This happens when you use old firmware with new scripts.

License: CC BY-NC-SA 4.0
[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
