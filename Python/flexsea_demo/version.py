#!/usr/bin/env python3

"""
FlexSEA version number demo
"""
import signal
import sys
from time import sleep

from flexsea import flexsea as flex
from flexsea import fxEnums as fxe  # pylint: disable=no-name-in-module
from flexsea import fxUtils as fxu  # pylint: disable=no-name-in-module


def timeout_handler(signum, frame):
	"""Raises exception if there's a timeout"""
	raise RuntimeError("Function call timeout")


def get_version(fxs, port, baud_rate):
	"""Check version of onboard MCUs"""
	debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
	dev_id = fxs.open(port, baud_rate, debug_logging_level)
	app_type = fxs.get_app_type(dev_id)

	try:
		app_name = fxe.APP_NAMES[app_type.value]
		print(f"Your device is an {app_name}", flush=True)
	except KeyError as err:
		raise RuntimeError(f"Unsupported application type: {app_type.value}") from err

	signal.signal(signal.SIGALRM, timeout_handler)
	signal.alarm(5)  # set timeout for 30s
	try:
		fw_version_status = fxs.request_firmware_version(dev_id)
	except (RuntimeError, ValueError, IOError) as err:
		fw_version_status = fxs.FX_FAILURE.value
		print(
			f"[WARNING]: Error encountered when getting firmware version: {err}", flush=True
		)
	signal.alarm(0)

	if fw_version_status == fxe.FX_SUCCESS.value:
		print("Collecting version information. Please wait...", flush=True)
	else:
		print("[WARNING]: Firmware version request failed", flush=True)

	sleep(5)

	fw_array = fxs.get_last_received_firmware_version(dev_id)
	fxs.close(dev_id)

	return fw_array


def main():
	"""
	Standalone version checking
	"""
	# pylint: disable=import-outside-toplevel
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"port", metavar="Port", type=str, nargs=1, help="Your device serial port."
	)
	parser.add_argument(
		"-b",
		"--baud",
		metavar="B",
		dest="baud_rate",
		type=int,
		default=230400,
		help="Serial communication baud rate.",
	)

	args = parser.parse_args()
	fw_array = fxe.FW()
	fw_array = get_version(flex.FlexSEA(), args.port[0], args.baud_rate)

	fw_mn = fxu.decode(fw_array.Mn)
	fw_ex = fxu.decode(fw_array.Ex)
	fw_re = fxu.decode(fw_array.Re)
	fw_habs = fxu.decode(fw_array.Habs)

	print("Firmware version ", flush=True)
	print(f"\t Mn  : v{fw_mn}", flush=True)
	print(f"\t Ex  : v{fw_ex}", flush=True)
	print(f"\t Re  : v{fw_re}", flush=True)
	print(f"\t Habs: v{fw_habs}", flush=True)

	return f"{fw_array.Mn}.{fw_array.Ex}.{fw_array.Re}.{fw_array.Habs}"


if __name__ == "__main__":
	sys.exit(main())
