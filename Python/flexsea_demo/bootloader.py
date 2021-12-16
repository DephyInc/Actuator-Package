#!/usr/bin/env python3

"""
FlexSEA Bootloader check demo
"""
import sys
from time import sleep
from flexsea import fxEnums as fxe  # pylint: disable=no-name-in-module
from flexsea import flexsea as flex

TARGETS = {
	"Habs": {"id": 0, "name": "Habsolute"},
	"Reg": {"id": 1, "name": "Regulate"},
	"Exe": {"id": 2, "name": "Execute"},
	"Mn": {"id": 3, "name": "Manage"},
	"BT121": {"id": 4, "name": "Bluetooth"},
	"XBee": {"id": 5, "name": "XBee"},
}


def bootloader(fxs, port, baud_rate, target="Mn", timeout=60):
	"""Activate bootloader in target and wait until it's active."""
	debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
	result = 1

	try:
		dev_id = fxs.open(port, baud_rate, debug_logging_level)
		app_type = fxs.get_app_type(dev_id)
	except IOError as err:
		raise RuntimeError(f"Failed to open device at {port}") from err

	try:
		print(f"Your device is an {fxe.APP_NAMES[app_type.value]}", flush=True)
	except KeyError as err:
		raise RuntimeError(f"Unknown application type: {app_type.value}") from err

	print(f"Activating {TARGETS[target]['name']} bootloader", flush=True)
	wait_step = 1
	state = fxe.FX_FAILURE.value
	while timeout > 0 and state != fxe.FX_SUCCESS.value:
		if timeout % 5 == 0:
			print("Sending signal to target device", flush=True)
			try:
				fxs.activate_bootloader(dev_id, TARGETS[target]["id"])
			except (IOError, ValueError):
				pass
		print(f"Waiting for response from target ({timeout}s)", flush=True)
		sleep(wait_step)
		timeout -= wait_step
		try:
			state = fxs.is_bootloader_activated(dev_id)
		except ValueError as err:
			raise RuntimeError from err
		except IOError as err:
			pass

	if state == fxe.FX_SUCCESS.value:
		result = 0
		print(f"{TARGETS[target]['name']} bootloader is activated", flush=True)
	else:
		print(f"Unable to activate {TARGETS[target]['name']} bootloader", flush=True)

	try:
		fxs.close(dev_id)
	except ValueError:
		pass
	return result


def main():
	"""
	Standalone bootloader check execution
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

	parser.add_argument(
		"-t",
		"--target",
		metavar="T",
		dest="target",
		type=str,
		default="Mn",
		choices=TARGETS.keys(),
		help="Target microcontroller",
	)

	parser.add_argument(
		"-d",
		"--delay",
		metavar="D",
		dest="delay",
		type=int,
		default=60,
		help="Timeout delay",
	)
	args = parser.parse_args()
	try:
		return bootloader(
			flex.FlexSEA(), args.port[0], args.baud_rate, args.target, timeout=args.delay
		)
	except RuntimeError as err:
		print(f"Problem encountered when bootloading: {err}")
		return 1


if __name__ == "__main__":
	sys.exit(main())
