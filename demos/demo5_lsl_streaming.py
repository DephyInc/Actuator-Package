"""
Demo 5: Lab Streaming Layer

Reads data from a Dephy device and streams it using the LSL protocol.

Besided the python dependencies in teh project, the LSL compiled
library is required: https://github.com/sccn/liblsl/releases

To visualize the data stream, use PlotJuggler:
https://github.com/Sotilrac/plotjuggler-lsl

"""

# pylint: disable=duplicate-code

import argparse
import platform
import uuid
from time import sleep

from pylsl import StreamInfo, StreamOutlet
from flexsea.device import Device


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="LSL Streaming Demo")

    # Adding arguments
    parser.add_argument(
        "--port", default="/dev/ttyACM0", help="Port to use (default: /dev/ttyACM0)"
    )
    parser.add_argument(
        "--freq", type=int, default=100, help="Freqency setting in Hz (default: 100)"
    )
    parser.add_argument(
        "--api", default="12.0.0", help="Version number (default: 12.0.0)"
    )

    # Parsing arguments
    args = parser.parse_args()

    # Accessing the arguments
    print(f"Port: {args.port}")
    print(f"Frequency: {args.freq} Hz")
    print(f"API Version: {args.api}")

    if "windows" == platform.system().lower():
        msg = "WARNING: these demos may not function properly on Windows "
        msg += "due to the way the OS handles timing. They are best run on "
        msg += "linux."
        print(msg)

    try:
        device = Device(port=args.port, firmwareVersion=args.api)
    except RuntimeError as err:
        print(f"There's a problem connecting to the device at {args.port}: \n {err}")
        return

    device.open()
    device.start_streaming(args.freq)

    # Get the data labels
    print(len(device._fields))
    labels = sorted(device.read().keys())

    print(f"{len(labels)} labels to be streamed:")
    print(labels)

    # Create LSL Stream
    info = StreamInfo(
        f"{device.id:X}",
        "Dephy",
        len(labels),
        float(args.freq),
        "int64",
        f"{uuid.uuid4()}",
    )

    chns = info.desc().append_child("channels")
    for label in labels:
        ch = chns.append_child("channel")
        ch.append_child_value("label", label)
    outlet = StreamOutlet(info, 64, 360)

    sleep(0.5)
    while True:
        try:
            data = device.read(allData=True)
        except AssertionError as err:
            data = []
            print(f"Problem reading: {err}")
        for sample in data:
            if sample["System Time"] != 0:  # Filter out invalid readings
                outlet.push_sample([sample[key] for key in sorted(sample)])
        sleep(0.1)

    device.close()


if __name__ == "__main__":
    main()
