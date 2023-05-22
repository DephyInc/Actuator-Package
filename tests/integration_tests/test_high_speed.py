# pylint: disable=duplicate-code

import argparse
from time import sleep

import numpy as np
from numpy.random import default_rng
from utils import plot  # pylint: disable=import-error

from flexsea.device import Device


# ============================================
#                    main
# ============================================
def main(  # pylint: disable=too-many-locals
    port: str,
    cLibVersion: str,
    libFile: str,
    freq: int,
    gains: dict,
    waveAmplitude: int,
    waveFrequency: int,
    commandFrequency: int,
    nLoops: int,
    cycleDelay: float,
):
    device = Device(port=port, firmwareVersion=cLibVersion, libFile=libFile)
    device.open()

    device.start_streaming(freq)

    gains = {
        "kp": 40,
        "ki": 400,
        "kd": 0,
        "k": 0,
        "b": 0,
        "ff": 128,
    }
    device.set_gains(**gains)

    nSamples = int(commandFrequency / waveFrequency)
    x = np.linspace(-np.pi, np.pi, nSamples)
    currents = waveAmplitude * np.sin(x)

    commandDelay = 1.0 / commandFrequency

    measuredCurrent = []
    desiredCurrent = []
    deviceTime = []

    for _ in range(nLoops):
        for current in currents:
            sleep(commandDelay)

            data = device.read()

            device.command_motor_current(int(current))

            measuredCurrent.append(data["mot_cur"])
            desiredCurrent.append(current)
            deviceTime.append(data["state_time"])

            # Delay between cycles
            for __ in range(int(cycleDelay / commandDelay)):
                sleep(commandDelay)

                data = device.read()

                measuredCurrent.append(data["mot_cur"])
                desiredCurrent.append(current)
                deviceTime.append(data["state_time"])

    device.close()
    print("Plotting...")
    # There's a long stretch of nothing before the demo gets going, so we
    # skip that for plotting. This is because the first several currents are small
    index = np.where(np.array(measuredCurrent) > 0)[0][0]
    des = np.array(desiredCurrent[index:])
    meas = np.array(measuredCurrent[index:])
    t = np.array(deviceTime[index:])
    # Plotting can be slow where there's a lot of data, so we use a fraction of it
    rng = default_rng()
    n = len(des) // 6
    indices = rng.choice(np.arange(0, len(des), 1), n)
    desSample = des[indices]
    measSample = meas[indices]
    tSample = t[indices]
    plot(desSample, measSample, tSample, "Current (mA)", "high_speed.png")


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
        "--kp",
        dest="kp",
        type=int,
        default=40,
        help="Proportional gain.",
    )
    parser.add_argument(
        "--ki",
        dest="ki",
        type=int,
        default=400,
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
        default=128,
        help="Feed-forward gain.",
    )
    parser.add_argument(
        "--wave-frequency",
        dest="waveFrequency",
        type=int,
        default=5,
        help="Frequency of the sine wave for the motor currents.",
    )
    parser.add_argument(
        "--wave-amplitude",
        dest="waveAmplitude",
        type=int,
        default=500,
        help="Amplitude of the sine wave for the motor currents.",
    )
    parser.add_argument(
        "--command-frequency",
        dest="commandFrequency",
        type=int,
        default=500,
        help="Reciprocal of the time between motor commands.",
    )
    parser.add_argument(
        "--n-loops",
        dest="nLoops",
        type=int,
        default=1,
        help="Number of times to iterate.",
    )
    parser.add_argument(
        "--cycle-delay",
        dest="cycleDelay",
        type=float,
        default=0.1,
        help="Delay between loops.",
    )

    args = parser.parse_args()

    gains_dict = {
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
        args.freq,
        gains_dict,
        args.waveAmplitude,
        args.waveFrequency,
        args.commandFrequency,
        args.nLoops,
        args.cycleDelay,
    )

    print("Done.")
