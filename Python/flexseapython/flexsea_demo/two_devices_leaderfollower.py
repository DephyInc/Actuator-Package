import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)
from pyFlexsea import *
from pyFlexsea_def import *
from fxUtil import *
from .streamManager import Stream

labels = ["State time", 				\
	"Accel X",	"Accel Y",	"Accel Z",	\
	"Gyro X", 	"Gyro Y", 	"Gyro Z",	\
	"Motor angle", "Motor voltage", "Motor current",	\
	"Battery voltage", "Battery current"				\
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,								\
	FX_MOT_VOLT, FX_MOT_CURR,				\
	FX_BATT_VOLT, FX_BATT_CURR 				\
]

def fxLeaderFollower(leaderPort, followerPort):
	
	leadStream = Stream(leaderPort, printingRate =2, labels=labels, varsToStream=varsToStream)
	followerStream = Stream(followerPort, printingRate =2, labels=labels, varsToStream=varsToStream)

	# Concatenates angles of both stream together
	initialAngles = leadStream([FX_ENC_ANG]) + followerStream([FX_ENC_ANG])
	timeout = 10
	timeoutCount = 0

	while(None in initialAngles):
		timeoutCount = timeoutCount + 1
		if(timeoutCount > timeout):
			raise Exception("Timed out trying to read data")
		else:
			sleep(0.5)
			# Concatenates angles of both stream together
			a = leadStream([FX_ENC_ANG])
			b = followerStream([FX_ENC_ANG])
			initialAngles = a + b

	# set first device to current controller with 0 current (0 torque)
	setControlMode(leadStream.devId, CTRL_CURRENT)
	setGains(leadStream.devId, 100, 20, 0, 0)
	setMotorCurrent(leadStream.devId, 0) # Start the current, holdCurrent is in mA 

	# set position controller for second device
	setPosition(followerStream.devId, initialAngles[1])
	setControlMode(followerStream.devId, CTRL_POSITION)
	setPosition(followerStream.devId, initialAngles[1])
	setGains(followerStream.devId, 50, 3, 0, 0)

	count = 0
	try:
		while(True):
			sleep(0.05)
			angle0 = leadStream([FX_ENC_ANG])[0]
			if(angle0 != None):
				diff0 = angle0 - initialAngles[0]
				setPosition(followerStream.devId, initialAngles[1] + 3*diff0)
			
			preamble = "device {} following device {}".format(followerStream.devId, leadStream.devId)
			followerStream()
			leadStream()
			followerStream.printData(message = preamble)
			leadStream.printData(clear_terminal = False)

	except:
		print("Unexpected error:", sys.exc_info()[0])

	print('Turning off position control...')
	setControlMode(leadStream.devId, CTRL_NONE)
	setControlMode(followerStream.devId, CTRL_NONE)

	# sleep so that the commmand makes it through before we stop streaming
	sleep(0.2)
	del followerStream
	sleep(0.2)
	del leadStream

if __name__ == '__main__':
	ports = sys.argv[1:3]
	try:
		fxLeaderFollower(ports[0], ports[1])
	except Exception as e:
		print("broke: " + str(e))
		pass
