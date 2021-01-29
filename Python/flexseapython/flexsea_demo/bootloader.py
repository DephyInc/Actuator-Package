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
	result = False;
	targetName = 'Unknown'

	if (appType == FxActPack):
		print('Your device is an ActPack', flush=True)
	elif (appType == FxExo):
		print('Your device is an Exo or ActPack Plus', flush=True)
	else:
		raise RuntimeError('Unsupported application type: ', appType)

	if (target == 'Habs'):
		print('Activating Habsolute bootloader', flush=True)
		targetID = 0;
		targetName = 'Habsolute'
	elif (target == 'Reg'):
		print('Activating Regulate bootloader', flush=True)
		targetID = 1;
		targetName = 'Regulate'
	elif (target == 'Exe'):
		print('Activating Execute bootloader', flush=True)
		targetID = 2;
		targetName = 'Execute'
	elif (target == 'Mn'):
		print('Activating Manage bootloader', flush=True)
		targetID = 3;
		targetName = 'Manage'
	else:
		raise RuntimeError('Unsupported bootloader target: ', target)		
		
	sleep(1)
	print('Sending signal to target device', flush=True)
	fxActivateBootloader(devId, targetID);

	for timeout in range(1, 60): #60 seconds timeout
		print('Waiting for response from target', flush=True)
		sleep(1)
		state = fxIsBootloaderActivated(devId);
		if state == 0: break

	if (state == 0):
		result = True
		print(targetName, 'bootloader is activated', flush=True)
	else:
		result = False
		print('Unable to activate ', targetName, 'bootloader', flush=True)

	fxClose(devId)
	return result

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
