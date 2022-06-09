"""
current_control.py

Implements the current control demo.
"""
from time import sleep
from typing import Dict
from typing import List

from cleo import Command
from flexsea import fx_enums as fxe
from flexsea import fx_utils as fxu
from flexsea.device import Device

from flexsea_demos.utils import setup

# ============================================
#                  _ramp
# ============================================
def _ramp(device, current):
    """
    Adjusts the device's current and print's the actual measured
    value for comparison.
    """
    print("Device", device)
    device.send_motor_command(fxe.FX_CURRENT, current)
    sleep(0.1)
    data = device.read()
    fxu.clear_terminal()
    print("Desired (mA):         ", current)
    print("Measured (mA):        ", data.mot_cur)
    print("Difference (mA):      ", (data.mot_cur - current), "\n")
    device.print(data)


# ============================================
#           CurrentControlCommand
# ============================================
class CurrentControlCommand(Command):
    """
    Runs the current control demo.

    current_control
            {paramFile? : Yaml file with demo parameters.}
            {--ports=* : List of device ports. Comma separated. Overrides parameter file.}
            {--baud-rate= : USB baud rate. Overrides parameter file.}
            {--streaming-freq= : Frequency (Hz) for device to stream data.}
            {--run-time= : Time (s) to run each device. Overrides parameter file.}
            {--gains= : Order: KP,KI,KD,K,B,FF. Comma separated. Overrides parameter file.}
            {--hold-current= : Target current to keep device at. Overrides parameter file.}
            {--ramp-down-steps= : Proxy for cooldown time. Overrides parameter file.}
    """

    # pylint: disable=too-many-instance-attributes

    # Schema of parameters required by the demo
    required = {
        "ports": List,
        "baud_rate": int,
        "streaming_freq": int,
        "run_time": int,
        "gains": Dict,
        "hold_current": int,
        "ramp_down_steps": int,
    }

    __name__ = "current_control"

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()
        self.ports = []
        self.baud_rate = 0
        self.streaming_freq = None
        self.run_time = 0
        self.gains = {}
        self.hold_current = 0
        self.ramp_down_steps = 0
        # Number of loops per device to give total desired run time
        self.n_loops = 0

    # -----
    # handle
    # -----
    def handle(self):
        """
        Current control demo.
        """
        # Creating a list to store the device id of the two exos
        device_list = []
        setup(self, self.required, self.argument("paramFile"), self.__name__)
        # Run time is the total length of the demo. Since each loop takes 0.1
        # seconds, the total number of loops for the whole demo is the total
        # run time / 0.1. We then divide this by the number of devices to
        # get the desired number of loops per device
        self.n_loops = int(self.run_time / (0.1 * len(self.ports)))
        if self.n_loops <= 0:
            self.n_loops = 1
        for port in self.ports:
            input("Press 'ENTER' to continue...")
            device = Device(port, self.baud_rate)
            device.open(self.streaming_freq)
            device.set_gains(**self.gains)
            device_list.append(device)

        self._current_control(device_list)

    # -----
    # _current_control
    # -----
    def _current_control(self, device_list):
        for device in device_list:
            for _ in range(self.n_loops):
                _ramp(device, self.hold_current)
        for device in device_list:
            for i in range(self.ramp_down_steps):
                current = (
                    self.hold_current
                    * (self.ramp_down_steps - i)
                    / self.ramp_down_steps
                )
                _ramp(device, current)
            device.send_motor_command(fxe.FX_NONE, 0)
            sleep(0.5)
            device.close()
