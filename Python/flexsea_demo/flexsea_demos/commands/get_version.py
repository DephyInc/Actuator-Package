from time import sleep
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#              VersionCommand
# ============================================
class VersionCommand(Command):
    """
    Check version of onboard MCUs.

    check_version
        {paramFile : Yaml file with demo parameters.}
    """

    # Schema of parameters required by the demo
    required = {
        "ports": List,
        "baud_rate": int,
    }

    __name__ = "check_version"

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.fxs = None

    # -----
    # handle
    # -----
    def handle(self):
        """
        Checks the versions of onboard MCUs.
        """
        setup(self, self.required, self.argument("paramFile"), self.__name__)
        for port in self.ports:
            device = Device(self.fxs, port, self.baud_rate)
            self._get_version(device)
            device.close()

    # -----
    # _get_version
    # -----
    def _get_version(self, device):
        if device.request_firmware_version() == fxe.FX_SUCCESS.value:
            print("Collecting version information. Please wait...", flush=True)
        else:
            print("Firware version request failed", flush=True)
            device.close()
            raise ValueError

        sleep(5)

        fw_array = fxe.FW()
        fw_array = device.get_last_received_firmware_version()
        fw_mn = fxu.decode(fw_array.Mn)
        fw_ex = fxu.decode(fw_array.Ex)
        fw_re = fxu.decode(fw_array.Re)
        fw_habs = fxu.decode(fw_array.Habs)

        print(f"Firmware version for device {device.dev_id}:", flush=True)
        print(f"\t Mn  : v{fw_mn}", flush=True)
        print(f"\t Ex  : v{fw_ex}", flush=True)
        print(f"\t Re  : v{fw_re}", flush=True)
        print(f"\t Habs: v{fw_habs}", flush=True)
