#!/usr/bin/env python3

"""
FlexSEA Leader-Follower demo
"""
from time import sleep
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex


def two_devices_position_control(fxs, ports, baud_rate):
	"""Runs position control on two devices"""

	exp_time = 8
	time_step = 0.1

	dev_id_0 = fxs.open(ports[0], baud_rate, 0)
	dev_id_1 = fxs.open(ports[1], baud_rate, 0)

	fxs.start_streaming(dev_id_0, 200, log_en=False)
	sleep(0.1)
	fxs.start_streaming(dev_id_1, 200, log_en=False)
	sleep(0.1)

	act_pack_state_0 = fxs.read_device(dev_id_0)
	act_pack_state_1 = fxs.read_device(dev_id_1)

	initial_angle_0 = act_pack_state_0.mot_ang
	initial_angle_1 = act_pack_state_1.mot_ang

	fxs.set_gains(dev_id_0, 50, 3, 0, 0, 0, 0)
	fxs.set_gains(dev_id_1, 50, 3, 0, 0, 0, 0)

	fxs.send_motor_command(dev_id_0, fxe.FX_POSITION, initial_angle_0)
	fxs.send_motor_command(dev_id_1, fxe.FX_POSITION, initial_angle_1)

	num_time_steps = int(exp_time / time_step)
	for i in range(num_time_steps):
		sleep(time_step)
		fxu.clear_terminal()

		act_pack_state_0 = fxs.read_device(dev_id_0)
		act_pack_state_1 = fxs.read_device(dev_id_1)
		current_angle_0 = act_pack_state_0.mot_ang
		current_angle_1 = act_pack_state_1.mot_ang

		print("Device 0:\n---------\n")
		print(f"Desired:              {initial_angle_0}")
		print(f"Measured:             {current_angle_0}")
		print(f"Difference:           {current_angle_0 - initial_angle_0}\n")
		fxu.print_device(act_pack_state_0, fxe.FX_ACT_PACK)

		print("\nDevice 1:\n---------\n")
		print(f"Desired:              {initial_angle_1}")
		print(f"Measured:             {current_angle_1}")
		print(f"Difference:           {current_angle_1 - initial_angle_1}\n", flush=True)
		fxu.print_device(act_pack_state_1, fxe.FX_ACT_PACK)

		fxu.print_loop_count(i, num_time_steps)

	print("Turning off position control...")
	fxs.set_gains(dev_id_0, 0, 0, 0, 0, 0, 0)
	fxs.set_gains(dev_id_1, 0, 0, 0, 0, 0, 0)
	fxs.send_motor_command(dev_id_1, fxe.FX_NONE, 0)
	fxs.send_motor_command(dev_id_0, fxe.FX_NONE, 0)
	sleep(0.5)
	fxs.close(dev_id_0)
	fxs.close(dev_id_1)


def main():
	"""
	Standalone leader-follower demo execution
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
	args = parser.parse_args()
	two_devices_position_control(flex.FlexSEA(), args.ports, args.baud_rate)


if __name__ == "__main__":
	main()
