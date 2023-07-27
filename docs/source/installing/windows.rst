.. _flexsea_docs_installing_windows:

Installing on Windows
=====================


Prerequisites
-------------

* Install `Git for Windows <https://git-scm.com/download/win>`_. Make sure you download the version (either 32-bit or 64-bit) that matches your system (most likely 64 bit)
* Install `Python 3.11 <https://www.python.org/downloads/windows/>`_

.. note::

   Make sure you download the 64-bit version if you downloaded the 64-bit Git above and the 32-bit version if you installed the 32-bit Git above.

.. note::

   When going through the installation wizard, make sure you check the box that adds Python to your PATH.

Install ``flexsea`` in a virtual environment. From your Git Bash terminal:

.. code-block:: bash

    mkdir -p ~/.venvs
    python -m venv ~/.venvs/dephy
    source ~/.venvs/dephy/Scripts/activate

You will need to run the above ``source`` command each time you open a new terminal unless you add the command to your profile.


Installing
----------

The easiest way to install ``flexsea`` is via ``pip``:

.. code-block:: bash

    python -m pip install flexsea

If you intend to contribute or modify the code, however, it may be helpful to install from source:

.. code-block:: bash

   git clone https://github.com/DephyInc/Actuator-Package.git
   cd Actuator-Package/
   git checkout v11.0.7
   python -m pip install .


Developing
----------

To develop ``flexsea``, we strongly recommend installing `Poetry <https://python-poetry.org/docs/>`_.

To do so, start Windows Powershell as Administrator. By default, Powershell will not
start in the same directory as Git Bash. This means in order to activate your virtual
environment from Powershell, we have to first navigate to that directory. Here we use
``USER`` in place of your user name:

.. code-block:: powershell

    cd C:\Users\USER\.venvs\dephy\Scripts
    .\Activate.ps1
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

.. note::

   Once installed, `poetry` should be available from your Git Bash terminal.

Activate the development environment and install the dependencies for ``flexsea`` by
running the following commands from your Git Bash terminal and the ``flexsea`` repository:

.. code-block:: bash

    poetry shell
    poetry install

Pull Requests and Bug Reports (Issues) are welcome!
