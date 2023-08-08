# FlexSEA


`flexsea` is a Python package for interacting with Dephy's wearable robotic devices.
It can be used for gathering data from a device or for writing your own controller.

## Installation

Please see the installation documentation [here](https://flexsea.readthedocs.io/en/latest/installing/index.html) for detailed
installation instructions.


## Usage

### Demos

A good reference for what `flexsea` is capable of is the collection of demo scripts
that live in the `demos/` directory. The demos are numbered and should be viewed in
order, as each successive demo builds off of the information presented in the previous
one. Each demo has verbose comments explaining each step.

You can also find a quickstart guide [here](https://flexsea.readthedocs.io/en/latest/quickstart.html)


## Testing
You really only need to do this if you're developing on `flexsea`. There are two types
of tests: unit tests and integration tests. Currently, the integration tests are,
essentially, the same as the demos, but set up in such a way as to be more configurable
from the command line.

The easiest way to run them is:

```bash
cd tests/integration_tests/
python3 ./test_open_control.py --help
```

The above command will show the required arguments for the test you've chosen to run.
You'll then run the script with the necessary arguments. For the open control test
referenced above, there are no required arguments, but all key parameters can be
controlled via command-line options.

```bash
python3 ./test_open_control.py
```


### API Overview

Please see the api documentation [here](https://flexsea.readthedocs.io/en/latest/api/index.html).


## Contributing

If you find a bug or have a feature request, please fork the repository, make your
changes, and then issue a pull request (PR). We'd love to hear from you!
