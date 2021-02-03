#!/usr/bin/env python3

"""
FlexSEA ActPackPlus Current Control Demo
"""
from time import sleep
from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex


def current_control(fxs, port, baud_rate, hold_current=[1000], time=6, time_step=0.1):
	dev_id = fxs.open(port, baud_rate, log_level=6)
	fxs.start_streaming(dev_id, 100, log_en=False)
	app_type = fxs.get_app_type(dev_id)

	if app_type.value != fxe.FX_ACT_PACK.value:
		print(
			"\n Unless you are using an ActPackPlus or have a VERY SPECIFIC "
			"reason to call this script, please exit.  "
			"Ignoring this advice could result in BROKEN electronics, "
			"ROBOTS, COMPUTERS, or in PHYSICAL INJURY. "
			"\n \nWould you like to run the script?\n"
		)
		continue_running = input("Enter yes or no....  ")
		if continue_running.lower() != "yes":
			# button it up
			print("quitting....")
			fxs.close(dev_id)
			return True

	print("Setting controller to current...")
	# Gains are, in order: kp, ki, kd, K, B & ff
	fxs.set_gains(dev_id, 40, 400, 0, 0, 0, 128)
	sleep(0.5)
	prev_current = hold_current[0]
	num_time_steps = int(time / time_step)

	for current in hold_current:
		for i in range(num_time_steps):
			des_current = int(
				(current - prev_current) * (i / float(num_time_steps)) + prev_current
			)
			fxs.send_motor_command(dev_id, fxe.FX_CURRENT, des_current)
			sleep(time_step)
			act_pack = fxs.read_device(dev_id)
			fxu.clear_terminal()
			print("Desired (mA):         ", des_current)
			print("Measured (mA):        ", act_pack.mot_cur)
			print("Difference (mA):      ", (act_pack.mot_cur - des_current), "\n")

			fxu.print_device(act_pack, app_type)
		prev_current = current

	print("Turning off current control...")
	# Ramp down first
	ramp_down_steps = 50
	for step in range(ramp_down_steps):
		des_current = prev_current * (ramp_down_steps - step) / ramp_down_steps
		fxs.send_motor_command(dev_id, fxe.FX_CURRENT, des_current)
		act_pack = fxs.read_device(dev_id)
		fxu.clear_terminal()
		print("Desired (mA):         ", des_current)
		print("Measured (mA):        ", act_pack.mot_cur)
		print("Difference (mA):      ", (act_pack.mot_cur - des_current), "\n")
		fxu.print_device(act_pack, app_type)
		sleep(time_step)

	# When we exit we want the motor to be off
	fxs.send_motor_command(dev_id, fxe.FX_NONE, 0)
	sleep(0.5)

	fxs.close(dev_id)
	return True


def main():
	"""
	Standalone current control execution
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
	current_control(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
