#!/usr/bin/env python3

"""
FlexSEA High Speed Test
"""
from time import sleep, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from flexsea import fxUtils as fxu  # pylint: disable=no-name-in-module
from flexsea import fxEnums as fxe  # pylint: disable=no-name-in-module
from flexsea import fxPlotting as fxp  # pylint: disable=no-name-in-module
from flexsea import flexsea as flex


# Plot in a browser:
matplotlib.use("WebAgg")
if fxu.is_pi():
	matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})


# pylint: disable=too-few-public-methods
class Signal:
	"""Signal type to send to controller"""

	sine = 1
	line = 2


def high_speed_test(  # pylint: disable=too-many-arguments too-many-statements too-many-locals too-many-branches
	fxs,
	ports,
	baud_rate,
	controller_type=fxe.HSS_CURRENT,
	signal_type=Signal.sine,
	cmd_freq=500,
	signal_amplitude=500,
	number_of_loops=4,
	signal_freq=5,
	cycle_delay=0.1,
	request_jitter=False,
	jitter=20,
	log_data=False,
	debug_log_level=6,
):
	"""
	baud_rate			Baud rate of outgoing serial connection to ActPack
	ports				List of ports with outgoing serial connection to ActPack
	controller_type		Position controller or current controller
	signal_type			Sine wave or line
	cmd_freq		Desired frequency of issuing commands to controller, actual
						command frequency will be slower due to OS overhead.
	signal_amplitude	Amplitude of signal to send to controller. Encoder position
						if position controller, current in mA if current controller
	number_of_loops		Number of times to send desired signal to controller
	signal_freq			Frequency of sine wave if using sine wave signal
	cycle_delay			Delay between signals sent to controller, use with sine wave only
	request_jitter		Add jitter amount to every other sample sent to controller
	jitter				Amount of jitter
	log_data			Enable data logging
	debug_log_level     6 is least verbose, 0 is most verbose
	"""

	win_max_freq = 100
	if fxu.is_win() and cmd_freq > win_max_freq:
		cmd_freq = win_max_freq
		print(f"Capping the command frequency in Windows to {cmd_freq}")

	# One vs two devices
	second_device = len(ports) > 1

	if second_device:
		print("Running High Speed Test with two devices")
	else:
		print("Running High Speed Test with one device")

	delay_time = 1.0 / (float(cmd_freq))
	print(delay_time)

	# Open the device and start streaming
	dev_id0 = fxs.open(ports[0], baud_rate, debug_log_level)
	fxs.start_streaming(dev_id0, cmd_freq, log_data)
	print("Connected to device 0 with ID", dev_id0)

	dev_id1 = -1
	if second_device:
		dev_id1 = fxs.open(ports[1], baud_rate, debug_log_level)
		fxs.start_streaming(dev_id1, cmd_freq, log_data)
		print("Connected to device 1 with ID", dev_id1)

	# Get initial position:
	if controller_type == fxe.HSS_POSITION:
		# Get initial position:
		print("Reading initial position...")
		# Give the device time to consume the startStreaming command and start streaming
		sleep(0.1)
		data = fxs.read_device(dev_id0)
		initial_pos_0 = data.mot_ang

		initial_pos_1 = 0
		if second_device:
			data = fxs.read_device(dev_id1)
			initial_pos_1 = data.mot_ang
	else:
		initial_pos_0 = 0
		initial_pos_1 = 0

	# Generate a control profile
	print("Command table:")
	if signal_type == Signal.sine:
		samples = fxu.sin_generator(signal_amplitude, signal_freq, cmd_freq)
		signal_type_str = "sine wave"
	elif signal_type == Signal.line:
		samples = fxu.line_generator(signal_amplitude, 1, cmd_freq)
		signal_type_str = "line"
	else:
		assert 0
	print(np.int64(samples))

	# Initialize lists
	requests = []
	measurements0 = []
	measurements1 = []
	times = []
	cycle_stop_times = []
	dev0_write_command_times = []
	dev1_write_command_times = []
	dev0_read_command_times = []
	dev1_read_command_times = []

	# Prepare controller:
	if controller_type == fxe.HSS_CURRENT:
		print("Setting up current control demo. Low current, high frequency.")
		# Gains are, in order: kp, ki, kd, K, B & ff
		fxs.set_gains(dev_id0, 40, 400, 0, 0, 0, 128)
		if second_device:
			fxs.set_gains(dev_id1, 40, 400, 0, 0, 0, 128)

	elif controller_type == fxe.HSS_POSITION:
		print("Setting up position control demo")
		# Gains are, in order: kp, ki, kd, K, B & ff
		fxs.set_gains(dev_id0, 300, 50, 0, 0, 0, 0)
		if second_device:
			fxs.set_gains(dev_id1, 300, 50, 0, 0, 0, 0)
	else:
		assert 0, "Invalid controller type"

	# Record start time of experiment
	i = 0
	start_time = time()
	# pylint: disable=too-many-nested-blocks
	for rep in range(number_of_loops):
		elapsed_time = time() - start_time
		fxu.print_loop_count_and_time(rep, number_of_loops, elapsed_time)
		for sample in samples:
			if i % 2 == 0 and request_jitter:
				sample = sample + jitter

			sleep(delay_time)

			# Read ActPack data
			dev0_read_time_before = time()
			data0 = fxs.read_device(dev_id0)
			dev0_read_time_after = time()
			if second_device:
				dev1_read_time_before = time()
				data1 = fxs.read_device(dev_id1)
				dev1_read_time_after = time()

			# Write setpoint
			if controller_type == fxe.HSS_CURRENT:
				dev0_write_time_before = time()
				fxs.send_motor_command(dev_id0, fxe.FX_CURRENT, sample)
				dev0_write_time_after = time()
				measurements0.append(data0.mot_cur)
				if second_device:
					dev1_write_time_before = time()
					fxs.send_motor_command(dev_id1, fxe.FX_CURRENT, sample)
					dev1_write_time_after = time()
					measurements1.append(data1.mot_cur)

			elif controller_type == fxe.HSS_POSITION:
				dev0_write_time_before = time()
				fxs.send_motor_command(dev_id0, fxe.FX_POSITION, sample + initial_pos_0)
				dev0_write_time_after = time()
				measurements0.append(data0.mot_ang - initial_pos_0)
				if second_device:
					dev1_write_time_before = time()
					fxs.send_motor_command(dev_id1, fxe.FX_POSITION, sample + initial_pos_1)
					dev1_write_time_after = time()
					measurements1.append(data1.mot_ang - initial_pos_1)

			dev0_read_command_times.append(dev0_read_time_after - dev0_read_time_before)
			dev0_write_command_times.append(dev0_write_time_after - dev0_write_time_before)
			if second_device:
				dev1_read_command_times.append(dev1_read_time_after - dev1_read_time_before)
				dev1_write_command_times.append(dev1_write_time_after - dev1_write_time_before)
			times.append(time() - start_time)
			requests.append(sample)
			i = i + 1

			# Delay between cycles (sine wave only)
			if signal_type == Signal.sine:
				for _j in range(int(cycle_delay / delay_time)):

					sleep(delay_time)
					# Read data from ActPack
					data0 = fxs.read_device(dev_id0)
					if second_device:
						data1 = fxs.read_device(dev_id1)

					if controller_type == fxe.HSS_CURRENT:
						measurements0.append(data0.mot_cur)
						if second_device:
							measurements1.append(data1.mot_cur)

					elif controller_type == fxe.HSS_POSITION:
						measurements0.append(data0.mot_ang - initial_pos_0)
						if second_device:
							measurements1.append(data1.mot_ang - initial_pos_1)

					times.append(time() - start_time)
					requests.append(sample)
					i = i + 1

		# We'll draw a line at the end of every period
		cycle_stop_times.append(time() - start_time)
	# Disable the controller, send 0 PWM
	fxs.send_motor_command(dev_id0, fxe.FX_NONE, 0)
	if second_device:
		fxs.send_motor_command(dev_id1, fxe.FX_NONE, 0)
	sleep(0.1)

	# End of Main Code - Start of plotting code

	elapsed_time = time() - start_time
	actual_period = cycle_stop_times[0]
	actual_frequency = 1 / actual_period
	cmd_freq = i / elapsed_time

	# Figure: setpoint, desired vs measured (1st device)
	figure_counter = 1  # First time, functions will increment
	figure_counter = fxp.plot_setpoint_vs_desired(
		dev_id0,
		figure_counter,
		controller_type,
		actual_frequency,
		signal_amplitude,
		signal_type_str,
		cmd_freq,
		times,
		requests,
		measurements0,
		cycle_stop_times,
	)
	figure_counter = fxp.plot_exp_stats(
		dev_id0, figure_counter, dev0_write_command_times, dev0_read_command_times
	)

	# Figure: setpoint, desired vs measured (2nd device)
	if second_device:
		figure_counter = fxp.plot_setpoint_vs_desired(
			dev_id1,
			figure_counter,
			controller_type,
			actual_frequency,
			signal_amplitude,
			signal_type_str,
			cmd_freq,
			times,
			requests,
			measurements1,
			cycle_stop_times,
		)
		figure_counter = fxp.plot_exp_stats(
			dev_id1, figure_counter, dev1_write_command_times, dev1_read_command_times
		)

	fxu.print_plot_exit()
	plt.show()
	fxs.close_all()


def main():
	"""
	Standalone High Speed Test execution
	"""
	# pylint: disable=import-outside-toplevel
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"ports", metavar="Ports", type=str, nargs="+", help="Your devices' serial ports."
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
		"-l",
		"--loops",
		metavar="L",
		dest="loops",
		type=int,
		default=4,
		help="Number of loops to run.",
	)
	parser.add_argument(
		"-d", "--log_data", dest="log_data", action="store_true", help="Enable data logging",
	)
	args = parser.parse_args()
	print(args.log_data)
	high_speed_test(
		flex.FlexSEA(),
		args.ports,
		args.baud_rate,
		number_of_loops=args.loops,
		log_data=args.log_data,
	)


if __name__ == "__main__":
	main()
