import os, sys

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import StreamManager

labels = ["genVar[0]", "genVar[1]", "genVar[2]", \
		"genVar[3]", "genVar[4]", "genVar[5]", \
		"genVar[6]", "genVar[7]", "genVar[8]", \
		"genVar[9]"]

varsToStream = [FX_GEN_VAR_0, FX_GEN_VAR_1, FX_GEN_VAR_2, \
			    FX_GEN_VAR_3, FX_GEN_VAR_4, FX_GEN_VAR_5, \
			    FX_GEN_VAR_6, FX_GEN_VAR_7, FX_GEN_VAR_8, \
			    FX_GEN_VAR_9]
																												

def fxUserRW(devId, time = 2, time_step = 0.1,  resolution = 100):
	result = True
	stream = StreamManager(devId,printingRate = 2, labels=labels,varsToStream = varsToStream)
	sleep(0.4)
	try:
		input = raw_input
	except NameError:
		pass
	while True:
		preamble = ""
		stream()
		command = input("""\'q\': quit the program \n\'w idx val\': writes val to the nth user write value\n\'r\': reads the user values: """)
		commands = command.split(' ')
		num_args = len(commands)
		if num_args == 1 and commands[0] == 'q':
			break
		elif num_args == 1 and commands[0] == 'r':
			readUser(devId)
		elif num_args == 3 and commands[0] == 'w':
			try:
				idx = int(commands[1])
				val = int(commands[2])
				if idx > 3 or idx < 0:
					raise Exception("Invalid index recieved, expecting a val between 3 and 0")
			except:
				# Add better exception handling?
				pass
			writeUser(devId,idx,val)
		else:
			print("Invalid input")
		
		sleep(time_step)
		#stream(nt* getUserWrite())	
		preamble = "The current read vals are" + str(getUserRead())
		print(preamble)
		#stream.printData(message=preamble)
	del stream
	return result

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxPositionControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
