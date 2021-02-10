#!/usr/bin/env python3

"""
FlexSEA Open Control Demo
"""
from time import sleep
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex


def open_control(
	fxs,
	port,
	baud_rate,
	run_time=2,
	num_times=5,
	time_resolution=0.1,
	max_voltage=3000,
	sign=-1,
):
	"""Implements open control for ActPack"""
	dev_id = fxs.open(port, baud_rate, log_level=6)
	fxs.start_streaming(dev_id, 100, log_en=False)
	app_type = fxs.get_app_type(dev_id)
	print("Setting open control...")
	fxs.send_motor_command(dev_id, fxe.FX_VOLTAGE, 0)
	sleep(0.5)
	step_count = int((run_time / 2) / time_resolution)

	for rep in range(num_times):
		# TODO(CA): Refactor loop to remove code repetition
		# Ramp-up:
		for step in range(step_count):
			sleep(time_resolution)
			voltage_mv = sign * max_voltage * (step * 1.0 / step_count)
			fxs.send_motor_command(dev_id, fxe.FX_VOLTAGE, voltage_mv)
			fxu.clear_terminal()
			print(f"Ramping up motor voltage {rep}...\n")
			data0 = fxs.read_device(dev_id)
			fxu.print_device(data0, app_type)

		# Ramp-down:
		for step in range(step_count):
			sleep(time_resolution)
			voltage_mv = sign * max_voltage * ((step_count - step) * 1.0 / step_count)
			fxs.send_motor_command(dev_id, fxe.FX_VOLTAGE, voltage_mv)
			fxu.clear_terminal()
			print(f"Ramping down motor voltage {rep}...\n")
			data0 = fxs.read_device(dev_id)
			fxu.print_device(data0, app_type)

	fxs.close(dev_id)
	return True


def main():
	"""
	Standalone open control execution
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
	open_control(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
