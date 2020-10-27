# Actuator-Package

The Dephy Actuator Package is a turn-key solution for people who want to test FlexSEA's capabilities or quickly design a prosthetic limb. The Package consists of a custom brushless motor integrated with a FlexSEA-Rigid circuit and a minimalist enclosure, pre-loaded embedded software, and a full suite of high-level software and test scripts.

## Scripts
The fx_plan_stack API is a suite of functions that configure and control FlexSEA devices. Detailed information can be found on the Dephy Wiki, which is included in the references below.

The repo contains the FlexSEA-Rigid Actuator Package library and sample programs for C/C++, Python, MATLAB and SIMULINK. These scripts are accompanied by and are dependent upon C based libraries for both Windows (.dll) and Unix(.so).

### Python Dependencies

Install Python 3.7.x on Ubuntu 20.04 or 18.04
```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
# Press [ENTER] to continue
sudo apt install python3.7 -y
```

On Windows, use [this installer](https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe) to isntall.

In order to install the required Python dependencies, run the following command from the root directory of this repository:

```bash
pip install -r Python/requirements.txt
```

Note that in Linux, you might need to use `pip3` or your specific Python version instead. Also the user flag can be used for the dependencies to be installed in user space instead of system-wide as follows.

```bash
python3.7 -m pip install -U -r Python/requirements.txt
```

## Getting Started
The latest instructions for working with the Actuatory Package and sample programs are located on Dephy's Wiki:

[General information about the Dephy Actuator Package](http://dephy.com/wiki/flexsea/doku.php?id=dephyactpack)

[Information about the scripts](http://dephy.com/wiki/flexsea/doku.php?id=scripts)

License: CC BY-NC-SA 4.0
[![License: CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
