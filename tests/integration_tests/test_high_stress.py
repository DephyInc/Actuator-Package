# pylint: disable=duplicate-code

import argparse
from time import sleep

import numpy as np
from utils import plot  # pylint: disable=import-error

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
#                    main
# ============================================
def main(
    port: str, cLibVersion: str, libFile: str, freq: int, nLoops: int
):  # pylint: disable=too-many-locals
    delay = 1.0 / freq
    # Factor to determine current on "way back" to starting point
    currentAsymmetricG = 1.15

    device = Device(port=port, firmwareVersion=cLibVersion, libFile=libFile)
    device.open()
    device.start_streaming(freq)

    # Initialize the gains to be used for each controller
    gains = get_gains()

    # Get the samples for each controller
    samples = get_samples(freq)

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
        print(f"Loop: {i+1}/{nLoops}")
        # Step 0
        sleep(delay)
        if i:
            command = {"cur": 0, "pos": device.read()["mot_ang"]}
        else:
            command = {"cur": 0, "pos": pos0}
        data = send_command(command, "position", gains["position"], True, data, device)

        # Step 1
        if i:
            currentPos = device.read()["mot_ang"]
            for sample in np.linspace(currentPos, pos0, 360):
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

    device.close()

    # Plot data
    print("Plotting...")
    times = [data["stateTime"], data["stateTime"]]
    desired = [data["desiredCurrent"], data["desiredPosition"]]
    measured = [data["measuredCurrent"], data["measuredPosition"]]
    labels = ["current", "position"]

    for t, des, meas, label in zip(times, desired, measured, labels):
        plot(des, meas, t, label, f"{label}_high_stress.png")


# ============================================
#                  Run Main
# ============================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=str,
        default="",
        help="Serial port device is connected to.",
    )
    parser.add_argument(
        "-c",
        "--clibversion",
        dest="cLibVersion",
        type=str,
        default="",
        help="Semantic version string of the pre-compiled C library.",
    )
    parser.add_argument(
        "-l",
        "--libfile",
        dest="libFile",
        type=str,
        default="",
        help="Path to the pre-compiled C library to use.",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        dest="freq",
        type=int,
        default=100,
        help="Frequency (Hz) at which device will stream data.",
    )
    parser.add_argument(
        "--n-loops",
        dest="nLoops",
        type=int,
        default=4,
        help="Feed-forward gain.",
    )

    args = parser.parse_args()

    main(args.port, args.cLibVersion, args.libFile, args.freq, args.nLoops)

    print("Done.")
