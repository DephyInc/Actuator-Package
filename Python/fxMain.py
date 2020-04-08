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

#List of available experiments.
#Format is: functionName, text string, max number of devices
experiments = [
	(fxReadOnly,					"Read Only",							1),
	(fxOpenControl, 				"Open Control",							1),
	(fxCurrentControl, 				"Current Control",						1),
	(fxPositionControl,				"Position Control",						1),
	(fxImpedanceControl, 			"Impedance Control",					1),
	#(fxUserRW, 					"User RW",								1),
	(fxRunFindPoles,				"Find Poles",							1),
	(fxTwoPositionControl, 			"Two Positions Control",				1),
	(fxHighSpeedTest, 				"High Speed Test",						2),
	(fxHighStressTest, 				"High Stress Test",						2),
	(fxTwoDevicePositionControl,	"Two Devices Position Control",			2),
	(fxLeaderFollower,				"Two Devices Leader Follower Control",	2),
]

MAX_EXPERIMENT			= len(experiments) - 1
MAX_EXPERIMENT_STR		= str(MAX_EXPERIMENT)
MAX_DEVICES				= 2

#Print list of available experiments
def print_experiments():
	for i in range(MAX_EXPERIMENT+1):
		print('[' + str(i) + ']', experiments[i][1])
	print('')

#Some error occurred. Print help message and exit.
def print_usage_exit(prog_name: str):
	print('\nUsage:\tPython', prog_name, '[experiment_number (0 - ' + \
			MAX_EXPERIMENT_STR + ') connected_devices (1 - 2)]')
	print('\t"connected_devices" ONLY required for specific experiments\n' +
			'\tOther experiments use [1] device by default.\n')
	sys.exit(0)

#Obtain experiment number from argument list or by prompting user
def get_exp_num(num_cl_args, argv):
	exp_num = -1
	if(num_cl_args > 0):
		#Get it from the command line argument list
		exp_num = argv[1]
	else:
		#Or prompt the user for it
		if(exp_num := input('Choose experiment number [q to quit]: ')) == 'q':
			sys.exit('Quitting ...')
	#Make sure it's valid and in range:
	if(not exp_num.isdecimal()):	#Filter out letters
		sys.exit('Please choose an experiment between [0 - ' + str(MAX_EXPERIMENT) + ']')
	exp_num = int(exp_num)			#Make sure is a int and not a string
	if((exp_num < 0) or (exp_num > MAX_EXPERIMENT)):	#And make sure it's in range
		sys.exit('Please choose an experiment between [0 - ' + str(MAX_EXPERIMENT) + ']')

	return exp_num

#Obtain number of devices from argument list or by prompting user
def get_dev_num(num_cl_args, argv, exp_num):
	dev_num = 1
	
	#We only bother if this experiment supports more than 1 device
	if(experiments[exp_num][2] > 1):
		print('Max number of devices for this experiment:', experiments[exp_num][2])
	else:
		#Nothing to do here, return default = 1
		return dev_num
	
	#Code below is executed when this experiment supports more than # device	
	if(num_cl_args > 1):
		#Get it from the command line argument list
		dev_num = argv[2]
	else:
		#Or prompt the user for it
		if(dev_num := input('Enter connected devices [q to quit]: ')) == 'q':
			sys.exit('Quitting ...')
	
	#Make sure it's valid and in range:
	if(not dev_num.isdecimal()):	#Filter out letters
		sys.exit('Please choose a valid number of devices.')
	dev_num = int(dev_num)			#Make sure is a int and not a string
	if((dev_num < 1) or (dev_num > experiments[exp_num][2])):	#And make sure it's in range
		sys.exit('Please choose a valid number of devices.')

	return dev_num

def main(argv):
	signal(SIGINT, handler)				# Handle Ctrl-C or SIGINT
	
	exp_num = -1
	num_dev = 1
	
	print('\n>>> Actuator Package Python Demo Scripts <<<\n')
	
	#Handles command line arguments and experiment setup
	num_cl_args = len(argv) - 1	# Get count of command line arguments
	if(num_cl_args < 3):
		print_experiments()
		exp_num = get_exp_num(num_cl_args, argv)
		dev_num = get_dev_num(num_cl_args, argv, exp_num)
	else:
		print('\nToo many command line arguments provided.')
		print_usage_exit(argv[0])
	
	print('Running Experiment [' + str(exp_num) + '] with [' + str(num_dev) + '] connected device(s)')
	
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	fpath = scriptPath + '/flexseapython/com.txt'
	ports, baudRate = loadPortsFromFile(fpath)
	baudRate = int(baudRate)
	print('Using ports:\t', ports)
	print('Using baud rate:', baudRate)
	
	#Time to call the demo script:
	try:
		if(dev_num == 1):
			experiments[exp_num][0](ports[0], baudRate)
		elif(dev_num == 2):
			experiments[exp_num][0](baudRate, ports[0], ports[1])
	except Exception as e:
		sys.exit(e)

	print('\nExiting fxMain()')

if __name__ == '__main__':
	main(sys.argv)
