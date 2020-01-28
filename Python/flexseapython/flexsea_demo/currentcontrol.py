import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def fxCurrentControl(port, baudRate, holdCurrent = [1000], time = 4, time_step = 0.1):
	devId = fxOpen(port, baudRate, 0)
	fxStartStreaming(devId, 100, True)
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
			print('Holding Current: ', desCurrent, ' mA...')
			actPack = fxReadDevice(devId)
			print('Measured Current: ', actPack.motorCurrent, ' mA...')
			print('Observed delta: ', (actPack.motorCurrent - desCurrent))
		prevCurrent = current

	print('Turning off current control...')
	# ramp down first
	n = 50
	for i in range(0, n):
		fxSendMotorCommand(devId, FxCurrent, prevCurrent * (n-i)/n)
		sleep(0.04)

	# wait for motor to spin down
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

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxCurrentControl(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
