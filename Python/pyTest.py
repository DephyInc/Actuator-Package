from pyFlexsea import *
from pyFlexsea_def import *
import platform
from time import sleep
import math

def main():

	loadSuccess = loadFlexsea()
	if(not loadSuccess):
		print("Load failed... quitting")

	print("Connecting")

	fxOpen(b"COM3", 0)
	
	waited = 0
	while(not fxIsOpen(0) and waited < 5):
		print("Waiting for port to be open")
		waited = waited+1
		sleep(0.1)

	if(not fxIsOpen(0)):
		print("Couldn't connect...")
		sys.exit(1)
	
	devId = fxGetDeviceIds()[0]
	while(devId == -1):
		sleep(0.1)
		devId = fxGetDeviceIds()[0]
	
	print("Got device with id: " + str(devId))
	
	try:

		fxSetStreamVariables(devId, [1,2,3,4,5])
		fxStartStreaming(devId, 100, False, 1)
		
		# for i in range(0,10):
		# 	sleep(0.1)
		# 	data = fxReadDevice(devId,[1,2,3,4,5])
		# 	print(data)

		print("Setting open control...") 
		setControlMode(devId, CTRL_OPEN)

		numSteps = 300
		numSeconds = 5
		maxVoltage = 5000
		numTimes = 2

		for time in range(0, numTimes):
			# print("Ramping up open controller...") 
			# for i in range(0, numSteps):
			# 	sleep(numSeconds / numSteps)
			# 	mV = maxVoltage * (i / numSteps)
			# 	setMotorVoltage(devId, mV)

			# print("Ramping down open controller...")
			# for i in range(0, numSteps):
			# 	sleep(numSeconds / numSteps)
			# 	mV = maxVoltage * ((numSteps - i) / numSteps)
			# 	setMotorVoltage(devId, mV)

			for i in range(0, numSteps):

					sleep(numSeconds / numSteps)
					mV = maxVoltage * math.sin ( math.pi * i / (numSteps) )
					setMotorVoltage(devId, mV)			

		fxStopStreaming(devId)
		
	except:
		print("broke")
		pass

main()