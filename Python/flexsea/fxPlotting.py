"""
Plotting Utilities
"""
import matplotlib
import matplotlib.pyplot as plt
from . import fxEnums as en
from . import fxUtils as fxu


def plot_setpoint_vs_desired(
	dev_id,
	fig,
	ctrl_type,
	sig_freq,
	sig_amplitude,
	sig_type,
	cmd_freq,
	times,
	reqs,
	measurements,
	cycle_stop_times,
):
	"""
	Figure: setpoint, desired vs measured
	"""
	plt.figure(fig)
	fig += 1

	# Current controller:
	if ctrl_type == en.HSS_CURRENT:
		title_str = (
			"Current control with {:.0f} Hz, {:.1f} mA {} and {:.0f} Hz commands (ID {})"
		)
		title = title_str.format(sig_freq, sig_amplitude, sig_type, cmd_freq, dev_id)
		plt.ylabel("Motor current (mA)")

	# Position controller:
	elif ctrl_type == en.HSS_POSITION:
		title_str = (
			"Position control with {:.0f} Hz, {:.0f} tick{} {} and {:.0f} Hz commands (ID {})"
		)
		title = title_str.format(
			sig_freq,
			sig_amplitude,
			("s" if sig_amplitude > 1 else ""),  # Pluralizes tick
			sig_type,
			cmd_freq,
			dev_id,
		)
		plt.ylabel("Encoder position (tick)")

	# Common info:
	plt.plot(times, reqs, color="b", label="Desired")
	plt.plot(times, measurements, color="r", label="Measured")
	plt.xlabel("Time (s)")
	plt.title(title, wrap=True)
	plt.legend(loc="upper right")

	# Style parameters and webb server address for external clients
	matplotlib.rcParams.update(
		{"figure.constrained_layout.use": True, "figure.constrained_layout.h_pad": 0.5}
	)
	if fxu.is_pi():
		matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

	# Draw a vertical line at the end of each cycle
	for endpoints in cycle_stop_times:
		plt.axvline(x=endpoints, color="xkcd:light grey", linestyle="--")

	return fig


def plot_exp_stats(dev_id, fig, write_cmd_times, read_cmd_times):
	"""
	Multiple figures: command and stream times in linear and occurrence log
	Supports two types at once
	"""
	fig = plot_exp_stats_one_type(dev_id, fig, write_cmd_times, "Write")
	fig = plot_exp_stats_one_type(dev_id, fig, read_cmd_times, "Read")
	return fig


def plot_exp_stats_one_type(dev_id, fig, action_times, title):
	"""
	Two figures: command and stream times in linear and occurrence log
	"""

	# Figure: command time vs time, linear scale
	plt.figure(fig)
	fig += 1
	action_times = [i * 1000 for i in action_times]
	# Convert command times into ms
	plt.plot(action_times, color="b", label="Times")
	plt.title(title + " Time vs Time" " (ID:" + str(dev_id) + ")")
	plt.legend(loc="upper right")
	plt.xlabel("Time (ms)")
	plt.ylabel("Command Time (ms)")

	# Figure: time occurrences, log
	plt.figure(fig)
	fig += 1
	plt.yscale("log")
	plt.hist(action_times, bins=100, label="Setpoints")
	plt.yscale("log")
	plt.title(title + " Time Occurrence" + " (ID:" + str(dev_id) + ")")
	plt.legend(loc="upper right")
	plt.xlabel("Time (ms)")
	plt.ylabel("Occurrences")

	return fig
