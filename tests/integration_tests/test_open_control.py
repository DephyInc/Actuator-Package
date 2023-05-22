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
    minVoltage: int,
    maxVoltage: int,
    nVoltages: int,
    nCycles: int,
    freq: int,
) -> None:
    device = Device(port=port, firmwareVersion=cLibVersion, libFile=libFile)
    device.open()
    device.start_streaming(freq)

    voltages = np.linspace(minVoltage, maxVoltage, nVoltages)

    for _ in range(nCycles):
        # Ramp up
        for voltage in voltages:
            device.command_motor_voltage(int(voltage))
            sleep(0.1)
            clear()
            device.print()

        # Ramp down
        for voltage in voltages[-1::-1]:
            device.command_motor_voltage(int(voltage))
            sleep(0.1)
            clear()
            device.print()

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
        "--max-voltage",
        dest="maxVoltage",
        type=int,
        default=3000,
        help="Maximum voltage to ramp to, in millivolts.",
    )
    parser.add_argument(
        "--min-voltage",
        dest="minVoltage",
        type=int,
        default=0,
        help="Minium voltage to start at, in millivolts.",
    )
    parser.add_argument(
        "-n",
        "--n-voltages",
        dest="nVoltages",
        type=int,
        default=10,
        help="The number of voltages to ramp over.",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        dest="nCycles",
        type=int,
        default=5,
        help="The number of times to loop over the voltage range.",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        dest="freq",
        type=int,
        default=100,
        help="The frequency (Hz) at which to stream data from the device.",
    )

    args = parser.parse_args()

    main(
        args.port,
        args.cLibVersion,
        args.libFile,
        args.minVoltage,
        args.maxVoltage,
        args.nVoltages,
        args.nCycles,
        args.freq,
    )

    print("Done.")
