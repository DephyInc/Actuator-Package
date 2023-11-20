"""
Demo 5: Lab Streaming Layer

Reads data from a dephy device and streams it using the LSL protocol.
"""
# pylint: disable=duplicate-code

import platform
import sys
from time import sleep

import numpy as np

from flexsea.device import Device


if "windows" == platform.system().lower():
    msg = "WARNING: these demos may not function properly on Windows "
    msg += "due to the way the OS handles timing. They are best run on "
    msg += "linux."
    print(msg)

firmwareVersion = "9.0.0"
port = "/dev/ttyACM0"
device = Device(port=port, firmwareVersion=firmwareVersion)
device.open()
device.start_streaming(100)

while True:
    device.print()
    sleep(0.1)

device.close()
