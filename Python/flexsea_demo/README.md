# FlexSEA Demos
This package contains demosfor the open-source [flexSEA library](https://pypi.org/project/flexsea/). The idea is for these demos to serve as both sanity checks for making sure flexSEA is working correctly as well as blueprints for how certain tasks can be accomplished with the library.


## Requirements
* `Python >= 3.8`
* `git`


## Installation on Linux

Install the dependencies:

```bash
sudo apt install python3 python3-pip git
```

Create a virtual environment:

```bash
mkdir ~/.venvs
python3 -m venv ~/.venvs/flexsea_demos_env
```

Activate the newly created virtual environment:

```bash
source ~/.venvs/flexsea_demos_env/bin/activate
```

Clone the repo:

```bash
git clone https://github.com/DephyInc/Actuator-Package.git
```

Change into the demos directory:

```bash
cd Actuator-Package/Python/flexsea_demo
```

and install the demos with `pip`:

```bash
pip3 install .
```


### Installation on Windows
Install the appropriate version of Python for Windows from [here](https://www.python.org/downloads/windows/) and get the Git for Windows client [here](https://gitforwindows.org/) here.

:warning: During the installation process, make sure you check the box that adds Python and Git to your Path.

Now, open the git bash terminal included with git for windows and create a virtual environment:

```bash
mkdir ~/.venvs
python -m venv ~/.venvs/flexsea_demos_env
```

Activate the newly created virtual environment:

```bash
source ~/.venvs/flexsea_demos_env/bin/activate
```

Clone the repo:

```bash
git clone https://github.com/DephyInc/Actuator-Package.git
```

Change into the demos directory:

```bash
cd Actuator-Package/Python/flexsea_demo
```

and install the demos with `pip`:

```bash
pip install .
```


## Usage

This tool is a **command line interface** (CLI), which means you interact with it in the same way you'd use any other terminal command (e.g., `ls`, `pwd`, etc.).

The basic usage pattern is:

```bash
flexsea_demos <demo_name> <parameter_file>
```

To see a list of the available demo names:

```bash
flexsea_demos -h
```

Each demo is fully configurable via the parameter file. A sample parameter file -- `sample_params.yaml.lock` -- is included and utilizes the [yaml](https://en.wikipedia.org/wiki/YAML) format.

If you want to tweak the default parameters, you can do so by making a copy of the sample parameter file and then editing the copied file.

Additionally, rather than using the parameter file (or in addition to it), you can override the value of a parameter by passing it as a command-line argument.

### Example
As an example we'll run the `read_only` demo. The first step is to create a space from which the demos will be run:

```bash
mkdir -p ~/code/sandbox/python/flexsea_demos
```

copy the parameter file:

```bash
flexsea_demos unlock sample_params.yaml.lock ~/code/sandbox/python/flexsea_demos/params.yaml
```

and switch to the newly created directory:

```bash
cd ~/code/sandbox/python/flexsea_demos
```

Before running the demo, open up `params.yaml` and make sure that the ports are set correctly and that there is one port specified for each device you want to run the demo with. On Windows, the ports are usually of the form `COM3, COM4`, etc. On linux (Ubuntu, raspbian), the ports are usually either of the form `/dev/ttyACM0` or `/dev/ttyS3`.

With the ports set correctly, run the `read_only` demo:

```bash
flexsea_demos read_only params.yaml
```
