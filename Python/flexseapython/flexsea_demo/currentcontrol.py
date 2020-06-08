import os, sys
from time import sleep
from flexseapython.fxUtil import *

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

def fxCurrentControl(port, baudRate, holdCurrent = [1000], time = 6, time_step = 0.1):
	devId = fxOpen(port, baudRate, logLevel = 6)
	fxStartStreaming(devId, 100, shouldLog = False)
	appType = fxGetAppType(devId)

	if(appType != FxActPack):
		print('\n Unless you are using an ActPackPlus or have a VERY SPECIFIC '
			  'reason to call this script, please exit.  '
			  'Ignoring this advice could result in BROKEN electronics, '
			  'ROBOTS, COMPUTERS, or in PHYSICAL INJURY. '
			  '\n \nWould you like to run the script?\n')
		continueRunning=input("Enter yes or no....  ")
		if continueRunning.lower() != 'yes':
			#button it up
			print('quitting....')
			fxClose(devId)
			return True

	result = True
	print('Setting controller to current...')
	fxSetGains(devId, 50, 32, 0, 0, 0)
	sleep(0.5)
	prevCurrent = holdCurrent[0]
	num_time_steps = int(time/time_step)

	for current in holdCurrent:
		for i in range(num_time_steps):
			desCurrent = int((current - prevCurrent) * (i / float(num_time_steps)) + prevCurrent)
			fxSendMotorCommand(devId, FxCurrent, desCurrent)
			sleep(time_step)
			actPack = fxReadDevice(devId)
			clearTerminal()
			print('Desired  (mA):        ', desCurrent)
			print('Measured  (mA):       ', actPack.motorCurrent)
			print('Difference (mA):      ', (actPack.motorCurrent - desCurrent), '\n')
			printDevice(actPack)
		prevCurrent = current

	print('Turning off current control...')
	# Ramp down first
	n = 50
	for i in range(n):
		desCurrent = prevCurrent * (n-i)/n
		fxSendMotorCommand(devId, FxCurrent, desCurrent)
		actPack = fxReadDevice(devId)
		clearTerminal()
		print('Desired  (mA):        ', desCurrent)
		print('Measured  (mA):       ', actPack.motorCurrent)
		print('Difference (mA):      ', (actPack.motorCurrent - desCurrent), '\n')
		printDevice(actPack)
		sleep(time_step)

	# When we exit we want the motor to be off
	fxSendMotorCommand(devId, FxNone, 0)
	sleep(0.5)

	fxClose(devId)
	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxCurrentControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
