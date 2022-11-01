"""
app.py

Contains the CLI Application class.
"""
from cleo import Application

from .commands.current_control import CurrentControlCommand
from .commands.find_poles import FindPolesCommand
from .commands.high_speed import HighSpeedCommand
from .commands.high_stress import HighStressCommand
from .commands.impedance_control import ImpedanceControlCommand
from .commands.leader_follower import LeaderFollowerCommand
from .commands.open_control import OpenControlCommand
from .commands.position_control import PositionControlCommand
from .commands.read_only import ReadOnlyCommand
from .commands.two_position_control import TwoPositionCommand
from .utils import ApplicationConfig


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
            CurrentControlCommand,
            FindPolesCommand,
            HighSpeedCommand,
            HighStressCommand,
            ImpedanceControlCommand,
            LeaderFollowerCommand,
            OpenControlCommand,
            PositionControlCommand,
            ReadOnlyCommand,
            TwoPositionCommand,
        ]
        for command in command_list:
            self.add(command())
