import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.fxUtil import *

def fxReadOnly(port, baudRate, time = 6,time_step = 0.1):
	print(port)
	
	devId =	fxOpen(port, baudRate)
	print(devId)
	fxStartStreaming(devId, frequency = 100, shouldLog = True)
    
	for i in range(int(time/time_step)):
		exoState = fxReadDevice(devId)
		print('accelx: ', exoState.accelx, ', accely: ', exoState.accely, ' accelz: ', exoState.accelz)
		print('gyrox: ', exoState.gyrox, ', gyroy: ', exoState.gyroy, ' gyroz: ', exoState.gyroz)
		print('motor position: ', exoState.encoderAngle, ', motor velocity: ', exoState.encoderVelocity)
		print('battery current: ', exoState.batteryCurrent, ' , battery voltage: ', exoState.batteryVoltage, ' , battery temperature: ', exoState.batteryTemp)
		sys.stdout.flush()
		sleep(time_step)
		
	return True

if __name__ == '__main__':
	baudRate = sys.argv[1]
	ports = sys.argv[2:3]
	try:
		fxReadOnly(ports, baudRate)
	except Exception as e:
		print("broke: " + str(e))
		pass
