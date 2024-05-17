"""
Demo 4: Impedance Control

Oscillates between two different positions by controlling the motor's
impedance, demonstrating how to:

    * Command motor impedance
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


# Start streaming; see demo2.py
frequency = 100
device.start_streaming(frequency)


# Read from the device; see demo2.py
data = device.read()


# Set positions
offset = 1000
pos0 = data["mot_ang"]
positions = [pos0, pos0 + offset]


# Set gains; see demo2.py
gains = {
    "kp": 40,
    "ki": 400,
    "kd": 0,
    "k": 600,
    "b": 300,
    "ff": 128,
}
device.set_gains(**gains)


# Move between the two positions; see demo2.py
runTime = 10
transitionTime = 0.8
commandDelay = 0.02
positionIndex = 0
bGainDelta = 150

measuredPosition = []
desiredPosition = []
deviceTime = []

nLoops = int(runTime / commandDelay)
transitionSteps = int(transitionTime / commandDelay)

for i in range(nLoops):
    data = device.read()

    measuredPosition.append(data["mot_ang"])
    deviceTime.append(data["state_time"])
    desiredPosition.append(positions[positionIndex])

    if i % transitionSteps == 0:
        gains["b"] += bGainDelta
        device.set_gains(**gains)
        positionIndex = (positionIndex + 1) % len(positions)
        # Here we command the motor impedance via the
        # `command_motor_impedance` method, which takes in a motor
        # position in ticks
        device.command_motor_impedance(int(positions[positionIndex]))

    sleep(commandDelay)

device.stop_motor()
device.close()


# Plot; see demo2.py
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

plot.figure.savefig("impedance_demo.png")

print("Data plot saved as: 'impedance_demo.png'")
