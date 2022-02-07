from time import sleep
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#            TwoDevPositionCommand
# ============================================
class TwoDevPositionCommand(Command):
	"""
	Runs the two devices position control demo.

	two_devices_position_control
		{paramFile : Yaml file with demo parameters.}
	"""

	# Schema of parameters required by the demo
	required = {"ports": List, "baud_rate": int, "run_time": int}

	__name__ = "two_devices_position_control"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
		self.run_time = 0
		self.nLoops = 0
		self.devices = []
		self.fxs = None
		self.gains = {"KP": 50, "KI": 3, "KD": 0, "K": 0, "B": 0, "FF": 0}
		self.off_gains = {"KP": 0, "KI": 0, "KD": 0, "K": 0, "B": 0, "FF": 0}

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Runs the two devices position control demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.nLoops = int(self.run_time / 0.1)

		try:
			assert len(self.ports) == 2
		except AssertionError:
			raise AssertionError(f"Need two devices. Got: '{len(self.ports)}'")

		for i in range(2):
			self.devices.append(Device(self.fxs, self.ports[i], self.baud_rate))
			self.devices[i].set_gains(self.gains)
			self.devices[i].motor(fxe.FX_POSITION, self.devices[i].initial_pos)

		self._two_devices_position_control()

		print("Turning off position control...")
		for i in range(2):
			self.devices[i].set_gains(self.off_gains)
			self.devices[i].motor(fxe.FX_NONE, 0)
			sleep(0.5)
			self.devices[i].close()

	# -----
	# _two_devices_position_control
	# -----
	def _two_devices_position_control(self):
		for i in range(self.nLoops):
			sleep(0.1)
			fxu.clear_terminal()

			for j in range(2):
				cur_pos = self.devices[j].get_pos()
				pos0 = self.devices[j].initial_pos

				print(f"Device {j}:\n---------\n")
				print(f"Desired:              {pos0}")
				print(f"Measured:             {cur_pos}")
				print(f"Difference:           {cur_pos - pos0}\n")
				self.devices[j].print()

				fxu.print_loop_count(i, self.nLoops)
