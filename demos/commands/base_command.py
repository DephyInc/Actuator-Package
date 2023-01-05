from typing import List

from cleo.commands.command import Command
from cleo.helpers import option

import flexsea.config as cfg
from flexsea.device import Device
from flexsea.utilities import find_port
from flexsea.utilities import get_os


# ============================================
#              BaseDemoCommand
# ============================================
class BaseDemoCommand(Command):

    options = [
        option("port", "-p", "COM port device is connected to.", False, multiple=True),
        option("baudRate", "-b", "Device's baud rate.", False, default=230400),
        option("frequency", "-f", "Streaming frequency in Hz.", False, default=100),
        option("runTime", "-r", "Demo duration in seconds.", False, default=10),
        option("gains", "-g", "Order: KP,KI,KD,K,B,FF. Comma separated.", False),
        option("cLibVer", "-c", "C library version to use.", False, default=cfg.LTS),
    ]

    _devices: List = []
    _loopTime: int = 0

    # -----
    # setup
    # -----
    def setup(self) -> None:
        if "windows" in get_os():
            msg = "Demos might not work right on Windows due to timing issues. Proceed?"
            if not self.confirm(msg, False):
                sys.exit(0)
        br = self.option("baudRate")
        cv = self.option("cLibVer")
        ports = self.option("port")

        self._devices = [Device(p, br, cv) for p in ports]

        if not self._devices:
            self._devices.append(Device(find_port(br, cv), br, cv))

        for device in self._devices:
            device.open()
            device.start_streaming(int(self.option("frequency")))

        # Run time is the total demo time. Loop time is the amount of time
        # each device gets such that loopTime * nDevices = runTime
        self._loopTime = int(self.option("runTime") / len(self._devices))

    # -----
    # cleanup
    # -----
    def cleanup(self) -> None:
        for device in self._devices:
            device.close()
