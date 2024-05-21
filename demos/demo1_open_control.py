"""
Demo 1: Open control

Here we loop over an array of voltages, demonstrating how to:

    * Instantiate the Device class
    * Establish a connection between the device and the computer
    * Command the motor voltage
    * Clean up once we're done
"""

# pylint: disable=duplicate-code

import platform
import sys
from time import sleep

import numpy as np

from flexsea.device import Device


if "windows" == platform.system().lower():
    msg = "WARNING: these demos may not function properly on Windows "
    msg += "due to the way the OS handles timing. They are best run on "
    msg += "linux."
    print(msg)


confirmed = input("Please power cycle the device before continuing. Then hit 'y'")
if confirmed.lower() != "y":
    print("Quitting.")
    sys.exit(1)

# We begin by creating an instance of the Device class. It will
# use a default value for the baud rate and log level. The C library
# version and device port must be manually specified.
firmwareVersion = input("Please enter the firmware version: ")
port = input("Please enter the device port: ")
device = Device(port=port, firmwareVersion=firmwareVersion)


# Once instantiated, we have to establish a connection between the
# computer and the device
device.open()


# Generate the array of voltages (millivolts) to loop over
maxVoltage = 3000
nVoltages = 10
voltages = np.linspace(0, maxVoltage, nVoltages)


# Ramp up and down the voltages several times
nCycles = 5

for _ in range(nCycles):
    # Ramp up
    for voltage in voltages:
        # We use the command_motor_voltage method to set the voltage
        device.command_motor_voltage(int(voltage))
        # We now perform a brief sleep in order to give the device time
        # to process and execute our command
        sleep(0.1)

    # Ramp down
    for voltage in voltages[-1::-1]:
        device.command_motor_voltage(int(voltage))
        sleep(0.1)


# Once we're done using the device, we should clean up by calling the
# close method
device.stop_motor()
device.close()
