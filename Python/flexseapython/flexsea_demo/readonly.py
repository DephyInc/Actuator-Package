import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.fxUtil import *

def fxReadOnly(port, baudRate, time = 6,time_step = 0.1):
	print(port)
	
	devId =	fxOpen(port, baudRate)
	print(devId)
	fxStartStreaming(devId, True)
    
	for i in range(int(time/time_step)):
		exoState = fxReadDevice(devId)
		print('accelx: ', exoState._manage._imu._accelx, ', accely: ', exoState._manage._imu._accely, ' accelz: ', exoState._manage._imu._accelz)
		print('gyrox: ', exoState._manage._imu._gyrox, ', gyroy: ', exoState._manage._imu._gyroy, ' gyroz: ', exoState._manage._imu._gyroz)
		print('motor position: ', exoState._execute._motor_data._motor_angle)
		print('battery current: ', exoState._regulate._battery._battery_current, ' , battery current: ', exoState._regulate._battery._battery_current, ' , battery temperature: ', exoState._regulate._battery._battery_temperature)
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
