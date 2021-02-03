#!/usr/bin/env python3

"""
FlexSEA Impedance Control Demo
"""
from time import sleep, time
import matplotlib
import matplotlib.pyplot as plt
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex

matplotlib.use("WebAgg")
if fxu.is_pi():
	matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

# Control gain constants
GAINS = {"kp": 40, "ki": 400, "K": 600, "B": 300, "B_Increments": 150, "FF": 128}


def impedance_control(
	fxs,
	port,
	baud_rate,
	exp_time=10,
	time_step=0.02,
	delta=7500,
	transition_time=0.8,
	resolution=500,
):
	# Open device
	dev_id = fxs.open(port, baud_rate, log_level=6)
	fxs.start_streaming(dev_id, resolution, log_en=False)
	sleep(0.1)

	# Read initial angle
	data = fxs.read_device(dev_id)
	initial_angle = data.mot_ang

	result = True
	transition_steps = int(transition_time / time_step)

	# Initialize lists for matplotlib
	requests = []
	measurements = []
	times = []

	# Setpoint = initial angle
	fxs.send_motor_command(dev_id, fxe.FX_IMPEDANCE, initial_angle)
	# Set gains (in order: kp, ki, kd, K, B & ff)
	fxs.set_gains(dev_id, GAINS["kp"], GAINS["ki"], 0, GAINS["K"], GAINS["B"], GAINS["FF"])

	# Select transition rate and positions
	current_pos = 0
	num_time_steps = int(exp_time / time_step)
	positions = [initial_angle, initial_angle + delta]
	sleep(0.4)

	# Record start time of experiment
	start_time = time()

	# Run demo
	loop_ctr = 0
	print("")
	for i in range(num_time_steps):
		loop_ctr += 1
		data = fxs.read_device(dev_id)
		measured_pos = data.mot_ang
		if i % transition_steps == 0:
			GAINS["B"] += GAINS["B_Increments"]  # Increments every cycle
			fxs.set_gains(
				dev_id, GAINS["kp"], GAINS["ki"], 0, GAINS["K"], GAINS["B"], GAINS["FF"]
			)
			delta = abs(positions[current_pos] - measured_pos)
			result &= delta < resolution
			current_pos = (current_pos + 1) % 2
			fxs.send_motor_command(dev_id, fxe.FX_IMPEDANCE, positions[current_pos])
		sleep(time_step)
		# We downsample the display refresh:
		if i % 10 == 0:
			fxu.clear_terminal()
			print(f"Loop {loop_ctr} of {num_time_steps}")
			print(f"Holding position: {positions[current_pos]}")
			print(GAINS)
			fxu.print_device(data, fxe.FX_ACT_PACK)
		# Plotting:
		measurements.append(measured_pos)
		times.append(time() - start_time)
		requests.append(positions[current_pos])

	# Disable the controller, send 0 PWM
	fxs.send_motor_command(dev_id, fxe.FX_VOLTAGE, 0)

	# Plot before we exit:
	title = "Impedance Control Demo"
	plt.plot(times, requests, color="b", label="Desired position")
	plt.plot(times, measurements, color="r", label="Measured position")
	plt.xlabel("Time (s)")
	plt.ylabel("Encoder position")
	plt.title(title)
	plt.legend(loc="upper right")
	fxu.print_plot_exit()
	plt.show()

	# Close device
	print("End of script, closing device.")
	fxs.close(dev_id)

	return True


def main():
	"""
	Standalone impedance control execution
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
	impedance_control(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
