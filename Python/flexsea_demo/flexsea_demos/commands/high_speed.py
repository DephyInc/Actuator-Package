from time import sleep
from time import time
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxPlotting as fxp
from flexsea import fxUtils as fxu
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#             HighSpeedCommand
# ============================================
class HighSpeedCommand(Command):
    """
    Runs the high speed demo.

    high_speed
        {paramFile : Yaml file with demo parameters.}
    """

    # Schema of parameters required by the demo
    required = {
        "ports": List,
        "baud_rate": int,
        "controller_type": int,
        "signal_type": int,
        "cmd_freq": int,
        "signal_amplitude": int,
        "nLoops": int,
        "signal_freq": int,
        "cycle_delay": float,
        "request_jitter": bool,
        "jitter": int,
    }

    __name__ = "high_speed"

    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()

        self.ports = []
        self.baud_rate = 0
        self.controller_type = 0
        self.signal_type = 0
        self.cmd_freq = 0
        self.signal_amplitude = 0
        self.nLoops = 0
        self.signal_freq = 0
        self.cycle_delay = 0
        self.request_jitter = False
        self.jitter = 0

        self.fxs = None
        self.dt = 0.0
        self.start_time = None
        self.samples = []
        self.figure_counter = 1
        self.signal = {"sine": 1, "line": 2}
        self.i = 0
        self.current_gains = {"KP": 40, "KI": 400, "KD": 0, "K": 0, "B": 0, "FF": 128}
        self.pos_gains = {"KP": 300, "KI": 50, "KD": 0, "K": 0, "B": 0, "FF": 0}
        self.plot_data = {
            "requests": [],
            "measurements": [],
            "times": [],
            "cycle_stop_times": [],
            "dev_write_command_times": [],
            "dev_read_command_times": [],
        }

        matplotlib.use("WebAgg")
        if fxu.is_pi():
            matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the high speed demo.
        """
        setup(self, self.required, self.argument("paramFile"), self.__name__)
        self.dt = 1.0 / (float(self.cmd_freq))
        self._get_samples()

        if self.controller_type == 0:
            self.controller_type = fxe.HSS_POSITION
            gains = self.pos_gains
        elif self.controller_type == 1:
            self.controller_type = fxe.HSS_CURRENT
            gains = self.current_gains
        else:
            raise ValueError(f"Invalid controller type '{self.controller_type}'")

        for port in self.ports:
            input("Press 'ENTER' to continue...")
            self._reset_plot()
            device = Device(self.fxs, port, self.baud_rate)
            device.set_controller(self.controller_type)
            device.set_gains(gains)
            self._high_speed(device)
            device.motor(fxe.FX_NONE, 0)
            sleep(0.1)
            self._plot(device)
            device.close()

    # -----
    # _get_samples
    # -----
    def _get_samples(self):
        """
        Generates sample values for the demo.
        """
        np.random.seed(42)
        if self.signal_type not in self.signal.values():
            raise ValueError(f"Unsupported signal type: `{self.signal_type}`")
        if self.signal_type == self.signal["sine"]:
            f = self.signal_freq
        else:
            f = 1
        self.samples = fxu.sin_generator(self.signal_amplitude, f, self.cmd_freq)
        if self.request_jitter:
            self.samples = self.samples + np.random.normal(
                loc=self.jitter, size=self.samples.shape
            )
        print("Command table:")
        print(np.int64(self.samples))

    # -----
    # _high_speed
    # -----
    def _high_speed(self, device):
        self.start_time = time()
        if device.controller_type == fxe.HSS_POSITION:
            sleep(0.1)
            data = device.read()
            pos0 = data.mot_ang
        else:
            pos0 = 0

        self.i = 0
        for rep in range(self.nLoops):
            elapsed_time = time() - self.start_time
            fxu.print_loop_count_and_time(rep, self.nLoops, elapsed_time)

            for sample in self.samples:
                sleep(self.dt)
                if device.controller_type != fxe.HSS_CURRENT:
                    sample = sample + pos0

                # Read
                begin_time = time()
                data = device.read()
                self.plot_data["dev_read_command_times"].append(time() - begin_time)

                # Write
                begin_time = time()
                device.motor(device.controller, sample)
                self.plot_data["dev_write_command_times"].append(time() - begin_time)

                if device.controller == fxe.FX_CURRENT:
                    val = data.mot_cur
                else:
                    val = data.mot_ang - pos0

                self.plot_data["times"].append(time() - self.start_time)
                self.plot_data["measurements"].append(val)
                self.plot_data["requests"].append(sample)
                self.i += 1

            # Delay between cycles (sine wave only)
            if self.signal_type == self.signal["sine"]:
                for _ in range(int(self.cycle_delay / self.dt)):
                    sleep(self.dt)
                    data = device.read()

                    if device.controller_type == fxe.HSS_CURRENT:
                        self.plot_data["measurements"].append(data.mot_cur)
                    elif device.controller_type == fxe.HSS_POSITION:
                        self.plot_data["measurements"].append(data.mot_ang - pos0)

                    self.plot_data["times"].append(time() - self.start_time)
                    self.plot_data["requests"].append(sample)
                    self.i += 1

            # We'll draw a line at the end of every period
            self.plot_data["cycle_stop_times"].append(time() - self.start_time)

    # -----
    # _plot
    # -----
    def _plot(self, device):
        if self.signal_type == self.signal["sine"]:
            signal_type_str = "sine"
        else:
            signal_type_str = "line"
        elapsed_time = time() - self.start_time
        actual_period = self.plot_data["cycle_stop_times"][0]
        actual_frequency = 1 / actual_period
        cmd_freq = self.i / elapsed_time
        # Figure: setpoint, desired vs measured (1st device)
        self.figure_counter = fxp.plot_setpoint_vs_desired(
            device.dev_id,
            self.figure_counter,
            device.controller_type,
            actual_frequency,
            self.signal_amplitude,
            signal_type_str,
            cmd_freq,
            self.plot_data["times"],
            self.plot_data["requests"],
            self.plot_data["measurements"],
            self.plot_data["cycle_stop_times"],
        )
        self.figure_counter = fxp.plot_exp_stats(
            device.dev_id,
            self.figure_counter,
            self.plot_data["dev_write_command_times"],
            self.plot_data["dev_read_command_times"],
        )
        fxu.print_plot_exit()
        plt.show()

    # -----
    # _reset_plot
    # -----
    def _reset_plot(self):
        self.plot_data = {
            "requests": [],
            "measurements": [],
            "times": [],
            "cycle_stop_times": [],
            "dev_write_command_times": [],
            "dev_read_command_times": [],
        }
        plt.clf()
