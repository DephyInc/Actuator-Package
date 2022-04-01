"""
General purpose utilities
"""
# pylint: disable=invalid-name
import os
import platform
import yaml
import numpy as np
from . import fxEnums as en
from .dev_spec import AllDevices as fx_devs


def print_logo():
	"""
	print cool logo.
	"""
	logo_str = """
	▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
	██░▄▄▀██░▄▄▄██░▄▄░██░██░██░███░██
	██░██░██░▄▄▄██░▀▀░██░▄▄░██▄▀▀▀▄██
	██░▀▀░██░▀▀▀██░█████░██░████░████
	▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n\t          Beyond Nature™
	"""
	try:
		print(logo_str)
	except UnicodeEncodeError:
		print("\tDephy\n\tBeyond Nature (TM)")


def is_win():
	"""
	Returns true if the OS is windows
	"""
	return "win" in platform.system().lower()


def is_pi():
	"""
	Returns true if the OS is running on an arm. Used to detect Raspberry pi
	"""
	try:
		return os.uname().machine.startswith("arm")
	except AttributeError:
		return False


def is_pi64():
	"""
	Returns true if the OS is running on an Ubuntu 64 for Arm. Used to detect Raspberry pi aarch64
	"""
	try:
		return os.uname().machine.startswith("aarch64")
	except AttributeError:
		return False


def decode(val):
	"""
	Returns decoded version number formatted as x.y.z
	"""
	x = y = z = 0

	if val > 0:
		while val % 2 == 0:
			x += 1
			val /= 2

		while val % 3 == 0:
			y += 1
			val /= 3

		while val % 5 == 0:
			z += 1
			val /= 5

	return f"{x}.{y}.{z}"


def clear_terminal():
	"""
	Clears the terminal - use before printing new values
	"""
	os.system("cls" if is_win() else "clear")


def print_plot_exit():
	"""
	Prints plot exit message
	"""
	if is_win():
		print("In Windows, press Ctrl+Break to exit. Ctrl+C may not work.")


def print_device(dev_id, app_type):
	"""
	Print device type given ann Application type

	Parameters:
	dev_id (int): The device ID.
	app_type (int): application type.
	"""
	if app_type.value == en.FX_ACT_PACK.value:
		print_act_pack(dev_id)
	elif app_type.value == en.FX_NET_MASTER.value:
		print_net_master(dev_id)
	elif app_type.value == en.FX_BMS.value:
		print_bms(dev_id)
	elif app_type.value == en.FX_EB5X.value:
		print_eb5x(dev_id)
	elif app_type.value == en.FX_MD.value:
		print_md(dev_id)
	else:
		raise RuntimeError("Unsupported application type: ", app_type)


def print_eb5x(eb5x_state: fx_devs.EB5xState):
	"""
	Print eb5x info
	"""
	print("[ Printing EB5x/ActPack Plus ]\n")
	print("State time:           ", eb5x_state.state_time)
	print("Accel X:              ", eb5x_state.accelx)
	print("Accel Y:              ", eb5x_state.accely)
	print("Accel Z:              ", eb5x_state.accelz)
	print("Gyro X:               ", eb5x_state.gyrox)
	print("Gyro Y:               ", eb5x_state.gyroy)
	print("Gyro Z:               ", eb5x_state.gyroz)
	print("Motor angle:          ", eb5x_state.mot_ang)
	print("Motor voltage (mV):   ", eb5x_state.mot_volt)
	print("Motor current (mA):   ", eb5x_state.mot_cur)
	print("Battery Current (mA): ", eb5x_state.batt_volt)
	print("Battery Voltage (mV): ", eb5x_state.batt_curr)
	print("Battery Temp (C):     ", eb5x_state.temperature)
	print("genVar[0]:            ", eb5x_state.genvar_0)
	print("genVar[1]:            ", eb5x_state.genvar_1)
	print("genVar[2]:            ", eb5x_state.genvar_2)
	print("genVar[3]:            ", eb5x_state.genvar_3)
	print("genVar[4]:            ", eb5x_state.genvar_4)
	print("genVar[5]:            ", eb5x_state.genvar_5)
	print("genVar[6]:            ", eb5x_state.genvar_6)
	print("genVar[7]:            ", eb5x_state.genvar_7)
	print("genVar[8]:            ", eb5x_state.genvar_8)
	print("genVar[9]:            ", eb5x_state.genvar_9)
	print("Ankle angle:          ", eb5x_state.ank_ang)
	print("Ankle velocity:       ", eb5x_state.ank_vel)


def print_md(md10_state: fx_devs.MD10State):
	"""
	Print md info
	"""
	print("[ Printing Medical Device ]\n")
	print("State time:           ", md10_state.state_time)
	print("Accel X:              ", md10_state.accelx)
	print("Accel Y:              ", md10_state.accely)
	print("Accel Z:              ", md10_state.accelz)
	print("Gyro X:               ", md10_state.gyrox)
	print("Gyro Y:               ", md10_state.gyroy)
	print("Gyro Z:               ", md10_state.gyroz)
	print("Motor angle:          ", md10_state.mot_ang)
	print("Motor voltage (mV):   ", md10_state.mot_volt)
	print("Motor current (mA):   ", md10_state.mot_cur)
	print("Battery Current (mA): ", md10_state.batt_volt)
	print("Battery Voltage (mV): ", md10_state.batt_curr)
	print("Battery Temp (C):     ", md10_state.temperature)
	print("genVar[0]:            ", md10_state.genvar_0)
	print("genVar[1]:            ", md10_state.genvar_1)
	print("genVar[2]:            ", md10_state.genvar_2)
	print("genVar[3]:            ", md10_state.genvar_3)
	print("genVar[4]:            ", md10_state.genvar_4)
	print("genVar[5]:            ", md10_state.genvar_5)
	print("genVar[6]:            ", md10_state.genvar_6)
	print("genVar[7]:            ", md10_state.genvar_7)
	print("genVar[8]:            ", md10_state.genvar_8)
	print("genVar[9]:            ", md10_state.genvar_9)
	print("Ankle angle:          ", md10_state.ank_ang)
	print("Ankle velocity:       ", md10_state.ank_vel)


def print_act_pack(act_pack_state: fx_devs.ActPackState):
	"""
	Print ActPack info
	"""
	print("[ Printing ActPack ]\n")
	print("State time:           ", act_pack_state.state_time)
	print("Accel X:              ", act_pack_state.accelx)
	print("Accel Y:              ", act_pack_state.accely)
	print("Accel Z:              ", act_pack_state.accelz)
	print("Gyro X:               ", act_pack_state.gyrox)
	print("Gyro Y:               ", act_pack_state.gyroy)
	print("Gyro Z:               ", act_pack_state.gyroz)
	print("Motor angle:          ", act_pack_state.mot_ang)
	print("Motor voltage (mV):   ", act_pack_state.mot_volt)
	print("Battery Current (mA): ", act_pack_state.batt_curr)
	print("Battery Voltage (mV): ", act_pack_state.batt_volt)
	print("Battery Temp (C):     ", act_pack_state.temperature)


def print_net_master(net_master_state: fx_devs.NetMasterState):
	"""
	Print net master info
	"""
	print("[ Printing NetMaster ]\n")
	print("State time:        ", net_master_state.state_time)
	print("genVar[0]:         ", net_master_state.genVar_0)
	print("genVar[1]:         ", net_master_state.genVar_1)
	print("genVar[2]:         ", net_master_state.genVar_2)
	print("genVar[3]:         ", net_master_state.genVar_3)
	print("Status:            ", net_master_state.status)
	print(
		"NetNode0 - accelx: ",
		net_master_state.A_accelx,
		", accely: ",
		net_master_state.A_accely,
		" accelz: ",
		net_master_state.A_accelz,
	)
	print(
		"NetNode0 - gyrox:  ",
		net_master_state.A_gyrox,
		", gyroy:  ",
		net_master_state.A_gyroy,
		" gyroz:  ",
		net_master_state.A_gyroz,
	)
	print(
		"NetNode1 - accelx: ",
		net_master_state.B_accelx,
		", accely: ",
		net_master_state.B_accely,
		" accelz: ",
		net_master_state.B_accelz,
	)
	print(
		"NetNode1 - gyrox:  ",
		net_master_state.B_gyrox,
		", gyroy:  ",
		net_master_state.B_gyroy,
		" gyroz:  ",
		net_master_state.B_gyroz,
	)
	print(
		"NetNode2 - accelx: ",
		net_master_state.C_accelx,
		", accely: ",
		net_master_state.C_accely,
		" accelz: ",
		net_master_state.C_accelz,
	)
	print(
		"NetNode2 - gyrox:  ",
		net_master_state.C_gyrox,
		", gyroy:  ",
		net_master_state.C_gyroy,
		" gyroz:  ",
		net_master_state.C_gyroz,
	)
	print(
		"NetNode3 - accelx: ",
		net_master_state.D_accelx,
		", accely: ",
		net_master_state.D_accely,
		" accelz: ",
		net_master_state.D_accelz,
	)
	print(
		"NetNode3 - gyrox:  ",
		net_master_state.D_gyrox,
		", gyroy:  ",
		net_master_state.D_gyroy,
		" gyroz:  ",
		net_master_state.D_gyroz,
	)
	print(
		"NetNode4 - accelx: ",
		net_master_state.E_accelx,
		", accely: ",
		net_master_state.E_accely,
		" accelz: ",
		net_master_state.E_accelz,
	)
	print(
		"NetNode4 - gyrox:  ",
		net_master_state.E_gyrox,
		", gyroy:  ",
		net_master_state.E_gyroy,
		" gyroz:  ",
		net_master_state.E_gyroz,
	)
	print(
		"NetNode5 - accelx: ",
		net_master_state.F_accelx,
		", accely: ",
		net_master_state.F_accely,
		" accelz: ",
		net_master_state.F_accelz,
	)
	print(
		"NetNode5 - gyrox:  ",
		net_master_state.F_gyrox,
		", gyroy:  ",
		net_master_state.F_gyroy,
		" gyroz:  ",
		net_master_state.F_gyroz,
	)
	print(
		"NetNode6 - accelx: ",
		net_master_state.G_accelx,
		", accely: ",
		net_master_state.G_accely,
		" accelz: ",
		net_master_state.G_accelz,
	)
	print(
		"NetNode6 - gyrox:  ",
		net_master_state.G_gyrox,
		", gyroy:  ",
		net_master_state.G_gyroy,
		" gyroz:  ",
		net_master_state.G_gyroz,
	)
	print(
		"NetNode7 - accelx: ",
		net_master_state.H_accelx,
		", accely: ",
		net_master_state.H_accely,
		" accelz: ",
		net_master_state.H_accelz,
	)
	print(
		"NetNode7 - gyrox:  ",
		net_master_state.H_gyrox,
		", gyroy:  ",
		net_master_state.H_gyroy,
		" gyroz:  ",
		net_master_state.H_gyroz,
	)


def print_bms(dev_id):
	"""Print BMS info"""
	# TODO (CA): Implement this function
	print("Printing BMS information not implemented. Device {}".format(dev_id))


def print_loop_count(count, total):
	"""
	Convenience function for printing run counts
	"""
	print("\nRun {} of {}".format(count + 1, total))


def print_loop_count_and_time(count, total, elapsed_time):
	"""
	Convenience function for printing run counts and elapsed time in s.
	"""
	print(
		"\nLoop {} of {} - Elapsed time: {}s".format(count + 1, total, round(elapsed_time))
	)


def sin_generator(amplitude, freq, command_freq):
	"""
	Generate a sine wave of a specific amplitude and frequency
	"""
	num_samples = command_freq / freq
	print("number of samples is: ", int(num_samples))
	in_array = np.linspace(-np.pi, np.pi, int(num_samples))
	sin_vals = amplitude * np.sin(in_array)
	return sin_vals


def line_generator(mag, length, command_freq):
	"""
	Generate a line with specific magnitude
	"""
	num_samples = np.int32(length * command_freq)
	line_vals = [mag for i in range(num_samples)]
	return line_vals


def linear_interp(start, end, points):
	"""
	Interpolates between two positions (A to B)
	"""
	return np.linspace(start, end, points)


def load_ports_from_file(file_name):
	"""
	Loads baud_rate and ports serial ports list from a yaml file.
	"""
	try:
		with open(file_name, "r", encoding="utf-8") as com_file:
			vals = yaml.load(com_file, Loader=yaml.FullLoader)
			return vals["ports"], int(vals["baud_rate"])

	except IOError as err:
		print("Problem loading {}: {}".format(file_name, err))
		print(
			"Copy the ports_template.yaml to a file named ports.yaml"
			"Be sure to use the same format of baud rate on the first line,"
			"and com ports on preceding lines"
		)
		raise err
	except ValueError as err:
		print("Problem with the yaml file syntax or values: {}", err)
		raise err
