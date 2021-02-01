"""
General purpose utilities
"""
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
	print(logo_str)


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
		return os.uname().startswith("arm")
	except AttributeError:
		return False


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
	elif app_type.value == en.FX_EXO.value:
		print_exo(dev_id)
	else:
		raise RuntimeError("Unsupported application type: ", app_type)


def print_exo(exo_state: fx_devs.ExoState):
	"""
	Print Exo info
	"""
	print("[ Printing Exo/ActPack Plus ]\n")
	print("State time:           ", exo_state.state_time)
	print("Accel X:              ", exo_state.accelx)
	print("Accel Y:              ", exo_state.accely)
	print("Accel Z:              ", exo_state.accelz)
	print("Gyro X:               ", exo_state.gyrox)
	print("Gyro Y:               ", exo_state.gyroy)
	print("Gyro Z:               ", exo_state.gyroz)
	print("Motor angle:          ", exo_state.mot_ang)
	print("Motor voltage (mV):   ", exo_state.mot_volt)
	print("Motor current (mA):   ", exo_state.mot_cur)
	print("Battery Current (mA): ", exo_state.batt_volt)
	print("Battery Voltage (mV): ", exo_state.batt_curr)
	print("Battery Temp (C):     ", exo_state.temperature)
	print("genVar[0]:            ", exo_state.genvar_0)
	print("genVar[1]:            ", exo_state.genvar_1)
	print("genVar[2]:            ", exo_state.genvar_2)
	print("genVar[3]:            ", exo_state.genvar_3)
	print("genVar[4]:            ", exo_state.genvar_4)
	print("genVar[5]:            ", exo_state.genvar_5)
	print("genVar[6]:            ", exo_state.genvar_6)
	print("genVar[7]:            ", exo_state.genvar_7)
	print("genVar[8]:            ", exo_state.genvar_8)
	print("genVar[9]:            ", exo_state.genvar_9)
	print("Ankle angle:          ", exo_state.ank_ang)
	print("Ankle velocity:       ", exo_state.ank_vel)


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
		with open(file_name, "r") as com_file:
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
