#!/usr/bin/env python3

"""
FlexSEA Position Control Demo
"""
from time import sleep
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex


def position_control(fxs, port, baud_rate, time=8, time_step=0.1, resolution=100):
	"""
	Implement position control
	"""
	dev_id = fxs.open(port, baud_rate, log_level=6)
	fxs.start_streaming(dev_id, resolution, log_en=False)
	sleep(0.1)

	act_pack_state = fxs.read_device(dev_id)
	fxu.print_device(act_pack_state, fxe.FX_ACT_PACK)
	initial_angle = act_pack_state.mot_ang

	# Gains are, in order: kp, ki, kd, K, B & ff
	fxs.set_gains(dev_id, 400, 50, 0, 0, 0, 0)

	fxs.send_motor_command(dev_id, fxe.FX_POSITION, initial_angle)

	num_time_steps = int(time / time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		fxu.clear_terminal()
		act_pack_state = fxs.read_device(dev_id)
		current_angle = act_pack_state.mot_ang
		print("Desired:              ", initial_angle)
		print("Measured:             ", current_angle)
		print("Difference:           ", current_angle - initial_angle, "\n", flush=True)
		fxu.print_device(act_pack_state, fxe.FX_ACT_PACK)
		fxu.print_loop_count(i, num_time_steps)

	# When we exit we want the motor to be off
	fxs.send_motor_command(dev_id, fxe.FX_NONE, 0)
	sleep(0.5)
	fxs.close(dev_id)

	return True


def main():
	"""
	Standalone position control execution
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
	position_control(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
