import argparse
from time import sleep

import numpy as np
import pandas as pd
import seaborn as sns

from flexsea.device import Device


# ============================================
#                     main
# ============================================
def main(
    port: str,
    cLibVersion: str,
    libFile: str,
    offset: int,
    gains: dict,
    runTime: int,
    transitionTime: int,
    commandDelay: int,
    freq: int,
):
    device = Device(port=port, cLibVersion=cLibVersion, libFile=libFile)
    device.open()
    device.start_streaming(freq)

    data = device.read()

    pos0 = data["mot_ang"]
    positions = [pos0, pos0 + offset]

    device.set_gains(**gains)

    positionIndex = 0

    # For plotting
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
            device.command_motor_position(int(positions[positionIndex]))

        sleep(commandDelay)

    device.close()
    plot(measuredPosition, desiredPosition, deviceTime)


# ============================================
#                     plot
# ============================================
def plot(measured, desired, times):
    nValues = len(times)
    t = np.concatenate((times, times))
    positionType = ["Desired Position"] * nValues + ["Measured Position"] * nValues
    position = np.concatenate((desired, measured))

    data = {
        "Time (ms)": t,
        "Position Type": positionType,
        "Motor Position (ticks)": position,
    }

    df = pd.DataFrame(data)

    plot = sns.relplot(
        data=df,
        x="Time (ms)",
        y="Motor Position (ticks)",
        hue="Position Type",
        kind="line",
    )

    plot.figure.savefig("two_position.png")

    print("Data plot saved as: 'two_position.png'")


# ============================================
#                   Run Main
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
        "-o",
        "--offset",
        dest="offset",
        type=int,
        default=1000,
        help="Number of motor ticks to move from initial position.",
    )
    parser.add_argument(
        "-t",
        "--run-time",
        dest="runTime",
        type=int,
        default=10,
        help="Duration of test in seconds.",
    )
    parser.add_argument(
        "--transition-time",
        dest="transitionTime",
        type=int,
        default=2,
        help="Number of seconds between position changes.",
    )
    parser.add_argument(
        "--command-delay",
        dest="commandDelay",
        type=float,
        default=0.1,
        help="Number of seconds to sleep after issuing a motor command.",
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
        "--kp",
        dest="kp",
        type=int,
        default=50,
        help="Proportional gain.",
    )
    parser.add_argument(
        "--ki",
        dest="ki",
        type=int,
        default=0,
        help="Integral gain.",
    )
    parser.add_argument(
        "--kd",
        dest="kd",
        type=int,
        default=0,
        help="Differential gain.",
    )
    parser.add_argument(
        "--k",
        dest="k",
        type=int,
        default=0,
        help="Stiffness gain.",
    )
    parser.add_argument(
        "--b",
        dest="b",
        type=int,
        default=0,
        help="Damping gain.",
    )
    parser.add_argument(
        "--ff",
        dest="ff",
        type=int,
        default=0,
        help="Feed-forward gain.",
    )

    args = parser.parse_args()

    gains = {
        "kp": args.kp,
        "ki": args.ki,
        "kd": args.kd,
        "k": args.k,
        "b": args.b,
        "ff": args.ff,
    }

    main(
        args.port,
        args.cLibVersion,
        args.libFile,
        args.offset,
        gains,
        args.runTime,
        args.transitionTime,
        args.commandDelay,
        args.freq,
    )

    print("Done.")
