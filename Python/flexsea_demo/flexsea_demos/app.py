"""
app.py

Contains the CLI Application class.
"""
from cleo import Application

from flexsea_demos.commands.bootloader import BootloaderCommand
from flexsea_demos.commands.current_control import CurrentControlCommand
from flexsea_demos.commands.find_poles import FindPolesCommand
from flexsea_demos.commands.get_version import VersionCommand
from flexsea_demos.commands.high_speed import HighSpeedCommand
from flexsea_demos.commands.high_stress import HighStressCommand
from flexsea_demos.commands.impedance_control import ImpedanceControlCommand
from flexsea_demos.commands.leader_follower import LeaderFollowerCommand
from flexsea_demos.commands.open_control import OpenControlCommand
from flexsea_demos.commands.position_control import PositionControlCommand
from flexsea_demos.commands.read_only import ReadOnlyCommand
from flexsea_demos.commands.two_dev_pos_control import TwoDevPositionCommand
from flexsea_demos.commands.two_position_control import TwoPositionCommand
from flexsea_demos.utils import ApplicationConfig


# ============================================
#            FlexseaDemoApplication
# ============================================
class FlexseaDemoApplication(Application):
	"""
	Defines the base `run_demos` command and adds each demo as a
	subcommand.
	"""

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__(config=ApplicationConfig())
		self._get_commands()

	# -----
	# _get_commands
	# -----
	def _get_commands(self):
		command_list = [
			ReadOnlyCommand,
			OpenControlCommand,
			CurrentControlCommand,
			ImpedanceControlCommand,
			PositionControlCommand,
			TwoPositionCommand,
			HighSpeedCommand,
			HighStressCommand,
			LeaderFollowerCommand,
			TwoDevPositionCommand,
			VersionCommand,
			BootloaderCommand,
			FindPolesCommand,
		]
		for command in command_list:
			self.add(command())
