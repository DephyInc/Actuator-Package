# Dephy FlexSEA Library

Use this library to work with Dephy's high performance actuators and exoskeletons.

More information at https://dephy.com/faster

## Usage

You can use the `flexsea` library in your code as follows:

```python
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex

fxs = flex.FlexSEA()
dev_id = fxs.open(...
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
Once the package is ready to publish and the version has been updated. Run this to upload it to PyPi to allow users to install it via `pip`
See [these instructions](https://packaging.python.org/tutorials/packaging-projects/) in case you need to get a PyPi account or token.

### Test upload
Upload to test server
```bash
python3 -m twine upload --repository testpypi dist/*
```
Install from test server
```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps flexsea
```

### Test upload
```bash
python3 -m twine upload --repository testpypi dist/*
```