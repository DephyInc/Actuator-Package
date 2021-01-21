import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)

from flexseapython.fxUtil import *

def fxBootloader(port, baudRate, target):
	debugLoggingLevel = 0	# 6 is least verbose, 0 is most verbose
	dataLog = True 			# False means no logs will be saved
	devId =	fxOpen(port, baudRate, debugLoggingLevel)
	appType = fxGetAppType(devId)

	if (appType == FxActPack):
		print('Your device is an ActPack')
	elif (appType == FxExo):
		print('Your device is an Exo or ActPack Plus')
	else:
		raise RuntimeError('Unsupported application type: ', appType)

	if (target == 'Habs'):
		print('Activating Habsolute bootloader')
		targetID = 0;
	elif (target == 'Reg'):
		print('Activating Regulate bootloader')
		targetID = 1;
	elif (target == 'Exe'):
		print('Activating Execute bootloader')
		targetID = 2;
	elif (target == 'Mn'):
		print('Activating Manage bootloader')
		targetID = 3;
	else:
		raise RuntimeError('Unsupported bootloader target: ', target)		
		
	fxActivateBootloader(devId, targetID);
	
	input("Press Enter to continue...")
	
	state = fxIsBootloaderActivated(devId);
	
	if (state == 0):
		print(target, 'bootloader is activated')
	else:
		print(target, 'bootloader is not activated')
		
	
	fxClose(devId)
	return True

if __name__ == '__main__':
	baudRate = int(sys.argv[1])
	port = sys.argv[2]
	target = sys.argv[3]
	try:
		loadSuccess = loadFlexsea()
		if(not loadSuccess):
			raise Exception('Could not load FlexSEA libraries')
		fxBootloader(port, baudRate, target)
	except Exception as e:
		print("broke: " + str(e))
		pass
