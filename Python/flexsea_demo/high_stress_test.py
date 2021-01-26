#!/usr/bin/python3
"""'Performs high-stress test on ActuatorPackage.'"""

import os
import sys
import traceback
from time import sleep, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from flexseapython import fxUtil as fx
from flexseapython.fxPlotting import plotSetpointVsDesired

# Plot in a browser:
matplotlib.use("WebAgg")

# Globals updated with every timestamp for plotting
TIMESTAMPS = []  # Elapsed times since strart of run
CYCLE_STOP_TIMES = []  # Timestamps for each loop end


def fxHighStressTest(
	port0,
	baudRate,
	port1="",
	commandFreq=1000,
	positionAmplitude=10000,
	currentAmplitude=1500,
	positionFreq=1,
	currentFreq=5,
	currentAsymmetricG=1.25,
	numberOfLoops=3,
):
	"""
	portX				port with outgoing serial connection to ActPack
	baudRate			baud rate of outgoing serial connection to ActPack
	commandFreq			Desired frequency of issuing commands to controller,
						actual command frequency will be slower due to OS
						overhead.
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
	devices.append({"port": port0})
	if port1:
		devices.append({"port": port1})

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
		"Running high stress test with {} device".format(len(devices)) + "s"
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
		dev["id"] = fx.fxOpen(dev["port"], baudRate, debug_logging_level)
		fx.fxStartStreaming(dev["id"], commandFreq, data_log)
		print("Connected to device with Id: ", dev["id"])

	# Get initial position:
	print("Reading initial position...")

	# Wait for device to consume the startStreaming command and start streaming
	sleep(0.1)

	# Get initial position
	for dev in devices:
		dev["data"] = fx.fxReadDevice(dev["id"])
		dev["initial_pos"] = dev["data"].mot_ang  # Used to offset readings
		print("Initial Position: {}".format(dev["initial_pos"]))

	# Generate control profiles
	print("Generating three Command tables...")
	position_samples = fx.sinGenerator(positionAmplitude, positionFreq, commandFreq)
	current_samples = fx.sinGenerator(currentAmplitude, currentFreq, commandFreq)
	current_samples_line = fx.lineGenerator(0, 0.15, commandFreq)

	start_time = time()  # Record start time of experiment
	cmd_count = 0
	try:
		for rep in range(0, numberOfLoops):
			fx.printLoopCountAndTime(rep, numberOfLoops, time() - start_time)

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

			send_and_time_cmds(start_time, devices, cmds, fx.FxPosition, True)

			# Step 1: go to initial position
			# -------------------------------
			if rep:  # Second or later iterations in loop
				print("Step 1: go to initial position")
				# Create interpolation angles for each device
				lin_samples = []
				for dev in devices:
					lin_samples.append(
						fx.linearInterp(dev["data"].mot_ang - dev["initial_pos"], 0, 100)
					)

				for samples in lin_samples:
					for sample in samples:
						cmds = [{"cur": 0, "pos": sample + dev["initial_pos"]} for dev in devices]
						sleep(delay_time)
						send_and_time_cmds(start_time, devices, cmds, fx.FxPosition, False)
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
				send_and_time_cmds(start_time, devices, cmds, fx.FxPosition, False)
				cmd_count += 1

			# Step 3: set current controller
			# -------------------------------
			print("Step 3: set current controller")
			cmds = [{"cur": 0, "pos": 0} for dev in devices]
			send_and_time_cmds(start_time, devices, cmds, fx.FxCurrent, True)

			# Step 4: current setpoint
			# --------------------------
			print("Step 4: track current sine wave")
			for sample in current_samples:
				sleep(delay_time)
				# We use more current on the "way back" to come back closer to
				# the staring point
				if sample > 0:  # Apply gain
					sample = np.int64(currentAsymmetricG * sample)
				cmds = [{"cur": sample, "pos": dev["initial_pos"]} for dev in devices]

				sleep(delay_time)
				send_and_time_cmds(start_time, devices, cmds, fx.FxCurrent, False)
				cmd_count += 1

			# Step 5: short pause at 0 current to allow a slow-down
			# -----------------------------------------------------
			print("Step 5: motor slow-down, zero current")

			for sample in current_samples_line:
				cmds = [{"cur": sample, "pos": dev["initial_pos"]} for dev in devices]
				sleep(delay_time)
				send_and_time_cmds(start_time, devices, cmds, fx.FxCurrent, False)
				cmd_count += 1

			# Draw a line at the end of every loop
			CYCLE_STOP_TIMES.append(time() - start_time)

	except KeyboardInterrupt:
		print("Keypress detected. Exiting gracefully...")

	elapsed_time = time() - start_time

	# Disable the controller, send 0 PWM
	for dev in devices:
		fx.fxSendMotorCommand(dev["id"], fx.FxVoltage, 0)
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
		devices, positionAmplitude, positionFreq, currentAmplitude, currentFreq, commandFreq
	)


def plot_data(
	devices, pos_amp, pos_freq, curr_amp, curr_freq, cmd_freq, type_str="sine wave"
):
	"""
	Plots received data
	devices:  Dictionarty containing iinfor foir ach connected device.
	"""
	global TIMESTAMPS  # Elapsed times since strart of run
	global CYCLE_STOP_TIMES  # Timestamps for each loop end

	figure_ind = 1
	for dev in devices:
		# Current Plot:
		figure_ind = plotSetpointVsDesired(
			dev["id"],
			figure_ind,
			fx.hssCurrent,
			curr_amp,
			curr_freq,
			type_str,
			cmd_freq,
			TIMESTAMPS,
			dev["curr_requests"],
			dev["curr_measurements"],
			CYCLE_STOP_TIMES,
		)

		figure_ind = plotSetpointVsDesired(
			dev["id"],
			figure_ind,
			fx.hssPosition,
			pos_amp,
			pos_freq,
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
	fx.printPlotExit()
	fx.fxCloseAll()
	print("Communication closed")


def send_and_time_cmds(start_time, devices, cmds, motor_cmd, set_gains: bool):
	"""
	Send FlexSEA commands and record their execution time.
	start_time:	Timestamp for start of run. (Current time-start_time) = Elapsed time
	devices:	Dictionary containing info on all connected devices
	cmds:		Dictionary containing position and current commands e.g. {pos: 0, curr: 0}
	motor_cmd:	An enum defined in flexseapython.py. Allowed values: FxPosition,, FxCurrent
	"""
	global TIMESTAMPS  # Elapsed times from start of run

	assert motor_cmd in [
		fx.FxPosition,
		fx.FxCurrent,
	], "Unexpected motor command, only FxPosition, FxCurrent allowed"

	for dev, cmd in zip(devices, cmds):
		tstart = time()
		dev["data"] = fx.fxReadDevice(dev["id"])  # Get ActPackState
		dev["read_times"].append(time() - tstart)

		if set_gains:
			tstart = time()
			# Gains are, in order: kp, ki, kd, K, B & ff
			fx.fxSetGains(dev["id"], 250, 200, 0, 0, 0, 128)
			dev["gains_times"].append(time() - tstart)
		else:
			dev["gains_times"].append(0)

		# Select command value
		cmd_val = cmd["cur"] if motor_cmd == fx.FxCurrent else cmd["pos"]
		# Command motor
		tstart = time()
		fx.fxSendMotorCommand(dev["id"], motor_cmd, cmd_val)
		dev["motor_times"].append(time() - tstart)
		dev["pos_requests"].append(cmd["pos"])
		dev["pos_measurements"].append(dev["data"].mot_ang)
		dev["curr_requests"].append(cmd["cur"])
		dev["curr_measurements"].append(dev["data"].mot_cur)

	TIMESTAMPS.append(time() - start_time)


# TODO: Support standalone execution
if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("baudrate", type=int, help="Communication baudrate")
	parser.add_argument("port", type=str, nargs="+", help="Ports for test devices")
	args = parser.parse_args()

	try:
		# TODO: Support more than 2 ports
		if len(args.port) > 1:
			fxHighStressTest(args.port[0], args.baudrate, args.port[1])
		else:
			fxHighStressTest(args.port[0], args.baudrate)
	except Exception as err:
		print("broke: {}".format(err))
		traceback.print_exc()
