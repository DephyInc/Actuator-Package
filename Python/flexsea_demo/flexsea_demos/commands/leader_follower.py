"""
leader_follower.py

Implements the leader-follower demo.
"""
from time import sleep
from typing import List

from cleo import Command
from flexsea import fxEnums as fxe
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#          LeaderFollowerCommand
# ============================================
class LeaderFollowerCommand(Command):
	"""
	Runs the leader follower demo.

	leader_follower
		{paramFile? : Yaml file with demo parameters.}
		{--ports=* : List of device ports. Comma separated. Overrides parameter file.}
		{--baud_rate= : USB baud rate. Overrides parameter file.}
		{--run_time= : Time (s) to run each device. Overrides parameter file.}
	"""

	# pylint: disable=too-many-instance-attributes

	# Schema of parameters required by the demo
	required = {"ports": List, "baud_rate": int, "run_time": int}

	__name__ = "leader_follower"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
		self.run_time = 0
		self.n_loops = 0
		self.devices = []
		self.loop_delay = 0.05
		self.fxs = None
		self.leader_gains = {"KP": 40, "KI": 400, "KD": 0, "K": 0, "B": 0, "FF": 128}
		self.follower_gains = {"KP": 100, "KI": 1, "KD": 0, "K": 0, "B": 0, "FF": 0}
		self.off_gains = {"KP": 0, "KI": 0, "KD": 0, "K": 0, "B": 0, "FF": 0}

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Runs the read_only demo. The first port given is the leader.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.n_loops = int(self.run_time / self.loop_delay)

		try:
			assert len(self.ports) == 2
		except AssertionError as err:
			raise AssertionError(f"Need two devices. Got: '{len(self.ports)}'") from err

		for i in range(2):
			self.devices.append(Device(self.fxs, self.ports[i], self.baud_rate))

		# Set first device to current controller with 0 current (0 torque)
		self.devices[0].set_gains(self.leader_gains)
		self.devices[0].motor(fxe.FX_CURRENT, 0)

		# Set position controller for second device
		self.devices[1].set_gains(self.follower_gains)
		self.devices[1].motor(fxe.FX_POSITION, self.devices[1].initial_pos)

		self._leader_follower()

		print("Turning off position control...")
		for i in range(2):
			self.devices[i].set_gains(self.off_gains)
			self.devices[i].motor(fxe.FX_NONE, 0)
			sleep(0.5)
			self.devices[i].close()

	# -----
	# _leader_follower
	# -----
	def _leader_follower(self):
		leader_pos0 = self.devices[0].initial_pos
		follower_pos0 = self.devices[1].initial_pos

		leader_id = self.devices[0].dev_id
		follower_id = self.devices[1].dev_id

		for i in range(self.n_loops):
			sleep(self.loop_delay)
			fxu.clear_terminal()

			leader_data = self.devices[0].read()

			diff = leader_data.mot_ang - leader_pos0

			self.devices[1].motor(fxe.FX_POSITION, follower_pos0 + diff)

			print(f"Device {follower_id} following device {leader_id}\n")
			self.devices[1].print()
			print("")
			self.devices[0].print()
			fxu.print_loop_count(i, self.n_loops)
