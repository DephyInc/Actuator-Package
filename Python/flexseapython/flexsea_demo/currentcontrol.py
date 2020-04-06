import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def fxCurrentControl(port, baudRate, holdCurrent = [1000], time = 6, time_step = 0.1):
	devId = fxOpen(port, baudRate, logLevel = 6)
	fxStartStreaming(devId, 100, shouldLog = False)
	result = True
	print('Setting controller to current...')
	fxSetGains(devId, 50, 32, 0, 0, 0)
	sleep(0.5)
	prevCurrent = holdCurrent[0]
	num_time_steps = int(time/time_step)

	for current in holdCurrent:
		for i in range(num_time_steps):
			desCurrent = int((current-prevCurrent) * (i / float(num_time_steps)) + prevCurrent)
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
		fxSendMotorCommand(devId, FxCurrent, prevCurrent * (n-i)/n)
		sleep(0.04)

	# Wait for motor to spin down
	fxSendMotorCommand(devId, FxCurrent, 0)
	actPack = fxReadDevice(devId)
	lastAngle = actPack.encoderAngle
	sleep(0.2)
	actPack = fxReadDevice(devId)
	currentAngle = actPack.encoderAngle

	while( abs(currentAngle - lastAngle) > 100):
		lastAngle = currentAngle
		sleep(0.2)
		actPack = fxReadDevice(devId)
		currentAngle = actPack.encoderAngle

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
