"""
high_speed.py

Implements the high speed demo.
"""
from time import sleep
from time import time
from typing import List

from cleo import Command
from flexsea import fx_enums as fxe
from flexsea import fx_plotting as fxp
from flexsea import fx_utils as fxu
from flexsea.flexsea import Device
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from flexsea_demos.utils import setup


# ============================================
#             HighSpeedCommand
# ============================================
class HighSpeedCommand(Command):
    """
    Runs the high speed demo.

    high_speed
            {paramFile? : Yaml file with demo parameters.}
            {--ports=* : List of device ports. Comma separated. Overrides parameter file.}
            {--baud-rate= : USB baud rate. Overrides parameter file.}
            {--streaming-freq= : Frequency (Hz) for device to stream data.}
            {--controller-type= : See flexsea.fxEnums. Overrides parameter file.}
            {--signal-type= : 1 is sine, 2 is line. Overrides parameter file.}
            {--cmd-freq= : Device streaming frequency (Hz). Overrides parameter file.}
            {--signal-amplitude= : Encoder position or current. Overrides parameter file.}
            {--n-loops= : Proxy for run time. Overrides parameter file.}
            {--signal-freq= : Frequency of sine wave. Overrides parameter file.}
            {--cycle-delay= : Time between signals to controller. Overrides parameter file.}
            {--request-jitter : Adds noise to signal. Overrides parameter file.}
            {--jitter= : Size of the noise added to signal. Overrides parameter file.}
    """

    # pylint: disable=too-many-instance-attributes

    # Schema of parameters required by the demo
    required = {
        "ports": List,
        "baud_rate": int,
        "streaming_freq": int,
        "controller_type": int,
        "signal_type": int,
        "cmd_freq": int,
        "signal_amplitude": int,
        "n_loops": int,
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
        self.streaming_freq = None
        self.controller_type = 0
        self.signal_type = 0
        self.cmd_freq = 0
        self.signal_amplitude = 0
        self.n_loops = 0
        self.signal_freq = 0
        self.cycle_delay = 0
        self.request_jitter = False
        self.jitter = 0

        # pylint: disable=C0103
        self.dt = 0.0
        self.start_time = None
        self.samples = []
        self.figure_counter = 1
        self.signal = {"sine": 1, "line": 2}
        self.i = 0
        self.current_gains = {"kp": 40, "ki": 400, "kd": 0, "k": 0, "b": 0, "ff": 128}
        self.pos_gains = {"kp": 300, "ki": 50, "kd": 0, "k": 0, "b": 0, "ff": 0}
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
            device = Device(self.fxs, port, self.baud_rate, self.streaming_freq)
            device.set_controller(self.controller_type)
            device.set_gains(**gains)
            self._high_speed(device)
            device.send_motor_command(fxe.FX_NONE, 0)
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
            # pylint: disable=C0103
            f = self.signal_freq
        else:
            f = 1  # pylint: disable=C0103
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
            data = device.read_device()
            pos0 = data.mot_ang
        else:
            pos0 = 0

        self.i = 0
        for rep in range(self.n_loops):
            elapsed_time = time() - self.start_time
            fxu.print_loop_count_and_time(rep, self.n_loops, elapsed_time)

            # pylint: disable=W0631
            for sample in self.samples:
                sleep(self.dt)
                if device.controller_type != fxe.HSS_CURRENT:
                    sample = sample + pos0

                # Read
                begin_time = time()
                data = device.read_device()
                self.plot_data["dev_read_command_times"].append(time() - begin_time)

                # Write
                begin_time = time()
                device.send_motor_command(device.controller, sample)
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
                    data = device.read_device()

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
