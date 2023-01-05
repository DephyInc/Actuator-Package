from cleo.helpers import option
from flexsea.device import Device
from numpy import linspace
from time import sleep

from .base_command import BaseDemoCommand


# ============================================
#           CurrentControlCommand
# ============================================
class CurrentControlCommand(BaseDemoCommand):
    name = "current_control"

    description = "Ramps up to the given current and then back down."

    help = """
    Ramps up to the desired current and then back down again. Demonstrates how to
    control the motor current.

    Examples
    --------
    flexsea-demos current_control -i <current>
    """

    # -----
    # __new__
    # -----
    def __new__(cls):
        obj = super().__new__(cls)
        obj.options.append(
            option(
                "current",
                "-i",
                "Peak motor current to reach in milliamps.",
                False,
                default=1000,
            )
        )
        return obj

    # -----
    # handle
    # -----
    def handle(self) -> int:
        """
        Entry point for the command.
        """
        self.setup()

        gLabels = ["kp", "ki", "kd", "k", "b", "ff"]
        g = self.option("gains")

        if g:
            gains = dict(zip(gLabels, map(int, g.split(","))))
        else:
            gains = dict(zip(gLabels, [40, 400, 0, 0, 0, 128]))

        nCurrents = 2
        currents = linspace(0, self.option("current"), nCurrents)

        rampTime = self._loopTime / 2
        holdTime = rampTime / nCurrents

        for device in self._devices:
            device.set_gains(**gains)

            data = device.read()
            msg = f"Device: {device.deviceId}\n"
            msg += f"Desired (mA):    {currents[0]}\n"
            msg += f"Measured (mA):   {data['mot_cur']}\n"
            msg += f"Difference (mA): {data['mot_cur'] - currents[0]}"
            self.write(msg)

            for current in currents:
                self._ramp(int(current), device, holdTime)
            for current in currents[-1::-1]:
                self._ramp(int(current), device, holdTime)

        self.line("")
        self.cleanup()

        return 0

    # -----
    # _ramp
    # -----
    def _ramp(self, current: int, device: Device, holdTime: float) -> None:
        """
        Adjusts the device's current and print's the actual measured
        value for comparison.

        Parameters
        ----------
        current : int
            The value to set the motor current to.

        device : Device
            The class representing the device being controlled.

        holdTime : float
            The length of time to stay at the given current.
        """
        device.command_motor_current(current)
        sleep(holdTime)
        data = device.read()

        msg = f"Device: {device.deviceId}\n"
        msg += f"Desired (mA):    {current}\n"
        msg += f"Measured (mA):   {data['mot_cur']}\n"
        msg += f"Difference (mA): {data['mot_cur'] - current}"

        self.overwrite(msg)
