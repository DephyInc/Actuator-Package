"""
Demo 5: High Speed

Runs the motor at a high speed, demonstrating how to:

    * Control which version of the pre-compiled C library is used
"""
# pylint: disable=duplicate-code

import platform
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


# Instantiate and connect to the device; see demo1.py
# Here we see that we can change which version of the pre-compiled C
# library is used by passing in a semantic version string to the
# `cLibVersion` keyword argument
device = Device(cLibVersion="9.1.0")
device.open()


# Start streaming; see demo2.py
frequency = 100
device.start_streaming(frequency)


# Set gains; see demo2.py
gains = {
    "kp": 40,
    "ki": 400,
    "kd": 0,
    "k": 0,
    "b": 0,
    "ff": 128,
}
device.set_gains(**gains)


# Generate current values to command following a sine wave
waveAmplitude = 500
waveFrequency = 5
commandFrequency = 500

nSamples = int(commandFrequency / waveFrequency)
x = np.linspace(-np.pi, np.pi, nSamples)
currents = waveAmplitude * np.sin(x)


# Loop over the currents several times
nLoops = 4
commandDelay = 1 / commandFrequency
cycleDelay = 0.1

measuredCurrent = []
desiredCurrent = []
deviceTime = []

for _ in range(nLoops):
    for current in currents:
        sleep(commandDelay)

        data = device.read()

        measuredCurrent.append(data["mot_cur"])
        desiredCurrent.append(current)
        deviceTime.append(data["state_time"])

        device.command_motor_current(int(current))

        # Delay between cycles
        for __ in range(int(cycleDelay / commandDelay)):
            sleep(commandDelay)

            data = device.read()

            measuredCurrent.append(data["mot_cur"])
            desiredCurrent.append(current)
            deviceTime.append(data["state_time"])


# Plot; see demo2.py
nValues = len(deviceTime)
t = np.concatenate((deviceTime, deviceTime))
currentType = ["Desired Current"] * nValues + ["Measured Current"] * nValues
current = np.concatenate((desiredCurrent, measuredCurrent))

data = {
    "Time (ms)": t,
    "Current Type": currentType,
    "Current (mA)": current,
}

df = pd.DataFrame(data)

plot = sns.relplot(
    data=df, x="Time (ms)", y="Current (mA)", hue="Current Type", kind="line"
)

plot.figure.savefig("high_speed.png")

print("Data plot saved as: 'high_speed.png'")
