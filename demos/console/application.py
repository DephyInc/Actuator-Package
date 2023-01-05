from typing import List

from cleo.application import Application
from cleo.commands.command import Command
from cleo.formatters.style import Style

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

        io = super().create_io(None, None, None)

        # Set our own CLI styles
        formatter = io.output.formatter
        formatter.set_style("c1", Style("cyan"))
        formatter.set_style("c2", Style("default", options=["bold"]))
        formatter.set_style("info", Style("blue"))
        formatter.set_style("comment", Style("green"))
        formatter.set_style("warning", Style("yellow"))
        formatter.set_style("debug", Style("default", options=["dark"]))
        formatter.set_style("success", Style("green"))

        # Dark variants
        formatter.set_style("c1_dark", Style("cyan", options=["dark"]))
        formatter.set_style("c2_dark", Style("default", options=["bold", "dark"]))
        formatter.set_style("success_dark", Style("green", options=["dark"]))

        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        self._io = io

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
