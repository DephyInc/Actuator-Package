#!/usr/bin/env python3

"""
FlexSEA Two Position Control Demo
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


def two_position_control(
	fxs,
	port,
	baudRate,
	expTime=13,
	time_step=0.1,
	delta=10000,
	transition_time=1.5,
	resolution=100,
):
	# Open device
	dev_id = fxs.open(port, baudRate, 0)
	fxs.start_streaming(dev_id, resolution, log_en=True)
	sleep(0.1)

	# Setting initial angle and angle waypoints
	act_pack_state = fxs.read_device(dev_id)
	initial_angle = act_pack_state.mot_ang

	# Setting angle waypoints
	positions = [initial_angle, initial_angle + delta]
	current_pos = 0
	num_pos = 2

	# Setting loop duration and transition rate
	num_time_steps = int(expTime / time_step)
	transition_steps = int(transition_time / time_step)

	# Setting gains (dev_id, kp, ki, kd, K, B, ff)
	fxs.set_gains(dev_id, 150, 75, 0, 0, 0, 0)

	# Setting position control at initial position
	fxs.send_motor_command(dev_id, fxe.FX_POSITION, initial_angle)

	# Matplotlib - initialize lists
	requests = []
	measurements = []
	times = []

	start_time = time()
	# Start two position control
	for i in range(num_time_steps):
		sleep(time_step)
		act_pack_state = fxs.read_device(dev_id)
		fxu.clear_terminal()
		measured_pos = act_pack_state.mot_ang
		print(f"Desired:              {positions[current_pos]}")
		print(f"Measured:             {measured_pos}")
		print(f"Difference:           {(measured_pos - positions[current_pos])}\n")
		fxu.print_device(act_pack_state, fxe.FX_ACT_PACK)

		if i % transition_steps == 0:
			current_pos = (current_pos + 1) % num_pos
			fxs.send_motor_command(dev_id, fxe.FX_POSITION, positions[current_pos])

		# Plotting
		times.append(time() - start_time)
		requests.append(positions[current_pos])
		measurements.append(measured_pos)

	# Disable the controller, send 0 PWM
	fxs.send_motor_command(dev_id, fxe.FX_VOLTAGE, 0)
	sleep(0.1)

	# Plot before exit:
	plt.title("Two Position Control Demo")
	plt.plot(times, requests, color="b", label="Desired position")
	plt.plot(times, measurements, color="r", label="Measured position")
	plt.xlabel("Time (s)")
	plt.ylabel("Encoder position")
	plt.legend(loc="upper right")
	fxu.print_plot_exit()
	plt.show()

	# Close device and do device cleanup

	return fxs.close(dev_id)


def main():
	"""
	Standalone two position control execution
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
	two_position_control(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
