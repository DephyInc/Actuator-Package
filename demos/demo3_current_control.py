"""
Demo 3: Current Control

Here we loop over an array of currents, demonstrating how to:

    * Command the motor current
    * Command the motor to stop
    * Print device data
"""

# pylint: disable=duplicate-code

import platform
import subprocess as sub
import sys
from time import sleep

import numpy as np

from flexsea.device import Device


# ============================================
#                   clear
# ============================================
def clear() -> None:
    if platform.system().lower() == "windows":
        # https://stackoverflow.com/a/24306385/8087342
        # Solves Issue #116
        sub.run(["cls"], check=True, shell=True)
    else:
        sub.run(["clear"], check=True)


if "windows" == platform.system().lower():
    msg = "WARNING: these demos may not function properly on Windows "
    msg += "due to the way the OS handles timing. They are best run on "
    msg += "linux."
    print(msg)

confirmed = input("Please power cycle the device before continuing. Then hit 'y'")
if confirmed.lower() != "y":
    print("Quitting.")
    sys.exit(1)


# Instantiate and connect to device; see demo1.py
firmwareVersion = input("Please enter firmwareVersion: ")
port = input("Please enter the device port: ")
device = Device(port=port, firmwareVersion=firmwareVersion)
device.open()


# Start streaming; see demo2.py
frequency = 100
device.start_streaming(frequency)


# Set device gains; see demo2.py
gains = {
    "kp": 40,
    "ki": 400,
    "kd": 0,
    "k": 0,
    "b": 0,
    "ff": 0,
}
device.set_gains(**gains)


# Create the array of currents we want to loop over (in milliamps)
maxCurrent = 1000
nCurrents = 50
currents = np.linspace(0, maxCurrent, nCurrents)


# Ramp up over the desired currents, hold, then ramp back down
commandDelay = 0.1
holdTime = 3

for current in currents:
    # We set the current with the `command_motor_current` method, which
    # takes in the desired current in milliamps
    device.command_motor_current(int(current))
    sleep(commandDelay)
    # There are two ways to print device data: we can either call the
    # `print` method to print the most recent data, or we can call the
    # `print` method with a data dictionary passed as an argument in
    # order to print the data dictionary instead of the most recent
    # data
    device.print()
    clear()

sleep(holdTime)

# During the ramp down phase, we here allow for a keyboard interrupt in
# order to demonstrate how the motor can be manually stopped via the
# `stop_motor` method
try:
    for current in currents[-1::-1]:
        device.command_motor_current(int(current))
        sleep(commandDelay)
        # Here we show the second way of calling `print` in order to
        # easily print data that was read at some point in the past
        data = device.read()
        device.print(data)
        clear()
except KeyboardInterrupt:
    device.stop_motor()
    sleep(commandDelay)

device.stop_motor()
device.close()
