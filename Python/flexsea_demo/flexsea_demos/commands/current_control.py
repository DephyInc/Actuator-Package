"""
current_control.py

Implements the current control demo.
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
#                  _ramp
# ============================================
def _ramp(device, current):
	"""
	Adjusts the device's current and print's the actual measured
	value for comparison.
	"""
	device.motor(fxe.FX_CURRENT, current)
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
		{paramFile : Yaml file with demo parameters.}
	"""

	# pylint: disable=too-many-instance-attributes

	# Schema of parameters required by the demo
	required = {
		"ports": List,
		"baud_rate": int,
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
		self.run_time = 0
		self.gains = {}
		self.hold_current = 0
		self.ramp_down_steps = 0
		self.n_loops = 0
		self.fxs = None

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Current control demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.n_loops = int(self.run_time / 0.1)
		for port in self.ports:
			input("Press 'ENTER' to continue...")
			device = Device(self.fxs, port, self.baud_rate)
			device.set_gains(self.gains)
			sleep(0.5)
			self._current_control(device)

	# -----
	# _current_control
	# -----
	def _current_control(self, device):
		for _ in range(self.n_loops):
			_ramp(device, self.hold_current)
		for i in range(self.ramp_down_steps):
			current = self.hold_current * (self.ramp_down_steps - i) / self.ramp_down_steps
			_ramp(device, current)
		device.motor(fxe.FX_NONE, 0)
		sleep(0.5)
		device.close()
