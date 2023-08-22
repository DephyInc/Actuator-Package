.. _flexsea_docs_installing_ubuntu:

Installing on Ubuntu
====================

Prerequisites
-------------


The following script will:

* Update your system
* Install the linux USB libraries
* Add your current user to the ``dialout`` group (needed for serial communication)

.. note::

   You must reboot your machine after adding your user to the ``dialout`` group in order for the changes to take effect. Logging out and back in is not enough.


.. code-block:: bash

    sudo apt update && sudo apt upgrade
    sudo apt install libusb-1.0-0 libusb-1.0-0-dev
    sudo usermod -a -G dialout "$USER"


Python
^^^^^^

``flexsea`` requires ``python >= 3.11``.

Installing via APT
++++++++++++++++++
Installing via the ``apt`` package manager is straightforward and quick, but will not
necessarily get you the latest version.

.. code-block:: bash

    sudo apt install python3.11 python3.11-venv

Now create a virtual environment:

.. code-block:: bash

    mkdir -p $HOME/.venvs
    python3.11 -m venv $HOME/.venvs/dephy
    source $HOME/.venvs/dephy/bin/activate

You will need to run the above ``source`` command each time you create a new terminal, unless you add the command to your profile.

Installing from Source
++++++++++++++++++++++

The following script will:

* Download all of the dependencies for Python (this list is current as of Python 3.11.3. If you are building a later version, it's possible that this list has changed. Please see `this <https://devguide.python.org/getting-started/setup-building/#build-dependencies>`_ link for the most up to date dependencies)
* Download the Python source code
* Build, test, and install Python (this can take a while)

.. code-block:: bash

    # Python dependencies
    sudo apt install build-essential gdb lcov pkg-config \
        libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
        libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
        lzma lzma-dev tk-dev uuid-dev zlib1g-dev

    # Clone the python repo
    git clone --depth 1 --branch v3.11.3 https://github.com/python/cpython.git
    cd cpython/

    # Switch to the version you want to build
    git checkout v3.11.3

    # Build (change the prefix path to install to a different location)
    mkdir -p $HOME/.local
    ./configure --enable-optimizations --prefix=$HOME/.local
    make
    make test
    sudo make install

Now create a virtual environment:

.. code-block:: bash

    mkdir -p $HOME/.venvs
    # Replace $HOME/.local with the prefix path you used during configuration
    $HOME/.local/bin/python3.11 -m venv $HOME/.venvs/dephy
    source $HOME/.venvs/dephy/bin/activate

You will need to run the above ``source`` command each time you create a new terminal unless you add the command to your profile.


Installing
----------

The easiest way to install ``flexsea`` is via ``pip``:

.. code-block:: bash

    python3 -m pip install flexsea

If you intend to contribute or modify the code, however, it may be helpful to install from source:

.. code-block:: bash

   git clone https://github.com/DephyInc/Actuator-Package.git
   cd Actuator-Package/
   git checkout v11.0.7
   python3 -m pip install .


Developing
----------

To develop ``flexsea``, we strongly recommend installing `Poetry <https://python-poetry.org/docs/>`_.

Activate the development environment and install the dependencies for ``flexsea``:

.. code-block:: bash

    poetry shell
    poetry install


Pull Requests and Bug Reports (Issues) are welcome!
