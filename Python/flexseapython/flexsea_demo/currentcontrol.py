import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from fxUtil import *
from .streamManager import StreamManager

labels = ["State time", 		\
"Motor angle", "Motor current",	\
"Battery voltage", "Battery current" \
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ENC_ANG,								\
	FX_MOT_CURR,								\
	FX_BATT_VOLT, FX_BATT_CURR \
]

def fxCurrentControl(devId, holdCurrent = [1000], time = 4, time_step = 0.1):
	stream = StreamManager(devId,printingRate = 2,labels=labels, varsToStream = varsToStream)
	result = True
	print('Setting controller to current...')
	setControlMode(devId, CTRL_CURRENT)
	setZGains(devId, 50, 32, 0, 0)
	prevCurrent = holdCurrent[0]
	num_time_steps = int(time/time_step)
	for current in holdCurrent:
		for i in range(num_time_steps):
			desCurrent = int((current-prevCurrent) * (i / float(num_time_steps)) + prevCurrent)
			setMotorCurrent(devId, desCurrent) # Start the current, holdCurrent is in mA
			sleep(time_step)
			preamble = "Holding Current: {} mA...".format(desCurrent)
			stream()
			stream.printData(message=preamble)
			measuredCurrent = stream([FX_MOT_CURR])[0]
			result ^= (abs(measuredCurrent - desCurrent) <= 0.2 * desCurrent) 
		prevCurrent = current

	print('Turning off current control...')
	# ramp down first
	n = 50
	for i in range(0, n):
		setMotorCurrent(devId, prevCurrent * (n-i)/n)
		sleep(0.04)

	# wait for motor to spin down

	setMotorCurrent(devId, 0)
	lastAngle = stream([FX_ENC_ANG])[0]
	sleep(0.2)
	currentAngle = stream([FX_ENC_ANG])[0]
	while( abs(currentAngle - lastAngle) > 100):
		lastAngle = currentAngle
		sleep(0.2)
		currentAngle = stream([FX_ENC_ANG])[0]

	setControlMode(devId, CTRL_NONE)
	del stream
	return result
if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxCurrentControl(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
