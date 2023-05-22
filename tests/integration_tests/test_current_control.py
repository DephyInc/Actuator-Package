# pylint: disable=duplicate-code

import argparse
from time import sleep

import numpy as np
from utils import clear  # pylint: disable=import-error

from flexsea.device import Device


# ============================================
#                    main
# ============================================
def main(
    port: str,
    cLibVersion: str,
    libFile: str,
    freq: int,
    gains: dict,
    minCurrent: int,
    maxCurrent: int,
    nCurrents: int,
    commandDelay: float,
    holdTime: int,
):
    device = Device(port=port, firmwareVersion=cLibVersion, libFile=libFile)
    device.open()
    device.start_streaming(freq)

    device.set_gains(**gains)

    currents = np.linspace(minCurrent, maxCurrent, nCurrents)

    for i, current in enumerate(currents):
        device.command_motor_current(int(current))
        sleep(commandDelay)
        if i % 5 == 0:
            data = device.read()
            print(f"Desired current: {current}")
            print(f"Measured current: {data['mot_cur']}")
            sleep(2)

    sleep(holdTime)

    try:
        for current in currents[-1::-1]:
            device.command_motor_current(int(current))
            sleep(commandDelay)
            device.print()
            clear()
    except KeyboardInterrupt:
        device.stop_motor()
        sleep(commandDelay)

    device.close()


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
        default=0,
        help="Feed-forward gain.",
    )
    parser.add_argument(
        "--max-current",
        dest="maxCurrent",
        type=int,
        default=1000,
        help="Maximum current to ramp to, in milliamps.",
    )
    parser.add_argument(
        "--min-current",
        dest="minCurrent",
        type=int,
        default=0,
        help="Minium current to start at, in milliamps.",
    )
    parser.add_argument(
        "-n",
        "--n-currents",
        dest="nCurrents",
        type=int,
        default=50,
        help="The number of currents to ramp over.",
    )
    parser.add_argument(
        "--command-delay",
        dest="commandDelay",
        type=float,
        default=0.1,
        help="Number of seconds to sleep after issuing a motor command.",
    )
    parser.add_argument(
        "--hold-time",
        dest="holdTime",
        type=int,
        default=3,
        help="The time (seconds) to hold peak current.",
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
        args.minCurrent,
        args.maxCurrent,
        args.nCurrents,
        args.commandDelay,
        args.holdTime,
    )

    print("Done.")
