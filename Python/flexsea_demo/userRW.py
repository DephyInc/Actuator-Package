import os, sys
from builtins import input

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from flexseapython.fxUtil import *

labels = ["genVar[0]", "genVar[1]", "genVar[2]", \
		"genVar[3]", "genVar[4]", "genVar[5]", \
		"genVar[6]", "genVar[7]", "genVar[8]", \
		"genVar[9]"]

varsToStream = [FX_GEN_VAR_0, FX_GEN_VAR_1, FX_GEN_VAR_2, \
			    FX_GEN_VAR_3, FX_GEN_VAR_4, FX_GEN_VAR_5, \
			    FX_GEN_VAR_6, FX_GEN_VAR_7, FX_GEN_VAR_8, \
			    FX_GEN_VAR_9]
																												

def fxUserRW(port, baudRate, time = 2, time_step = 0.1,  resolution = 100):
	result = True
	stream = Stream(port, baudRate, printingRate = 2, labels=labels, varsToStream = varsToStream)

	while True:
		preamble = ""
		stream()
		command = input("""\'q\': quit the program \n\'w idx val\': writes val to the nth user write value\n\'r\': reads the user values: """)
		commands = command.split(' ')
		num_args = len(commands)
		if num_args == 1 and commands[0] == 'q':
			break
		elif num_args == 1 and commands[0] == 'r':
			readUser(stream.devId)
		elif num_args == 3 and commands[0] == 'w':
			try:
				idx = int(commands[1])
				val = int(commands[2])
				if idx > 3 or idx < 0:
					raise Exception("Invalid index recieved, expecting a val between 3 and 0")
			except:
				# Add better exception handling?
				pass
			writeUser(stream.devId,idx,val)
		else:
			print("Invalid input")
		
		sleep(time_step)
		preamble = "The current read vals are" + str(getUserRead())
		print(preamble)
		#stream.printData(message=preamble)
	del stream
	return result

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxUserRW(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
