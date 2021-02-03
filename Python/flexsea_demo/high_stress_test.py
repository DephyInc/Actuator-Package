#!/usr/bin/env python3

"""
Performs high-stress test on Actuator Package.
"""
from time import sleep, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import fxPlotting as fxp
from flexsea import flexsea as flex


# Plot in a browser:
matplotlib.use("WebAgg")
if fxu.is_pi():
	matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

# Globals updated with every timestamp for plotting
TIMESTAMPS = []  # Elapsed times since start of run
CYCLE_STOP_TIMES = []  # Timestamps for each loop end


def high_stress_test(
	fxs,
	ports,
	baudRate,
	commandFreq=100,
	positionAmplitude=10000,
	currentAmplitude=1500,
	positionFreq=1,
	currentFreq=5,
	currentAsymmetricG=1.15,
	numberOfLoops=3,
):
	"""
	portX				port with outgoing serial connection to ActPack
	baudRate			baud rate of outgoing serial connection to ActPack
	commandFreq			Desired frequency of issuing commands to controller,
						actual command frequency will be slower due to OS
						overhead. On Win, use 100Hz. On Unix you can go up to 1kHz.
	positionAmplitude	amplitude (in ticks), position controller
	currentAmplitude	amplitude (in mA), current controller
	positionFreq		frequency (Hz) of the sine wave, position controller
	currentFreq			frequency (Hz) of the sine wave, current controller
	currentAsymmetricG	we use more current on the "way back" to come back
						closer to the staring point. Positive numbers only,
						1-3 range.
	numberOfLoops		Number of times to send desired signal to controller
	"""

	global TIMESTAMPS  # Elapsed times since strart of run
	global CYCLE_STOP_TIMES  # Timestamps for each loop end

	devices = []
	for port in ports:
		devices.append({"port": port})

	# Initialize devices
	for dev in devices:
		dev["read_times"] = []
		dev["gains_times"] = []
		dev["motor_times"] = []
		dev["pos_requests"] = []
		dev["pos_measurements"] = []
		dev["curr_requests"] = []
		dev["curr_measurements"] = []

	print(
		"Running High Stress Test with {} device".format(len(devices)) + "s"
		if len(devices) > 1
		else ""
	)

	# Debug & Data Logging
	debug_logging_level = 6  # 6 is least verbose, 0 is most verbose
	data_log = False  # Data log logs device data

	delay_time = float(1 / (float(commandFreq)))
	print("Delay time: ", delay_time)

	# Open the device and start streaming
	for dev in devices:
		print("Port: ", dev["port"])
		print("BaudRate: ", baudRate)
		print("Logging Level: ", debug_logging_level)
		dev["id"] = fxs.open(dev["port"], baudRate, debug_logging_level)
		fxs.start_streaming(dev["id"], commandFreq, data_log)
		print("Connected to device with Id: ", dev["id"])

	# Get initial position:
	print("Reading initial position...")

	# Wait for device to consume the startStreaming command and start streaming
	sleep(0.1)

	# Gains are, in order: kp, ki, kd, K, B & ff
	cur_gains = [40, 400, 0, 0, 0, 128]
	pos_gains = [100, 10, 0, 0, 0, 0]

	# Get initial position
	for dev in devices:
		dev["data"] = fxs.read_device(dev["id"])
		dev["initial_pos"] = dev["data"].mot_ang  # Used to offset readings
		print("Initial Position: {}".format(dev["initial_pos"]))

	# Generate control profiles
	print("Generating three command tables...")
	position_samples = fxu.sin_generator(positionAmplitude, positionFreq, commandFreq)
	current_samples = fxu.sin_generator(currentAmplitude, currentFreq, commandFreq)
	current_samples_line = fxu.line_generator(0, 0.5, commandFreq)

	start_time = time()  # Record start time of experiment
	cmd_count = 0
	try:
		for rep in range(0, numberOfLoops):
			fxu.print_loop_count_and_time(rep, numberOfLoops, time() - start_time)

			# Step 0: set position controller
			# -------------------------------
			print("Step 0: set position controller")

			sleep(delay_time)  # Important in loop 2+
			cmds = []
			for dev in devices:
				if rep:  # Second or later iterations in loop
					initial_cmd = {"cur": 0, "pos": dev["data"].mot_ang}
				else:
					initial_cmd = {"cur": 0, "pos": dev["initial_pos"]}
				cmds.append(initial_cmd)

			send_and_time_cmds(fxs, start_time, devices, cmds, fxe.FX_POSITION, pos_gains, True)

			# Step 1: go to initial position
			# -------------------------------
			if rep:  # Second or later iterations in loop
				print("Step 1: go to initial position")
				# Create interpolation angles for each device
				lin_samples = []
				for dev in devices:
					lin_samples.append(
						fxu.linear_interp(dev["data"].mot_ang - dev["initial_pos"], 0, 30)
					)

				for samples in lin_samples:
					for sample in samples:
						cmds = [{"cur": 0, "pos": sample + dev["initial_pos"]} for dev in devices]
						sleep(delay_time)
						send_and_time_cmds(
							fxs, start_time, devices, cmds, fxe.FX_POSITION, pos_gains, False
						)
						cmd_count += 1
			else:
				# First time in loop
				print("Step 1: skipped, first round")

			# Step 2: position sine wave
			# --------------------------
			print("Step 2: track position sine wave")

			for sample in position_samples:
				cmds = [{"cur": 0, "pos": sample + dev["initial_pos"]} for dev in devices]
				sleep(delay_time)
				send_and_time_cmds(
					fxs, start_time, devices, cmds, fxe.FX_POSITION, pos_gains, False
				)
				cmd_count += 1

			# Step 3: set current controller
			# -------------------------------
			print("Step 3: set current controller")
			cmds = [{"cur": 0, "pos": dev["initial_pos"]} for dev in devices]
			send_and_time_cmds(fxs, start_time, devices, cmds, fxe.FX_CURRENT, cur_gains, True)

			# Step 4: current setpoint
			# --------------------------
			print("Step 4: track current sine wave")
			for sample in current_samples:
				sleep(delay_time)
				# We use more current on the "way back" to come back closer to
				# the staring point
				sample = np.int64(sample)
				if sample > 0:  # Apply gain
					sample = np.int64(currentAsymmetricG * sample)
				cmds = [{"cur": sample, "pos": dev["initial_pos"]} for dev in devices]

				sleep(delay_time)
				send_and_time_cmds(fxs, start_time, devices, cmds, fxe.FX_CURRENT, cur_gains, False)
				cmd_count += 1

			# Step 5: short pause at 0 current to allow a slow-down
			# -----------------------------------------------------
			print("Step 5: motor slow-down, zero current")

			for sample in current_samples_line:
				cmds = [{"cur": sample, "pos": dev["initial_pos"]} for dev in devices]
				sleep(delay_time)
				send_and_time_cmds(fxs, start_time, devices, cmds, fxe.FX_CURRENT, cur_gains, False)
				cmd_count += 1

			# Draw a line at the end of every loop
			CYCLE_STOP_TIMES.append(time() - start_time)

	except KeyboardInterrupt:
		print("Keypress detected. Exiting gracefully...")

	elapsed_time = time() - start_time

	# Disable the controller, send 0 PWM
	for dev in devices:
		fxs.send_motor_command(dev["id"], fxe.FX_VOLTAGE, 0)
	sleep(0.1)

	######## Stats: #########
	print("")
	print("Final Stats:")
	print("------------")
	print("Number of commands sent: {}".format(cmd_count))
	print("Total time (s): {}".format(elapsed_time))
	print("Requested command frequency: {:.2f}".format(commandFreq))
	assert elapsed_time != 0, "Elapsed time is 0."
	print("Actual command frequency (Hz): {:.2f}".format(cmd_count / elapsed_time))
	print("")
	print("current_samples_line: {}".format(len(current_samples_line)))
	print("size(TIMESTAMPS): {}".format(len(TIMESTAMPS)))
	print("size(currentRequests): {}".format(len(devices[0]["curr_requests"])))
	print("size(currentMeasurements0): {}".format(len(devices[0]["curr_measurements"])))
	print("size(SET_GAINS_TIMES): {}".format(len(devices[0]["gains_times"])))
	print("")

	plot_data(
		fxs,
		devices,
		positionAmplitude,
		positionFreq,
		currentAmplitude,
		currentFreq,
		commandFreq,
	)


def plot_data(
	fxs, devices, pos_amp, pos_freq, curr_amp, curr_freq, cmd_freq, type_str="sine wave"
):
	"""
	Plots received data
	devices:  Dictionary containing info for each connected device.
	"""
	global TIMESTAMPS  # Elapsed times since start of run
	global CYCLE_STOP_TIMES  # Timestamps for each loop end

	figure_ind = 1
	for dev in devices:
		# Current Plot:
		figure_ind = fxp.plot_setpoint_vs_desired(
			dev["id"],
			figure_ind,
			fxe.HSS_CURRENT,
			curr_freq,
			curr_amp,
			type_str,
			cmd_freq,
			TIMESTAMPS,
			dev["curr_requests"],
			dev["curr_measurements"],
			CYCLE_STOP_TIMES,
		)

		figure_ind = fxp.plot_setpoint_vs_desired(
			dev["id"],
			figure_ind,
			fxe.HSS_POSITION,
			pos_freq,
			pos_amp,
			type_str,
			cmd_freq,
			TIMESTAMPS,
			dev["pos_requests"],
			dev["pos_measurements"],
			CYCLE_STOP_TIMES,
		)

	print("Showing plots")
	plt.show()
	sleep(0.1)
	fxu.print_plot_exit()
	fxs.close_all()
	print("Communication closed")


def send_and_time_cmds(
	fxs, start_time, devices, cmds, motor_cmd, gains, set_gains: bool
):
	"""
	Send FlexSEA commands and record their execution time.
	start_time:	Timestamp for start of run. (Current time-start_time) = Elapsed time
	devices:	Dictionary containing info on all connected devices
	cmds:		Dictionary containing position and current commands e.g. {pos: 0, curr: 0}
	motor_cmd:	An enum defined in flexseapython.py. Allowed values: FX_POSITION,, FX_CURRENT
	"""
	global TIMESTAMPS  # Elapsed times from start of run

	assert motor_cmd in [
		fxe.FX_POSITION,
		fxe.FX_CURRENT,
	], "Unexpected motor command, only FX_POSITION, FX_CURRENT allowed"

	for dev, cmd in zip(devices, cmds):
		tstart = time()
		dev["data"] = fxs.read_device(dev["id"])  # Get ActPackState
		dev["read_times"].append(time() - tstart)

		if set_gains:
			tstart = time()
			# Gains are, in order: kp, ki, kd, K, B & ff
			fxs.set_gains(dev["id"], *gains)
			dev["gains_times"].append(time() - tstart)
		else:
			dev["gains_times"].append(0)

		# Select command value
		cmd_val = cmd["cur"] if motor_cmd == fxe.FX_CURRENT else cmd["pos"]
		# Command motor
		tstart = time()
		fxs.send_motor_command(dev["id"], motor_cmd, cmd_val)
		dev["motor_times"].append(time() - tstart)
		dev["pos_requests"].append(cmd["pos"])
		dev["pos_measurements"].append(dev["data"].mot_ang)
		dev["curr_requests"].append(cmd["cur"])
		dev["curr_measurements"].append(dev["data"].mot_cur)

	TIMESTAMPS.append(time() - start_time)


def main():
	"""
	Standalone High Stress Test execution
	"""
	# pylint: disable=import-outside-toplevel
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument(
		"ports", metavar="Ports", type=str, nargs="+", help="Your devices serial ports."
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
	high_stress_test(flex.FlexSEA(), args.ports, args.baud_rate)


if __name__ == "__main__":
	main()
