import os, sys
from time import sleep

pardir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pardir)
from flexseapython.fxUtil import *
from .streamManager import StreamManager

labels = ["State time", 	\
		"Accel X", 	"Accel Y", 	"Accel Z", 	\
		"Gyro X", 	"Gyro Y",	"Gyro Z", 	\
		"Motor angle", "Joint angle",		\
		"Motor voltage", "Motor current",	\
		"Battery voltage", "Battery current", \
		"genVar[0]", "genVar[1]", "genVar[2]", \
		"genVar[3]", "genVar[4]", "genVar[5]", \
		"genVar[6]", "genVar[7]", "genVar[8]", \
		"genVar[9]"
]

varsToStream = [ 		\
	FX_STATETIME, 		\
	FX_ACCELX,	FX_ACCELY,	FX_ACCELZ, 	\
	FX_GYROX,  	FX_GYROY,  	FX_GYROZ,	\
	FX_ENC_ANG,	FX_ANKLE_ANG,	\
	FX_MOT_VOLT, FX_MOT_CURR,	\
	FX_BATT_VOLT, FX_BATT_CURR, \
	FX_GEN_VAR_0, FX_GEN_VAR_1, FX_GEN_VAR_2, \
	FX_GEN_VAR_3, FX_GEN_VAR_4, FX_GEN_VAR_5, \
	FX_GEN_VAR_6, FX_GEN_VAR_7, FX_GEN_VAR_8, \
	FX_GEN_VAR_9
]

def fxReadOnly(devId, time = 6,time_step = 0.1):
	stream = StreamManager(devId,printingRate = 4,labels=labels,varsToStream = varsToStream,updateFreq = 100)
	#stream.InitCSV("readall.csv")

	for i in range(int(time/time_step)):
		sleep(time_step)
		stream()
		#stream.writeToCSV()
		stream.printData()

	del stream
	return True

if __name__ == '__main__':
	ports = sys.argv[1:2]
	devId = loadAndGetDevice(ports)[0]
	try:
		fxReadOnly(devId)	
	except Exception as e:
		print("broke: " + str(e))
		pass
