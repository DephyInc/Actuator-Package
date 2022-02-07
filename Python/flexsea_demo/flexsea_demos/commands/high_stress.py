from time import sleep
from time import time
from typing import List

from cleo import Command
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flexsea import fxEnums as fxe
from flexsea import fxPlotting as fxp
from flexsea import fxUtils as fxu

from flexsea_demos.device import Device
from flexsea_demos.utils import setup


# ============================================
#             HighStressCommand
# ============================================
class HighStressCommand(Command):
	"""
	Runs the high stress demo.

	high_stress
		{paramFile : Yaml file with demo parameters.}
	"""

	# Schema of parameters required by the demo
	required = {
		"ports": List,
		"baud_rate": int,
		"cmd_freq": int,
		"position_amplitude": int,
		"current_amplitude": int,
		"position_freq": int,
		"current_freq": int,
		"current_asymmetric_g": float,
		"nLoops": int,
	}

	__name__ = "high_stress"

	# -----
	# constructor
	# -----
	def __init__(self):
		super().__init__()
		self.ports = []
		self.baud_rate = 0
		self.cmd_freq = 0
		self.position_amplitude = 0
		self.current_amplitude = 0
		self.position_freq = 0
		self.current_freq = 0
		self.current_asymmetric_g = 0.0
		self.nLoops = 0

		self.dt = 0
		self.devices = []
		self.cur_gains = {"KP": 40, "KI": 400, "KD": 0, "K": 0, "B": 0, "FF": 128}
		self.pos_gains = {"KP": 100, "KI": 10, "KD": 0, "K": 0, "B": 0, "FF": 0}
		self.cmd_count = 0
		self.start_time = 0
		self.timestamps = []
		self.cycle_stop_times = []
		self.figure_ind = 1
		self.samples = {
			"position_samples": [],
			"current_samples": [],
			"current_samples_line": [],
		}

		matplotlib.use("WebAgg")
		if fxu.is_pi():
			matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

	# -----
	# handle
	# -----
	def handle(self):
		"""
		Runs the high stress demo.
		"""
		setup(self, self.required, self.argument("paramFile"), self.__name__)
		self.dt = float(1 / (float(self.cmd_freq)))
		for i, port in enumerate(self.ports):
			self.devices.append({"port": Device(self.fxs, port, self.baud_rate)})
			self.devices[i]["initial_pos"] = self.devices[i]["port"].initial_pos
			self.devices[i]["data"] = self.devices[i]["port"].read()
			self.devices[i]["read_times"] = []
			self.devices[i]["gains_times"] = []
			self.devices[i]["motor_times"] = []
			self.devices[i]["pos_requests"] = []
			self.devices[i]["pos_measurements"] = []
			self.devices[i]["curr_requests"] = []
			self.devices[i]["curr_measurements"] = []

		self._get_samples()
		self.start_time = time()
		self.cmd_count = 0
		self._high_stress()

	# -----
	# _high_stress
	# -----
	def _high_stress(self):
		for rep in range(self.nLoops):
			fxu.print_loop_count_and_time(rep, self.nLoops, time() - self.start_time)
			self._step0(rep)
			self._step1(rep)
			self._step2()
			self._step3()
			self._step4()
			self._step5()
			self.cycle_stop_times.append(time() - self.start_time)

		elapsed_time = time() - self.start_time

		for dev in self.devices:
			dev["port"].motor(fxe.FX_VOLTAGE, 0)
		sleep(0.1)

		self._print_stats(elapsed_time)
		self._plot()
		for dev in self.devices:
			dev["port"].close()

	# -----
	# _step0
	# -----
	def _step0(self, rep):
		sleep(self.dt)
		cmds = []
		for dev in self.devices:
			if rep:
				initial_cmd = {"cur": 0, "pos": dev["port"].get_pos()}
			else:
				initial_cmd = {"cur": 0, "pos": dev["port"].initial_pos}
			cmds.append(initial_cmd)
		self._send_and_time_cmds(cmds, fxe.FX_POSITION, self.pos_gains, True)

	# -----
	# _step1
	# -----
	def _step1(self, rep):
		if rep:
			# Create interpolation angles for each device
			lin_samples = []
			for dev in self.devices:
				lin_samples.append(
					fxu.linear_interp(dev["data"].mot_ang, dev["initial_pos"], 360)
				)

			for samples in np.array(lin_samples).transpose():
				cmds = [{"cur": 0, "pos": sample} for sample in samples]
				sleep(self.dt)
				self._send_and_time_cmds(cmds, fxe.FX_POSITION, self.pos_gains, False)
				self.cmd_count += 1

	# -----
	# _step2
	# -----
	def _step2(self):
		for sample in self.samples["position_samples"]:
			cmds = []
			for dev in self.devices:
				cmds.append({"cur": 0, "pos": sample + dev["initial_pos"]})
			sleep(self.dt)
			self._send_and_time_cmds(cmds, fxe.FX_POSITION, self.pos_gains, False)
			self.cmd_count += 1

	# -----
	# _step3
	# -----
	def _step3(self):
		cmds = [{"cur": 0, "pos": dev["initial_pos"]} for dev in self.devices]
		# TODO(CA): Investigate this problem and remove the hack below
		# Set gains several times since they might not get set when only set once.
		for _ in range(5):
			self._send_and_time_cmds(cmds, fxe.FX_CURRENT, self.cur_gains, True)
			sleep(self.dt)

	# -----
	# _step4
	# -----
	def _step4(self):
		for sample in self.samples["current_samples"]:
			sleep(self.dt)
			# use more current on "way back" to get closer to start
			sample = np.int64(sample)
			# Apply gain
			if sample > 0:
				sample = np.int64(self.current_asymmetric_g * sample)
			cmds = [{"cur": sample, "pos": dev["initial_pos"]} for dev in self.devices]

			sleep(self.dt)
			self._send_and_time_cmds(cmds, fxe.FX_CURRENT, self.cur_gains, False)
			self.cmd_count += 1

	# -----
	# _step5
	# -----
	def _step5(self):
		for sample in self.samples["current_samples_line"]:
			cmds = [{"cur": sample, "pos": dev["initial_pos"]} for dev in self.devices]
			sleep(self.dt)
			self._send_and_time_cmds(cmds, fxe.FX_CURRENT, self.cur_gains, False)
			self.cmd_count += 1

	# -----
	# _get_samples
	# -----
	def _get_samples(self):
		self.samples["position_samples"] = fxu.sin_generator(
			self.position_amplitude, self.position_freq, self.cmd_freq
		)
		self.samples["current_samples"] = fxu.sin_generator(
			self.current_amplitude, self.current_freq, self.cmd_freq
		)
		self.samples["current_samples_line"] = fxu.line_generator(0, 0.5, self.cmd_freq)

	# -----
	# _send_and_time_cmds
	# -----
	def _send_and_time_cmds(self, cmds, motor_cmd, gains, set_gains):
		try:
			assert motor_cmd in [fxe.FX_POSITION, fxe.FX_CURRENT]
		except AssertionError:
			msg = "Unexpected motor command, only FX_POSITION, FX_CURRENT allowed"
			raise AssertionError(msg)

		for dev, cmd in zip(self.devices, cmds):
			tstart = time()
			dev["data"] = dev["port"].read()
			dev["read_times"].append(time() - tstart)

			if set_gains:
				tstart = time()
				# Gains are, in order: kp, ki, kd, K, B & ff
				dev["port"].set_gains(gains)
				dev["gains_times"].append(time() - tstart)
			else:
				dev["gains_times"].append(0)

			cmd_val = cmd["cur"] if motor_cmd == fxe.FX_CURRENT else cmd["pos"]

			tstart = time()
			dev["port"].motor(motor_cmd, cmd_val)
			dev["motor_times"].append(time() - tstart)
			dev["pos_requests"].append(cmd["pos"])
			dev["pos_measurements"].append(dev["data"].mot_ang)
			dev["curr_requests"].append(cmd["cur"])
			dev["curr_measurements"].append(dev["data"].mot_cur)

		self.timestamps.append(time() - self.start_time)

	# -----
	# _print_stats
	# -----
	def _print_stats(self, elapsed_time):
		print("\nFinal Stats:")
		print("------------")
		print(f"Number of commands sent: {self.cmd_count}")
		print(f"Total time (s): {elapsed_time}")
		print(f"Requested command frequency: {self.cmd_freq}")
		print(f"Actual command frequency (Hz): {self.cmd_count / elapsed_time}")
		print(f"\ncurrent_samples_line: {len(self.samples['current_samples_line'])}")
		print(f"size(TIMESTAMPS): {len(self.timestamps)}")
		print(f"size(currentRequests): {len(self.devices[0]['curr_requests'])}")
		print(
			f"size(currentMeasurements0): {len(self.devices[0]['curr_measurements'])}"
		)
		print(f"size(SET_GAINS_TIMES): {len(self.devices[0]['gains_times'])}\n")

	# -----
	# _plot
	# -----
	def _plot(self, type_str="sine wave"):
		for dev in self.devices:
			self.figure_ind = fxp.plot_setpoint_vs_desired(
				dev["port"].dev_id,
				self.figure_ind,
				fxe.HSS_CURRENT,
				self.current_freq,
				self.current_amplitude,
				type_str,
				self.cmd_freq,
				self.timestamps,
				dev["curr_requests"],
				dev["curr_measurements"],
				self.cycle_stop_times,
			)

			self.figure_ind = fxp.plot_setpoint_vs_desired(
				dev["port"].dev_id,
				self.figure_ind,
				fxe.HSS_POSITION,
				self.position_freq,
				self.position_amplitude,
				type_str,
				self.cmd_freq,
				self.timestamps,
				dev["pos_requests"],
				dev["pos_measurements"],
				self.cycle_stop_times,
			)

		plt.show()
		sleep(0.1)
		fxu.print_plot_exit()
