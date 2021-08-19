#!/usr/bin/env python3

"""
FlexSEA version number demo
"""
from time import sleep
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex
import ctypes as c

def decode(val):
	x = y = z = 0
	
	if (val > 0):
		while (val%2 == 0):
			x += 1 
			val /= 2

		while (val%3 == 0):
			y += 1 
			val /= 3		

		while (val%5 == 0):
			z += 1 
			val /= 5
		
	return str(x) + "." + str(y) + "." + str(z)	

def get_version(fxs, port, baud_rate):
	"""Check bootloader in target"""
	debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
	dev_id = fxs.open(port, baud_rate, debug_logging_level)
	app_type = fxs.get_app_type(dev_id)

	if app_type.value == fxe.FX_ACT_PACK.value:
		app_name = "ActPack"
	elif app_type.value == fxe.FX_EB5X.value:
		app_name = "Exo or ActPack Plus"
	else:
		raise RuntimeError(f"Unsupported application type: {app_type.value}")

	print(f"Your device is an {app_name}", flush=True)

	request = fxs.request_firmware_version(dev_id)
	if request == fxe.FX_SUCCESS.value:
		print(f"Collecting version information. Please wait...", flush=True)
	else:
		print(f"Firware version request failed", flush=True)

	sleep(5)

	fw_array = fxe.FW()
	fw_array = fxs.get_last_received_firmware_version(dev_id)

	fw_Mn = decode(fw_array.Mn)
	fw_Ex = decode(fw_array.Ex)
	fw_Re = decode(fw_array.Re)
	fw_Habs = decode(fw_array.Habs)

	print(f"Firmware version ", flush=True)
	print(f"\t Mn  : v{fw_Mn}", flush=True)
	print(f"\t Ex  : v{fw_Ex}", flush=True)
	print(f"\t Re  : v{fw_Re}", flush=True)
	print(f"\t Habs: v{fw_Habs}", flush=True)

	fxs.close(dev_id)
	return str(fw_array.Mn) + "." + str(fw_array.Ex) + "." + str(fw_array.Re) + "." +str(fw_array.Habs)


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

	args = parser.parse_args()
	return get_version(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	exit(main())
