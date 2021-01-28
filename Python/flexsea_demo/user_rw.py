import os, sys
from builtins import input

from flexsea import fxUtils as fxu
from flexsea import fxEnums as fxe
from flexsea import flexsea as flex

labels = [
	"genVar[0]",
	"genVar[1]",
	"genVar[2]",
	"genVar[3]",
	"genVar[4]",
	"genVar[5]",
	"genVar[6]",
	"genVar[7]",
	"genVar[8]",
	"genVar[9]",
]

varsToStream = [
	fxe.FX_GEN_VAR_0,
	fxe.FX_GEN_VAR_1,
	fxe.FX_GEN_VAR_2,
	fxe.FX_GEN_VAR_3,
	fxe.FX_GEN_VAR_4,
	fxe.FX_GEN_VAR_5,
	fxe.FX_GEN_VAR_6,
	fxe.FX_GEN_VAR_7,
	fxe.FX_GEN_VAR_8,
	fxe.FX_GEN_VAR_9,
]


def user_rw(port, baudRate, time=2, time_step=0.1, resolution=100):
	result = True
	stream = Stream(
		port, baudRate, printingRate=2, labels=labels, varsToStream=varsToStream
	)

	while True:
		preamble = ""
		stream()
		command = input(
			"""\'q\': quit the program \n\'w idx val\': writes val to the nth user write value\n\'r\': reads the user values: """
		)
		commands = command.split(" ")
		num_args = len(commands)
		if num_args == 1 and commands[0] == "q":
			break
		elif num_args == 1 and commands[0] == "r":
			readUser(stream.devId)
		elif num_args == 3 and commands[0] == "w":
			try:
				idx = int(commands[1])
				val = int(commands[2])
				if idx > 3 or idx < 0:
					raise Exception("Invalid index recieved, expecting a val between 3 and 0")
			except:
				# Add better exception handling?
				pass
			writeUser(stream.devId, idx, val)
		else:
			print("Invalid input")

		sleep(time_step)
		preamble = "The current read vals are" + str(getUserRead())
		print(preamble)
		# stream.printData(message=preamble)
	del stream
	return result


def main():
	"""
	Standalone user read/write demo execution
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
	user_rw(flex.FlexSEA(), args.port[0], args.baud_rate)


if __name__ == "__main__":
	main()
