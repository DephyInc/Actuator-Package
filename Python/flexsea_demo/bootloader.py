#!/usr/bin/env python3

"""
FlexSEA Bootloader check demo
"""
from time import sleep
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex


def bootloader(fxs, port, baud_rate, target="Mn", timeout=60):
	"""Check bootloader in target"""
	debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
	dev_id = fxs.open(port, baud_rate, debug_logging_level)
	app_type = fxs.get_app_type(dev_id)
	result = False

	targets = {
		"Habs": {"id": 0, "name": "Habsolute"},
		"Reg": {"id": 1, "name": "Regulate"},
		"Exe": {"id": 2, "name": "Execute"},
		"Mn": {"id": 3, "name": "Manage"},
		"BT": {"id": 4, "name": "Bluetooth"},
		"XBee": {"id": 5, "name": "XBee"},
	}

	if app_type.value == fxe.FX_ACT_PACK.value:
		app_name = "ActPack"
	elif app_type.value == fxe.FX_EXO.value:
		app_name = "Exo or ActPack Plus"
	else:
		raise RuntimeError(f"Unsupported application type: {app_type.value}")

	print(f"Your device is an {app_name}", flush=True)

	try:
		print(f"Activating {targets[target]['name']} bootloader", flush=True)
		sleep(1)
		while timeout > 0:
			if timeout % 5 == 0:
				print("Sending signal to target device", flush=True)
				fxs.activate_bootloader(dev_id, targets[target]["id"])
			print(f"Waiting for response from target ({timeout}s)", flush=True)
			sleep(1)
			timeout -= 1
			state = fxs.is_bootloader_activated(dev_id)
			if state == 0:
				break

		if state == 0:
			result = True
			print(targets[target]["name"], "bootloader is activated", flush=True)
		else:
			result = False
			print(f"Unable to activate {targets[target]['name']} bootloader", flush=True)

	except KeyError:
		raise RuntimeError(f"Unsupported bootloader target: {target}")
	fxs.close(dev_id)
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
		choices=["Habs", "Mn", "Reg", "Exe"],
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
	return bootloader(
		flex.FlexSEA(), args.port[0], args.baud_rate, args.target, timeout=args.delay
	)


if __name__ == "__main__":
	exit(main())
