"""
open_control.py

Implements the open control demo.
"""
from time import sleep
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#                _ramp_device
# ============================================
def _ramp_device(device, voltage):
	"""
	Boilerplate for stepping through voltages.

	Parameters
	----------
	device : flexsea_demos.device.Device
		Object that manages the device information and state.

	voltage : float
		The voltage to set.
	"""
	sleep(0.1)
	device.motor(fxe.FX_VOLTAGE, voltage)
	fxu.clear_terminal()
	device.print()


# ============================================
#              OpenControlCommand
# ============================================
class OpenControlCommand(Command):
	"""
	Implements the open control demo.

	open_control
		{paramFile? : Yaml file with demo parameters.}
		{--ports=* : List of device ports. Comma separated. Overrides parameter file.}
		{--baud-rate= : USB baud rate. Overrides parameter file.}
        {--streaming-freq= : Frequency (Hz) for device to stream data.}
		{--run-time= : Time (s) to run each device. Overrides parameter file.}
		{--n-cycles= : Number of times to ramp each device. Overrides parameter file.}
		{--max-voltage= : Peak voltage to use (mV). Overrides parameter file.}
	"""

	# Schema of parameters required by the demo
	required = {
		"ports": List,
		"baud_rate": int,
        "streaming_freq" : int,
		"run_time": int,
		"n_cycles": int,
		"max_voltage": int,
	}

	__name__ = "open_control"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
        self.streaming_freq = None
		self.run_time = 0
		self.n_cycles = 0
		self.max_voltage = 0
		self.fxs = None
		self.voltages = []

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Runs the open_control demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self._get_voltages()
		for port in self.ports:
			input("Press 'ENTER' to continue...")
			device = Device(self.fxs, port, self.baud_rate, self.streaming_freq)
			self._open_control(device)

	# -----
	# _get_voltages
	# -----
	def _get_voltages(self):
		"""
		Generates the list of voltages to step through.
		"""
		cycle_time = self.run_time / float(self.n_cycles)
		step_count = int((cycle_time / 2) / 0.1)
		# pylint: disable=C0103
		for s in range(step_count):
			self.voltages.append(-1 * self.max_voltage * (s * 1.0 / step_count))

	# -----
	# _open_control
	# -----
	def _open_control(self, device):
		print(f"Setting open control for device {device.dev_id}...")
		device.motor(fxe.FX_VOLTAGE, 0)
		sleep(0.5)

		for rep in range(self.n_cycles):
			# Ramp-up
			print(f"Ramping up motor voltage {rep}...\n")
			for voltage in self.voltages:
				_ramp_device(device, voltage)
			# Ramp-down
			print(f"Ramping down motor voltage {rep}...\n")
			for voltage in self.voltages[-1::-1]:
				_ramp_device(device, voltage)

		device.motor(fxe.FX_NONE, 0)
		sleep(0.1)
		device.close()
