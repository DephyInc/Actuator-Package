from signal import signal, SIGINT
import os
import sys
import traceback

if sys.platform == 'win32':		# Need for WebAgg server to work in Python 3.8
	import asyncio
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

thisdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(thisdir)

from flexseapython.pyFlexsea import *
from flexseapython.fxUtil import *
from flexseapython.flexsea_demo.readonly import fxReadOnly
from flexseapython.flexsea_demo.opencontrol import fxOpenControl
from flexseapython.flexsea_demo.currentcontrol import fxCurrentControl
from flexseapython.flexsea_demo.positioncontrol import fxPositionControl
from flexseapython.flexsea_demo.high_speed_test import fxHighSpeedTest
from flexseapython.flexsea_demo.high_stress_test import fxHighStressTest
from flexseapython.flexsea_demo.two_devices_positioncontrol import fxTwoDevicePositionControl
from flexseapython.flexsea_demo.impedancecontrol import fxImpedanceControl
from flexseapython.flexsea_demo.two_devices_leaderfollower import fxLeaderFollower
from flexseapython.flexsea_demo.twopositioncontrol import fxTwoPositionControl

def handler(signal_received, frame):
	sys.exit('\nCTRL-C or SIGINT detected\nExiting ...')


def fxRunFindPoles(port, baudRate):
	devId = fxOpen(port, baudRate, 0)
	if (fxFindPoles(devId) == FxInvalidDevice):
		raise ValueError('fxFindPoles: invalid device ID')


experiments =  [
	(fxReadOnly,					"Read Only"),
	(fxOpenControl, 				"Open Control"),
	(fxCurrentControl, 				"Current Control"),
	(fxPositionControl,				"Position Control"),
	(fxImpedanceControl, 			"Impedance Control"),
	# (fxUserRW, 					"User RW"),
	(fxRunFindPoles,				"Find Poles"),
	(fxTwoPositionControl, 			"Two Positions Control"),
	(fxHighSpeedTest, 				"High Speed Test"),
	(fxHighStressTest, 				"High Stress Test"),
	(fxTwoDevicePositionControl,	"Two Devices Position Control"),
	(fxLeaderFollower,				"Two Devices Leader Follower Control"),
]
IDX_MAX			  = len(experiments) - 1
IDX_MAX_STR		  = str(IDX_MAX)
IDX_MAX_1_DEV	  = IDX_MAX - 4		# Experiments [0 - 6] accept 1 device only
IDX_MAX_1_DEV_STR = str(IDX_MAX_1_DEV)


def print_experiments():
	""" Print list of available experiments """
	for i in range(IDX_MAX+1):
		print('[' + str(i) + ']', experiments[i][1])


def print_usage_exit(prog_name: str):
	""" Some error occurred.  Print help message and exit. """
	print('\nUsage:\tPython', prog_name, '[experiment_number (0 - ' + \
			IDX_MAX_STR + ') connected_devices (1 - 2)]')
	print('\t"connected_devices" ONLY required for experiment_number [' + str(IDX_MAX_1_DEV + 1)  + \
			'- ' + IDX_MAX_STR + '].\n' + \
			'\tOther experiments use [1] device by default.\n')
	print_experiments()
	sys.exit(0)


def parse_exp_num( argv):
	""" Parse command line args to get the experiment number """
	exp_num_str = argv[1]
	if not exp_num_str.isdecimal():
		print_usage_exit(argv[0])
	exp_num = int(exp_num_str)
	if exp_num < 0 or exp_num > IDX_MAX:
		print('\nInvalid  exp_num:', exp_num)
		print_usage_exit(argv[0])
	return exp_num


def parse_num_dev(argv, exp_num: int):
	""" Parse command line args to get count of connected devices """
	if len(argv) != 3:					# Defensive programming
		print_usage_exit(argv[0])
	num_dev_str = argv[2]
	if not num_dev_str.isdecimal():
		print_usage_exit(argv[0])
	num_dev = int(num_dev_str)
	if num_dev < 1 or num_dev > 2:
		print('\nInvalid num_dev:', num_dev)
		print_usage_exit(argv[0])
	elif num_dev == 2 and exp_num <= IDX_MAX_1_DEV:
		print('\nExperiment [' + str(exp_num) + '] only accepts [1] connected device.')
		print_usage_exit(argv[0])
	return num_dev


def get_exp_num():
	""" Prompt user for the experiment number """
	print_experiments()
	if (exp_num := input('Choose experiment number\t[q to quit]:\t')) == 'q':
		sys.exit('Quitting ...')
	if not exp_num.isdecimal():
		sys.exit('Please choose an experiment between [0 - ' + str(IDX_MAX) + ']')
	exp_num = int(exp_num)
	if exp_num < 0 or exp_num > IDX_MAX:
		sys.exit('Please choose an experiment between [0 - ' + str(IDX_MAX) + ']')
	return exp_num


def get_num_dev(exp_num: int):
	""" Prompt user for number of connected devices """
	if (num_dev := input('Enter connected devices [1 - 2] [q to quit]:\t')) == 'q':
		sys.exit('Quitting ...')
	if not num_dev.isdecimal():
		sys.exit('Please provide a number between [1 - 2]')
	num_dev = int(num_dev)
	if num_dev < 1 or num_dev > 2:
		sys.exit('Please provide a number between [1 - 2]')
	if num_dev == 2 and exp_num <= (IDX_MAX - 3):
		print('Experiment [' + str(exp_num) + '] only accepts [1] connected device.')
		print_usage_exit(argv[0])
	return num_dev


def main(argv):
	signal(SIGINT, handler)				# Handle Ctrl-C or SIGINT

	exp_num = -1
	num_dev = 1

	num_cl_args = len(argv) - 1			# Get count of command line arguments
	if num_cl_args == 0:				# No command-line arguments
		exp_num = get_exp_num()
		if exp_num > IDX_MAX_1_DEV:		# 1 or 2 connected devices
			num_dev = get_num_dev(exp_num)
	elif num_cl_args  < 3:				# 1-2 command-line arguments provided
		exp_num = parse_exp_num( argv)
		if num_cl_args == 2:
			num_dev = parse_num_dev(argv, exp_num)
	else:								# Too many command line arguments provided
		print('\nToo many command line arguments provided.')
		print_usage_exit(argv[0])
	print('Running Experiment [' + str(exp_num) + '] with [' + str(num_dev) + '] connected device(s)')

	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports, baudRate = loadPortsFromFile(fpath)
	baudRate = int(baudRate)
	print('Using ports:\t', ports)
	print('Using baud rate:', baudRate)

	try:
		if exp_num > IDX_MAX_1_DEV:		# 1 or 2 connected devices
			if num_dev == 1:
				experiments[exp_num][0](baudRate, ports[0])
			else:
		 		experiments[exp_num][0](baudRate, ports[0], ports[1])
		else:	# Only 1 connected device permitted. Note order of ports/baudRate is reversed
		 	experiments[exp_num][0](ports[0], baudRate)

	except Exception as e:
		sys.exit(e)

	print('\nExiting fxMain()')


if __name__ == '__main__':
	main(sys.argv)
