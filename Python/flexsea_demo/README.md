# FlexSEA Demos
This repo contains demo scripts for the open-source [flexSEA library](https://pypi.org/project/flexsea/). The idea is for these demos to serve as both sanity checks for making sure flexSEA is working correctly as well as blueprints for how certain tasks can be accomplished with the library.


## Requirements
* `Python >= 3.8`.
* [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)


## Installation
First clone the repository:

```bash
git clone https://github.com/jcoughlin11/flexsea_demos
cd flexsea_demos
```


Now create a virtual environment:

```bash
mkdir ~/.venvs
virtualenv ~/.venvs/flexsea_demos_env
```

Activate the newly created virtual environment:

```bash
source ~/.venvs/flexsea_demos_env/bin/activate
```

and install with `pip`:

### On Windows
```bash
python -m pip install .
```

### On Linux

```bash
pip3 install .
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

Each demo is fully configurable via the parameter file. A sample parameter file -- `sample_params.yaml` -- is included and utilizes the [yaml](https://en.wikipedia.org/wiki/YAML) format.

The parameter file is source controlled, so you can feel free to make changes to it directly and then, should you desire to get back to the original version, simply check it out:

```bash
git checkout <parameter_file>
```


### Example
As an example we'll run the `read_only` demo. The first step is to create a space from which the demos will be run:

```bash
mkdir -p ~/code/sandbox/python/flexsea_demos
```

copy the parameter file:

```bash
cp sample_params.yaml ~/code/sandbox/python/flexsea_demos/params.yaml
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
