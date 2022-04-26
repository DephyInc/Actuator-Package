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
	print("Device",device)
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
		{paramFile? : Yaml file with demo parameters.}
		{--ports=* : List of device ports. Comma separated. Overrides parameter file.}
		{--baud-rate= : USB baud rate. Overrides parameter file.}
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
		#Creating a list to store the device id of the two exos
		device_list = []
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		#self.n_loops = int(self.run_time / 0.1)
		for port in self.ports:
			input("Press 'ENTER' to continue...")
			device = Device(self.fxs, port, self.baud_rate)
			device.set_gains(self.gains)
			device_list.append(device)

		self._current_control(device_list)

	# -----
	# _current_control
	# -----
	def _current_control(self, device_list):
		while True:
			try:
				for device in device_list:
					sleep(0.5)
					_ramp(device, self.hold_current)

			except KeyboardInterrupt:
				print('Ctrl-C detected, Exiting Gracefully')
				break

		for device in device_list:
			for i in range(self.ramp_down_steps):
				current = self.hold_current * (self.ramp_down_steps - i) / self.ramp_down_steps
				_ramp(device, current)
			sleep(0.5)
			device.close()
