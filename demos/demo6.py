"""
Demo 6: High Stress
"""
# pylint: disable=duplicate-code

import platform
from time import sleep
from typing import List

import numpy as np
import pandas as pd
import seaborn as sns

from flexsea.device import Device


# ============================================
#                 send_command
# ============================================
def send_command(
    cmd: dict, cmdType: str, gains: dict, setGains: bool, plotData: dict, device: Device
) -> dict:
    deviceData = device.read()

    if setGains:
        device.set_gains(**gains)

    setPoint = cmd["cur"] if cmdType == "current" else cmd["pos"]

    if cmdType == "current":
        device.command_motor_current(int(setPoint))
    else:
        device.command_motor_position(int(setPoint))

    plotData["stateTime"].append(deviceData["state_time"])
    plotData["desiredPosition"].append(cmd["pos"])
    plotData["measuredPosition"].append(deviceData["mot_ang"])
    plotData["desiredCurrent"].append(cmd["cur"])
    plotData["measuredCurrent"].append(deviceData["mot_cur"])

    return plotData


# ============================================
#                 get_device
# ============================================
def get_device(frequency: int) -> Device:
    device = Device()
    device.open()
    device.start_streaming(frequency)

    return device


# ============================================
#                  get_gains
# ============================================
def get_gains() -> dict:
    positionGains = {
        "kp": 100,
        "ki": 10,
        "kd": 0,
        "k": 0,
        "b": 0,
        "ff": 0,
    }

    currentGains = {
        "kp": 40,
        "ki": 400,
        "kd": 0,
        "k": 0,
        "b": 0,
        "ff": 128,
    }

    gains = {
        "current": currentGains,
        "position": positionGains,
    }

    return gains


# ============================================
#                 get_samples
# ============================================
def get_samples(frequency: int) -> dict:
    # Position samples
    positionAmplitude = 10000
    positionFreq = 1

    nSamples = int(frequency / positionFreq)
    x = np.linspace(-np.pi, np.pi, nSamples)
    positionSamples = positionAmplitude * np.sin(x)

    # Current samples
    currentAmplitude = 1500
    currentFreq = 5

    nSamples = int(frequency / currentFreq)
    x = np.linspace(-np.pi, np.pi, nSamples)
    currentSamples = currentAmplitude * np.sin(x)

    # Current samples: line
    value = 0
    length = 0.5

    nSamples = np.int32(length * frequency)
    currentSamplesLine = np.array([value for _ in range(nSamples)])

    # Samples
    samples = {
        "position": positionSamples,
        "currentSine": currentSamples,
        "currentLine": currentSamplesLine,
    }

    return samples


# ============================================
#                    plot
# ============================================
def plot(time: List, desired: List, measured: List, label: str) -> None:
    nValues = len(time)
    t = np.concatenate((time, time))
    dataType = ["Desired"] * nValues + ["Measured"] * nValues
    data = np.concatenate((desired, measured))

    df = pd.DataFrame({"Time (ms)": t, "Type": dataType, label: data})

    plt = sns.relplot(data=df, x="Time (ms)", y=label, hue="Type", kind="line")

    plt.figure.savefig(f"{label}_demo6.png")


# ============================================
#                    main
# ============================================
def main():  # pylint: disable=too-many-locals
    """
    This demo alternates between a position control loop and a current
    control loop several times in a demanding fashion. The setpoints
    for each controller are generated from two different sine waves.
    """
    if "windows" == platform.system().lower():
        msg = "WARNING: these demos may not function properly on Windows "
        msg += "due to the way the OS handles timing. They are best run on "
        msg += "linux."
        print(msg)

    frequency = 1000
    delay = 1.0 / frequency
    nLoops = 3
    # Factor to determine current on "way back" to starting point
    currentAsymmetricG = 1.15

    # Instantiate the device and start streaming
    device = get_device(frequency)

    # Initialize the gains to be used for each controller
    gains = get_gains()

    # Get the samples for each controller
    samples = get_samples(frequency)

    # Initial device position
    pos0 = device.read()["mot_ang"]

    # Plotting arrays
    data = {
        "stateTime": [],
        "desiredPosition": [],
        "measuredPosition": [],
        "desiredCurrent": [],
        "measuredCurrent": [],
    }

    for i in range(nLoops):
        # Step 0
        sleep(delay)
        if i:
            command = {"cur": 0, "pos": device.read()["mot_ang"]}
        else:
            command = {"cur": 0, "pos": pos0}
        data = send_command(command, "position", gains["position"], True, data, device)

        # Step 1
        if i:
            for sample in np.linspace(data["mot_ang"], pos0, 360):
                command = {"cur": 0, "pos": sample}
                sleep(delay)
                data = send_command(command, "position", {}, False, data, device)

        # Step 2
        for sample in samples["position"]:
            command = {"cur": 0, "pos": sample + pos0}
            sleep(delay)
            data = send_command(command, "position", {}, False, data, device)

        # Step 3
        command = {"cur": 0, "pos": pos0}
        data = send_command(command, "current", gains["current"], True, data, device)
        sleep(delay)

        # Step 4
        for sample in samples["currentSine"].astype(np.int64):
            sleep(delay)
            if sample > 0:
                sample *= currentAsymmetricG
            command = {"cur": sample, "pos": pos0}
            sleep(delay)
            data = send_command(command, "current", {}, False, data, device)

        # Step 5
        for sample in samples["currentLine"]:
            command = {"cur": sample, "pos": pos0}
            sleep(delay)
            data = send_command(command, "current", {}, False, data, device)

    # Clean up
    device.close()

    # Plot data
    times = [data["stateTime"], data["stateTime"]]
    desired = [data["desiredCurrent"], data["desiredPosition"]]
    measured = [data["measuredCurrent"], data["measuredPosition"]]
    labels = ["current", "position"]

    for t, des, meas, label in zip(times, desired, measured, labels):
        plot(t, des, meas, label)


if __name__ == "__main__":
    main()
