# Actuator-Package

The Dephy Actuator Package is a turn-key solution for people who want to test FlexSEA's capabilities or quickly design a prosthetic limb. The Package consists of a custom brushless motor integrated with a FlexSEA-Rigid circuit and a minimalist enclosure, pre-loaded embedded software, and a full suite of high-level software and test scripts.

### Important - Compatibility
You must use compatible firmware! Failure to do so will result in segmentation faults. Refer to the Dephy Wiki to know what goes with what.

### Scripts

The fx_plan_stack API is a suite of functions that configure and control FlexSEA devices. Detailed information can be found on the Dephy Wiki, which is included in the references below.

The repo contains the FlexSEA-Rigid Actuator Package library `flexsea` and sample programs for C/C++, Python, MATLAB and SIMULINK. These scripts are accompanied by and are dependent upon C based libraries for both Windows (.dll) and Unix(.so).

### Install Python

#### Linux
Run this script to install the python dependencies before running the python scripts
```bash
./install_python_deps.sh
```

#### Windows 10

On Windows, use [this installer](https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe) to install Python 3.7.

Then, to install the required Python dependencies, run the following command from the root directory of this repository using PowerShell:

### Install FlexSEA Library

```bash
# Define your own virtual environment
# this is not required but it helps keeping your environment clean
python3 -m virtualenv --python=/usr/bin/python3.7 actpack
# Activate your virtualenv
source actpack/bin/activate
# Once the environment is activated, install the package
python3 -m pip install --upgrade pip 
python3 -m pip install flexsea
# Run your script that uses flexsea
# Once you want to stop using the flexsea library and go back to the regular shell
deactivate 

```

If `flexsea` is already installed and you need to upgrade it, run this:
```bash
#activate your virtual environment if desired as shown above
python3 -m pip install --upgrade flexsea
```

### Removal
To uninstall `flexsea` from your computer, run this:
```bash
python3 -m pip uninstall flexsea
```

### Getting Started
The latest instructions for working with the Actuatory Package and sample programs are located on Dephy's Wiki:

[General information about the Dephy Actuator Package](http://dephy.com/wiki/flexsea/doku.php?id=dephyactpack)

[Information about the scripts](http://dephy.com/wiki/flexsea/doku.php?id=scripts)

### Runing The Demo Scripts

All scripts can be run on their own. use `--help` to see the required command line arguments.

For your convenience, `run_demos.py` displays a menu of all available scripts.

`run_demos.py` uses `ports.yaml` to configure the ports used to communicate with the ActPacks.

Feel free to modify `ports.yaml` to suit your needs. By default this files contains the most common configuration along with examples for other platforms.

Once you modify your copy of `ports.yaml`, use the following command to prevent git from tracking the changes.
```bash
git update-index --assume-unchanged Python/flexsea_demo/ports.yaml
```

License: CC BY-NC-SA 4.0
[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
