from typing import List

from cleo.application import Application
from cleo.commands.command import Command

from flexsea import __version__

from demos.commands.current_control import CurrentControlCommand


# ============================================
#           FlexseaDemoApplication
# ============================================
class FlexseaDemoApplication(Application):
    """
    The CLI object.
    """

    # -----
    # constructor
    # -----
    def __init__(self) -> None:
        super().__init__("flexsea-demos", __version__)

        for command in self._get_commands():
            self.add(command())

    # -----
    # _get_commands
    # -----
    def _get_commands(self) -> List[Command]:
        """
        Helper method for telling the CLI about the commands available to
        it.

        Returns
        -------
        commandList : List[Command]
            A list of commands available to the CLI.
        """
        commandList = [
            CurrentControlCommand,
        ]

        return commandList
