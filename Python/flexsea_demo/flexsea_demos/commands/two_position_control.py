"""
two_position_control.py

Implements the two-position control demo.
"""
from time import sleep
from time import time
from typing import Dict
from typing import List

from cleo import Command
from flexsea import fx_enums as fxe
from flexsea import fx_utils as fxu
from flexsea.flexsea import Device
import matplotlib
import matplotlib.pyplot as plt

from flexsea_demos.utils import setup


# ============================================
#             TwoPositionCommand
# ============================================
class TwoPositionCommand(Command):
	"""
	Runs the two position control demo.

	two_position_control
		{paramFile? : Yaml file containing the parameters for the demo.}
		{--ports=* : List of device ports. Comma separated. Overrides parameter file.}
		{--baud-rate= : USB baud rate. Overrides parameter file.}
		{--streaming-freq= : Frequency (Hz) for device to stream data.}
		{--run-time= : Time (s) to run each device. Overrides parameter file.}
		{--delta= : Offset from initial position. Overrides parameter file.}
		{--transition-time= : Time (s) between positions. Overrides parameter file.}
		{--gains= : Order: KP,KI,KD,K,B,FF. Comma separated. Overrides parameter file.}
	"""

	# pylint: disable=too-many-instance-attributes

	# Schema of parameters required by the demo
	required = {
		"ports": List,
		"baud_rate": int,
		"streaming_freq": int,
		"run_time": int,
		"delta": int,
		"transition_time": float,
		"gains": Dict,
	}

	__name__ = "two_position_control"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
		self.streaming_freq = None
		self.run_time = 0
		self.delta = 0
		self.transition_time = 0.0
		self.gains = {}
		self.plot_data = {"times": [], "requests": [], "measurements": []}
		self.n_loops = 0
		self.transition_steps = 0
		self.start_time = 0

		matplotlib.use("WebAgg")
		if fxu.is_pi():
			matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Runs the two position control demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.n_loops = int(self.run_time / 0.1)
		self.transition_steps = int(self.transition_time / 0.1)

		for port in self.ports:
			input("Press 'ENTER' to continue...")
			device = Device(port, self.baud_rate)
			device.open(self.streaming_freq)
			self._reset_plot()
			self._two_position_control(device)
			device.send_motor_command(fxe.FX_VOLTAGE, 0)
			self._plot()
			device.close()

	# -----
	# _two_position_control
	# -----
	def _two_position_control(self, device):
		data = device.read_device()
		initial_angle = data.mot_ang
		positions = [initial_angle, initial_angle + self.delta]
		current_pos = 0

		device.set_gains(**self.gains)
		device.send_motor_command(fxe.FX_POSITION, initial_angle)
		self.start_time = time()

		for i in range(self.n_loops):
			sleep(0.1)
			data = device.read_device()
			fxu.clear_terminal()
			measured_pos = data.mot_ang
			print(f"Desired:              {positions[current_pos]}")
			print(f"Measured:             {measured_pos}")
			print(f"Difference:           {(measured_pos - positions[current_pos])}\n")
			device.print(data)

			if i % self.transition_steps == 0:
				current_pos = (current_pos + 1) % len(positions)
				device.send_motor_command(fxe.FX_POSITION, positions[current_pos])

			self.plot_data["times"].append(time() - self.start_time)
			self.plot_data["requests"].append(positions[current_pos])
			self.plot_data["measurements"].append(measured_pos)

	# -----
	# _plot
	# -----
	def _plot(self):
		plt.title("Two Position Control Demo")
		plt.plot(
			self.plot_data["times"],
			self.plot_data["requests"],
			color="b",
			label="Desired position",
		)
		plt.plot(
			self.plot_data["times"],
			self.plot_data["measurements"],
			color="r",
			label="Measured position",
		)
		plt.xlabel("Time (s)")
		plt.ylabel("Encoder position")
		plt.legend(loc="upper right")
		fxu.print_plot_exit()
		plt.show()

	# -----
	# _reset_plot
	# -----
	def _reset_plot(self):
		self.plot_data = {"times": [], "requests": [], "measurements": []}
		plt.clf()
