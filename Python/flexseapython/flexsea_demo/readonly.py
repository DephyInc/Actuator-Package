import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.fxUtil import *

def printActPack(devId):
	exoState = fxReadDevice(devId)
	print('accelx: ', exoState.accelx, ', accely: ', exoState.accely, ' accelz: ', exoState.accelz)
	print('gyrox: ', exoState.gyrox, ', gyroy: ', exoState.gyroy, ' gyroz: ', exoState.gyroz)
	print('motor position: ', exoState.encoderAngle, ', motor velocity: ', exoState.encoderVelocity)
	print('battery current: ', exoState.batteryCurrent, ' , battery voltage: ', exoState.batteryVoltage, ' , battery temperature: ', exoState.batteryTemp)


def printNetMaster(devId):
	netMasterState = fxReadNetMasterDevice(devId)
	print('NetNode0 - accelx: ', netMasterState.netNode[0].accelx, ', accely: ', netMasterState.netNode[0].accely, ' accelz: ', netMasterState.netNode[0].accelz)
	print('NetNode0 - gyrox: ', netMasterState.netNode[0].gyrox, ', gyroy: ', netMasterState.netNode[0].gyroy, ' gyroz: ', netMasterState.netNode[0].gyroz)
	print('NetNode1 - accelx: ', netMasterState.netNode[1].accelx, ', accely: ', netMasterState.netNode[1].accely, ' accelz: ', netMasterState.netNode[1].accelz)
	print('NetNode1 - gyrox: ', netMasterState.netNode[1].gyrox, ', gyroy: ', netMasterState.netNode[1].gyroy, ' gyroz: ', netMasterState.netNode[1].gyroz)
	print('NetNode2 - accelx: ', netMasterState.netNode[2].accelx, ', accely: ', netMasterState.netNode[2].accely, ' accelz: ', netMasterState.netNode[2].accelz)
	print('NetNode2 - gyrox: ', netMasterState.netNode[2].gyrox, ', gyroy: ', netMasterState.netNode[2].gyroy, ' gyroz: ', netMasterState.netNode[2].gyroz)
	print('NetNode3 - accelx: ', netMasterState.netNode[3].accelx, ', accely: ', netMasterState.netNode[3].accely, ' accelz: ', netMasterState.netNode[3].accelz)
	print('NetNode3 - gyrox: ', netMasterState.netNode[3].gyrox, ', gyroy: ', netMasterState.netNode[3].gyroy, ' gyroz: ', netMasterState.netNode[3].gyroz)
	print('NetNode4 - accelx: ', netMasterState.netNode[4].accelx, ', accely: ', netMasterState.netNode[4].accely, ' accelz: ', netMasterState.netNode[4].accelz)
	print('NetNode4 - gyrox: ', netMasterState.netNode[4].gyrox, ', gyroy: ', netMasterState.netNode[4].gyroy, ' gyroz: ', netMasterState.netNode[4].gyroz)
	print('NetNode5 - accelx: ', netMasterState.netNode[5].accelx, ', accely: ', netMasterState.netNode[5].accely, ' accelz: ', netMasterState.netNode[5].accelz)
	print('NetNode5 - gyrox: ', netMasterState.netNode[5].gyrox, ', gyroy: ', netMasterState.netNode[5].gyroy, ' gyroz: ', netMasterState.netNode[5].gyroz)
	print('NetNode6 - accelx: ', netMasterState.netNode[6].accelx, ', accely: ', netMasterState.netNode[6].accely, ' accelz: ', netMasterState.netNode[6].accelz)
	print('NetNode6 - gyrox: ', netMasterState.netNode[6].gyrox, ', gyroy: ', netMasterState.netNode[6].gyroy, ' gyroz: ', netMasterState.netNode[6].gyroz)
	print('NetNode7 - accelx: ', netMasterState.netNode[7].accelx, ', accely: ', netMasterState.netNode[7].accely, ' accelz: ', netMasterState.netNode[7].accelz)
	print('NetNode7 - gyrox: ', netMasterState.netNode[7].gyrox, ', gyroy: ', netMasterState.netNode[7].gyroy, ' gyroz: ', netMasterState.netNode[7].gyroz)
	

def fxReadOnly(port, baudRate, time = 6,time_step = 0.1):
	print(port)
	
	devId =	fxOpen(port, baudRate)
	print(devId)
	fxStartStreaming(devId, frequency = 100, shouldLog = True)

	appType = fxGetAppType(devId)

	for i in range(int(time/time_step)):
		if (appType == FxActPack):
			printActPack(devId)
		elif (appType == FxNetMaster):
			printNetMaster(devId)
		else:
			raise RuntimeError('Unsupported application type: ', appType)
			return False

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
