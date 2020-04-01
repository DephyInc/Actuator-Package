import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *

def fxOpenControl(port, baudRate, time = 2, num_times = 2, time_resolution = 0.1, maxVoltage = 3000, sign = -1):
	devId = fxOpen(port, baudRate, 0)
	fxStartStreaming(devId, 100, True)
	print("Setting open control...")
	fxSendMotorCommand(devId, FxVoltage, 0)
	sleep(0.5)
	numSteps = int((time/2)/time_resolution)
	direction = 1

	for time in range(0, num_times):
		direction = direction * sign

		for i in range(0, numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * (i*1.0 / numSteps)
			fxSendMotorCommand(devId, FxVoltage, mV)
			clearTerminal()
			print('Open control demo... \nRamping up open controller...')
			exoState = fxReadDevice(devId)
			print('State time: ', exoState.timestamp)
			print('Accel X: ', exoState.accelx, ', Accel Y: ', exoState.accely, ' Accel Z: ', exoState.accelz)
			print('Gyro X: ', exoState.gyrox, ', Gyro Y: ', exoState.gyroy, ' Gyro Z: ', exoState.gyroz)
			print('Motor angle: ', exoState.encoderAngle, ', Motor voltage: ', exoState.motorVoltage)

		for i in range(0, numSteps):
			sleep(time_resolution)
			mV = direction * maxVoltage * ((numSteps - i)*1.0 / numSteps)
			fxSendMotorCommand(devId, FxVoltage, mV)
			clearTerminal()
			print('Open control demo... \nRamping down open controller...')
			exoState = fxReadDevice(devId)
			print('State time: ', exoState.timestamp)
			print('Accel X: ', exoState.accelx, ', Accel Y: ', exoState.accely, ' Accel Z: ', exoState.accelz)
			print('Gyro X: ', exoState.gyrox, ', Gyro Y: ', exoState.gyroy, ' Gyro Z: ', exoState.gyroz)
			print('Motor angle: ', exoState.encoderAngle, ', Motor voltage: ', exoState.motorVoltage)

	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxOpenControl(baudRate)
	except Exception as e:
		print("Broke... ")
		print(str(e))
