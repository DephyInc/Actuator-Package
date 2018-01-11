#FlexSEA_Demo_5: Adding a Timer Thread
#Stream Rigid Data

import serial
from time import sleep
from pyFlexSEA import *
import os
from pyFlexSEA_commTimer import *

def timerEventReadRigid():
	os.system('cls') #Clear terminal
	print('\nPython + DLL Rigid Stream Demo\n')
	readRigid()

#"Main":
print('\nDemo code #5 - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

#Open serial port:
hser = serial.Serial('COM5')
print('Opened', hser.portstr)

#Background: read Rigid at 100Hz:
t = commTimer(0.01, timerEventReadRigid)
t.start()

#pyFlexSEA:
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass handle to pyFlexSEA

#Demo code - Multiple Read, Rigid:
#===============================

try:
	while True:
		#Nothing to do...
		sleep(0.01)
except KeyboardInterrupt:
	pass

#Closing:
t.cancel()
sleep(0.5)
hser.close
print('\nDone.\n')
