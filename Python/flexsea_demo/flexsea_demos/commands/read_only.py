"""
read_only.py

Implements the read only demo.
"""
from time import sleep
from typing import List

from cleo import Command
from flexsea import fx_utils as fxu
from flexsea.flexsea import Device

from flexsea_demos.utils import setup


# ============================================
#              ReadOnlyCommand
# ============================================
class ReadOnlyCommand(Command):
	"""
	Reads device data and prints it to the screen.

	read_only
		{paramFile? : Yaml file with demo parameters.}
		{--ports=* : List of device ports. Comma separated. Overrides parameter file.}
		{--baud-rate= : USB baud rate. Overrides parameter file.}
		{--streaming-freq= : Frequency (Hz) for device to stream data.}
		{--run-time= : Time (s) to run each device. Overrides parameter file.}
	"""

	# Schema of parameters required by the demo
	required = {"ports": List, "baud_rate": int, "streaming_freq": int, "run_time": int}

	__name__ = "read_only"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
		self.streaming_freq = None
		self.run_time = 0
		self.n_loops = 0

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Runs the read_only demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.n_loops = int(self.run_time / 0.1)
		for port in self.ports:
			input("Press 'ENTER' to continue...")
			device = Device(port, self.baud_rate)
			device.open(self.streaming_freq)
			self._read_only(device)

	# -----
	# _read_only
	# -----
	def _read_only(self, device):
		"""
		Reads FlexSEA device and prints gathered data.

		Parameters
		----------
		device : flexsea_demos.device.Device
			Object that manages the device information and state.
		"""
		for i in range(self.n_loops):
			fxu.print_loop_count(i, self.n_loops)
			sleep(0.1)
			fxu.clear_terminal()
			device.print()
		device.close()
