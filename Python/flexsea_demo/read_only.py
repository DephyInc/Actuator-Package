#!/usr/bin/env python3

"""
FlexSEA Read Only Demo
"""
from time import sleep
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex

# TODO(CA): move to fxUtils
def print_bms_state(fxs, dev_id):
	"""
	Read BMS info
	"""
	bms_state = fxs.read_bms_device_all(dev_id, 1)
	for i in range(9):
		print("Cell [{}] Voltage: {}".format(i, bms_state.cellVoltage[i]))
	for i in range(3):
		print("Temperature [{}]: {}".format(i, bms_state.temperature[i]))


def read_only(fxs, port, baud_rate, run_time=8, time_step=0.1):
	"""
	Reads FlexSEA device and prints gathered data.
	"""
	debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
	data_log = True  # False means no logs will be saved
	dev_id = fxs.open(port, baud_rate, debug_logging_level)
	fxs.start_streaming(dev_id, freq=100, log_en=data_log)
	app_type = fxs.get_app_type(dev_id)

	if app_type.value == fxe.FX_ACT_PACK.value:
		print("\nYour device is an ActPack.\n")
		input("Press Enter to continue...")
	elif app_type.value == fxe.FX_NET_MASTER.value:
		print("\nYour device is a NetMaster.\n")
		input("Press Enter to continue...")
	elif app_type.value == fxe.FX_BMS.value:
		print("\nYour device is a BMS.\n")
		input("Press Enter to continue...")
	elif app_type.value == fxe.FX_EXO.value:
		print("\nYour device is an Exo or ActPack Plus.\n")
		input("Press Enter to continue...")
	else:
		raise RuntimeError(f"Unsupported application type: {app_type}")

	total_loop_count = int(run_time / time_step)
	for i in range(total_loop_count):
		fxu.print_loop_count(i, total_loop_count)
		sleep(time_step)
		fxu.clear_terminal()
		data = fxs.read_device(dev_id)
		fxu.print_device(data, app_type)
	fxs.close(dev_id)
	return True


def main():
	"""
	Standalone read only execution
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
	read_only(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
