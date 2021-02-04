#!/usr/bin/env python3
"""
FlexSEA devices Python demo
"""

import os
import sys
from signal import signal, SIGINT
from flexsea import flexsea as flex
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from read_only import read_only
from open_control import open_control
from current_control import current_control
from position_control import position_control
from impedance_control import impedance_control
from two_position_control import two_position_control
from high_speed_test import high_speed_test
from high_stress_test import high_stress_test
from two_devices_position_control import two_devices_position_control
from two_devices_leader_follower import leader_follower
from bootloader import bootloader


if (sys.version_info[0] == 3) and (sys.version_info[1] == 8):
	if fxu.is_win():  # Need for WebAgg server to work in Python 3.8
		print("Detected Python 3.8")
		print("Detected: {}".format(sys.platform))
		import asyncio

		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def sig_handler(*_unused):
	"""
	Handle program exit via SIGINT
	"""
	return sys.exit("\nCTRL-C or SIGINT detected\nExiting ...")


def find_poles(port, baud_rate):
	"""
	Find motor poles
	"""
	fxs = flex.FlexSEA()
	dev_id = fxs.open(port, baud_rate, 0)
	if fxs.find_poles(dev_id) == fxe.FX_INVALID_DEVICE:
		raise ValueError("fxFindPoles: invalid device ID")


# List of available experiments.
# Format is: functionName, text string, min number of devices, max devices
EXPERIMENTS = [
	(read_only, "Read Only", 1, 1),
	(open_control, "Open Control", 1, 1),
	(current_control, "Current Control", 1, 1),
	(position_control, "Position Control", 1, 1),
	(impedance_control, "Impedance Control", 1, 1),
	(two_position_control, "Two Positions Control", 1, 1),
	(high_speed_test, "High-speed Test", 1, 2),
	(high_stress_test, "High-stress Test", 1, 2),
	(two_devices_position_control, "Two Devices Position Control", 2, 2),
	(leader_follower, "Two Devices Leader Follower Control", 2, 2),
	(bootloader, "Bootloader Check", 1, 1),
	(find_poles, "Find Poles", 1, 1),
]


def print_demos():
	"""
	Print list of available experiments
	"""
	print("STOP!")
	print("Read our important safety information at https://dephy.com/start/")
	print("before running the scripts for the first time.\n")

	print("Actuator Package Demo Scripts:")
	print("------------------------------")
	for exp in EXPERIMENTS[:-2]:
		print(f"[{EXPERIMENTS.index(exp)}] {exp[1]}")

	print("\nAdvanced Utilities:")
	print("------------------------------")

	for exp in EXPERIMENTS[-2:]:
		print(f"[{EXPERIMENTS.index(exp)}] {exp[1]}")
	print("")


def print_usage(prog_name: str):
	"""
	Some error occurred. Print help message and exit.
	"""
	# TODO (CA): use argparse for all arguments and usage
	print(
		f"Usage:\tPython {prog_name} [experiment_number (0 - {len(EXPERIMENTS) - 1 }) connected_devices (1 - N)]"
	)
	print(
		"""
		"connected_devices" is ONLY required for some experiments
		 other experiments use [1] device by default.
		"""
	)


def get_exp_ind(argv):
	"""
	Obtain experiment number from argument list or by prompting user
	"""
	if len(argv) > 1:
		# Get it from the command line argument list
		exp_ind = argv[1]
	else:
		# Or prompt the user for it
		exp_ind = input("Choose experiment number [q to quit]: ")
		if exp_ind.lower() == "q":
			sys.exit(0)
	# Make sure it's valid and in range:
	if not exp_ind.isdecimal():  # Filter out letters
		sys.exit(f"Please choose an experiment between [0 - {len(EXPERIMENTS) - 1} ]")
	exp_ind = int(exp_ind)  # Make sure is a int and not a string
	if exp_ind not in range(len(EXPERIMENTS)):
		sys.exit(f"Please choose an experiment between [0 - {len(EXPERIMENTS) - 1} ]")
	return exp_ind


def get_dev_num(argv, exp_ind):
	"""
	Obtain number of devices from argument list or by prompting user
	"""
	dev_range = range(EXPERIMENTS[exp_ind][2], EXPERIMENTS[exp_ind][3] + 1)

	# Only one valid option
	if len(dev_range) == 1:
		return EXPERIMENTS[exp_ind][2]

	print(f"Max number of devices for this experiment: {EXPERIMENTS[exp_ind][3]}")
	# Get it from the command line argument list
	if len(argv) > 2:
		dev_num = argv[2]
	# Or prompt the user for it
	else:
		dev_num = input("Enter connected devices [or q to quit]: ")
		if dev_num.lower() == "q":
			sys.exit(0)

	# Make sure it's valid and in range:
	if not dev_num.isdecimal():  # Filter out letters
		sys.exit("Please enter number")

	dev_num = int(dev_num)  # Make sure is a int and not a string
	# And make sure it's in range
	if dev_num in dev_range:
		return dev_num

	sys.exit(
		f"Choose a number of device between {EXPERIMENTS[exp_ind][2]} and {EXPERIMENTS[exp_ind][3]}"
	)


def main(argv):
	"""
	Interactive menu for experiment selection and running
	"""
	signal(SIGINT, sig_handler)  # Handle Ctrl-C or SIGINT
	fxu.print_logo()

	# Handles command line arguments and experiment setup
	if len(argv) <= 3:
		print_demos()
		exp_ind = get_exp_ind(argv)
		dev_num = get_dev_num(argv, exp_ind)
	else:
		print_usage(argv[0])
		sys.exit("Too many command line arguments provided.")

	print(
		f"\nRunning Experiment [{exp_ind}] with [{dev_num}] connected device{'s' if dev_num > 1 else ''}."
	)

	port_cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ports.yaml")
	ports, baud_rate = fxu.load_ports_from_file(port_cfg_path)
	print(f"Using ports:\t{ports}")
	print(f"Using baud rate:\t{baud_rate}")

	# TODO (CA): add support for n ports and use argparser
	# Call selected demo script:
	try:
		if EXPERIMENTS[exp_ind][3] == 1:
			EXPERIMENTS[exp_ind][0](flex.FlexSEA(), ports[0], baud_rate)
		else:
			EXPERIMENTS[exp_ind][0](flex.FlexSEA(), ports[:dev_num], baud_rate)
	except Exception as err:
		print("Problem encountered when running the demo: {}".format(err))
		sys.exit(err)

	print(f"\nExiting {argv[0]} normally...\n")
	sys.exit(0)


if __name__ == "__main__":
	main(sys.argv)
