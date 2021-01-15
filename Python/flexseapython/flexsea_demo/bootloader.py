import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)

from flexseapython.fxUtil import *

def fxBootloader(port, baudRate, time = 8, time_step = 0.1):
	debugLoggingLevel = 0	# 6 is least verbose, 0 is most verbose
	dataLog = True 			# False means no logs will be saved
	devId =	fxOpen(port, baudRate, debugLoggingLevel)
	appType = fxGetAppType(devId)

	if (appType == FxActPack):
		print('\nYour device is an ActPack.\n')
		input("Press Enter to continue...")
	elif (appType == FxExo):
		print('\nYour device is an Exo or ActPack Plus.\n')
		input("Press Enter to continue...")
	else:
		raise RuntimeError('Unsupported application type: ', appType)

	fxActivateBootloader(devId, 2);
	fxClose(devId)
	return True

if __name__ == '__main__':
	baudRate = int(sys.argv[1])
	port = sys.argv[2]
	try:
		loadSuccess = loadFlexsea()
		if(not loadSuccess):
			raise Exception('Could not load FlexSEA libraries')
		fxBootloader(port, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
