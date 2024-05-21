"""
Demo 2: Two position control

Here we demonstrate how to:
    * Command motor position
    * Read data from the device
    * Set the motor gains
"""

# pylint: disable=duplicate-code

import platform
import sys
from time import sleep

import numpy as np
import pandas as pd
import seaborn as sns

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

# Instantiate and connect to the device; see demo1.py
firmwareVersion = input("Please enter firmwareVersion: ")
port = input("Please enter the device port: ")
device = Device(port=port, firmwareVersion=firmwareVersion)
device.open()


# In order to read data from the device, we have to instruct the device
# to send its data to the computer via the `start_streaming` method.
# This method takes in the frequency (in hertz) at which you would like
# the device to send data
frequency = 100
device.start_streaming(frequency)


# Once streaming, we use the `read` method. This method returns a
# dictionary. The fields available in the dictionary depend on the
# device being read as well as the firmware version
data = device.read()


# In this demo we are going to command the motor to move between two
# positions: the initial position and then the initial position plus
# some offset. The motor position is given in "ticks", and the
# conversion between ticks and degrees depends on the device. For an
# actpack, the conversion is 360 degrees = 16384 ticks
offset = 1000
pos0 = data["mot_ang"]
positions = [pos0, pos0 + offset]


# In order for the motor to move properly, we have to set the gains.
# The exact values of the gains depends on the device and the
# application, but here we are assuming that an actpack under no load
# is being used. The gains are set via the `set_gains` method, which
# expects the gains to be given in the following order: proportional,
# integral, differential, stiffness (impedance), damping (impedance),
# and feed-forward
gains = {
    "kp": 50,
    "ki": 0,
    "kd": 0,
    "k": 0,
    "b": 0,
    "ff": 0,
}
device.set_gains(**gains)


# Now we can command the motor to oscillate between the two positions
# several times. This is done by specifying how long we want the demo
# to last for (in seconds), how long we want to wait between position
# swaps (in seconds), and how long we want to wait between device
# reads. This allows us to finely sample the device's data for plotting
# purposes
runTime = 10
transitionTime = 2
commandDelay = 0.1
positionIndex = 0

measuredPosition = []
desiredPosition = []
deviceTime = []

nLoops = int(runTime / commandDelay)
transitionSteps = int(transitionTime / commandDelay)

# Oscillate between the two positions nLoops times
for i in range(nLoops):
    data = device.read()

    # Save the data for plotting
    measuredPosition.append(data["mot_ang"])
    desiredPosition.append(positions[positionIndex])
    deviceTime.append(data["state_time"])

    # Every transitionTime seconds, we go to the next position
    if i % transitionSteps == 0:
        positionIndex = (positionIndex + 1) % len(positions)
        # Here we tell the motor which position to move to, with the
        # value we give it in ticks
        device.command_motor_position(int(positions[positionIndex]))

    # Wait the desired amount of time for the device to process and
    # complete the command
    sleep(commandDelay)

device.stop_motor()
device.close()


# Now we can plot the data to see how well the measured motor position
# tracked the desired square wave. First we put the data into a
# data frame with three columns: time, position, and position type.
# Position type indicates whether the value in the positio column is
# a measured position or desired position and makes plotting these
# values on the same plot much easier via seaborn's `hue` keyword
nValues = len(deviceTime)
t = np.concatenate((deviceTime, deviceTime))
positionType = ["Desired Position"] * nValues + ["Measured Position"] * nValues
position = np.concatenate((desiredPosition, measuredPosition))

data = {
    "Time (ms)": t,
    "Position Type": positionType,
    "Motor Position (ticks)": position,
}

df = pd.DataFrame(data)

plot = sns.relplot(
    data=df, x="Time (ms)", y="Motor Position (ticks)", hue="Position Type", kind="line"
)

plot.figure.savefig("two_position_demo.png")

print("Data plot saved as: 'two_position_demo.png'")
