#!/usr/bin/env python3

"""
FlexSEA Read Only Demo
"""
from time import sleep
from flexsea import fxUtils as fxu  # pylint: disable=no-name-in-module
from flexsea import fxEnums as fxe  # pylint: disable=no-name-in-module
from flexsea import flexsea as flex  # pylint: disable=no-name-in-module

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


def read_only(fxs, port, baud_rate, run_time=8, user_input=True):
	"""
	Reads FlexSEA device and prints gathered data.
	"""
	time_step = 0.1
	debug_logging_level = 0  # 6 is least verbose, 0 is most verbose
	dev_id = fxs.open(port, baud_rate, debug_logging_level)
	app_type = fxs.get_app_type(dev_id)
	fxs.start_streaming(dev_id, freq=100, log_en=True)

	try:
		print(f"Your device is an {fxe.APP_NAMES[app_type.value]}", flush=True)
		if app_type.value == fxe.FX_INVALID_APP.value:
			raise KeyError(app_type.value)
		if user_input:
			input("Press Enter to continue...")
	except KeyError as err:
		raise RuntimeError(f"Unsupported application type: {app_type.value}") from err

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
	parser.add_argument(
		"-rt",
		"--run_t",
		nargs=1,
		metavar="R",
		dest="run_time",
		type=int,
		default=[8],
		help="Total run time in seconds.",
	)
	parser.add_argument(
		"-UI",
		"--no_user_input",
		dest="no_user_input",
		action="store_false",
		help="Do not wait for user input.",
	)
	args = parser.parse_args()
	read_only(
		flex.FlexSEA(), args.port[0], args.baud_rate, args.run_time[0], args.no_user_input
	)


if __name__ == "__main__":
	main()
