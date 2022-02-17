"""
position_control.py

Implements the position control demo.
"""
from time import sleep
from typing import Dict
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#          PositionControlCommand
# ============================================
class PositionControlCommand(Command):
	"""
	Runs the position control demo.

	position_control
		{paramFile? : Yaml file with demo parameters.}
		{--ports=* : List of device ports. Comma separated. Overrides parameter file.}
		{--baud-rate= : USB baud rate. Overrides parameter file.}
		{--run-time= : Time (s) to run each device. Overrides parameter file.}
		{--gains= : Order: KP,KI,KD,K,B,FF. Comma separated. Overrides parameter file.}
	"""

	# Schema of parameters required by the demo
	required = {"ports": List, "baud_rate": int, "run_time": int, "gains": Dict}

	__name__ = "position_control"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
		self.run_time = 0
		self.gains = {}
		self.n_loops = 0
		self.fxs = None

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Position control demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.n_loops = int(self.run_time / 0.1)
		for port in self.ports:
			input("Press 'ENTER' to continue...")
			device = Device(self.fxs, port, self.baud_rate)
			self._position_control(device)

	# -----
	# _position_control
	# -----
	def _position_control(self, device):
		data = device.read()
		device.print(data)
		initial_angle = data.mot_ang
		device.set_gains(self.gains)
		device.motor(fxe.FX_POSITION, initial_angle)
		for i in range(self.n_loops):
			sleep(0.1)
			fxu.clear_terminal()
			data = device.read()
			current_angle = data.mot_ang
			print("Desired:              ", initial_angle)
			print("Measured:             ", current_angle)
			print(
				"Difference:           ", current_angle - initial_angle, "\n", flush=True,
			)
			device.print(data)
			fxu.print_loop_count(i, self.n_loops)
		device.motor(fxe.FX_NONE, 0)
		sleep(0.5)
		device.close()
