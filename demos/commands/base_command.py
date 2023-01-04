from cleo.helpers import option

import flexsea.config as cfg
from flexsea.device import Device
from flexsea.utilities import find_device
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

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__()

        self.add_style("info", fg="cyan")
        self.add_style(
            "error",
            fg="red",
            options=[
                bold,
            ],
        )
        self.add_style(
            "warning",
            fg="yellow",
            options=[
                bold,
            ],
        )
        self.add_style("success", fg="green")

        self._devices: List = []
        self._loopTime: int = 0

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
            self._devices.append(find_device(None, br, cv))

        for device in self._devices:
            device.open()
            device.start_streaming(self.option("frequency"))

        # Run time is the total demo time. Loop time is the amount of time
        # each device gets such that loopTime * nDevices = runTime
        self._loopTime = int(self.option("runTime") / len(self._devices))

    # -----
    # cleanup
    # -----
    def cleanup(self) -> None:
        for device in self._devices:
            device.stop_motor()
            device.stop_streaming()
            device.close()
