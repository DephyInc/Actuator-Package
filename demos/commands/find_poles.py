"""
find_poles.py

Implements the pole-finding tool.
"""
from typing import List

from cleo import Command

from flexsea.device import Device

from ..utils import setup


# ============================================
#              FindPolesCommand
# ============================================
class FindPolesCommand(Command):
    """
    Finds poles on the device.

    find_poles
            {paramFile? : Yaml file with demo parameters.}
            {--ports=* : List of device ports. Overrides parameter file.}
            {--baud-rate= : USB baud rate. Overrides parameter file.}
    """

    # Schema of parameters required by the demo
    required = {
        "ports": List,
        "baud_rate": int,
    }

    __name__ = "find_poles"

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0

    # -----
    # handle
    # -----
    def handle(self):
        """
        Finds the devices' poles.
        """
        setup(self, self.required, self.argument("paramFile"), self.__name__)
        for port in self.ports:
            input("Press 'ENTER' to continue...")
            device = Device(port, self.baud_rate)
            device.open()
            device.find_poles()
