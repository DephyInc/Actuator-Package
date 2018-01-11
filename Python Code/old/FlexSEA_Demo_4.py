#FlexSEA_Demo_4: importing FlexSEA libs from other module.
#Stream Rigid Data

import serial
from time import sleep
from pyFlexSEA import *
import os

#"Main":
print('\nDemo code #4 - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

#Open serial port:
hser = serial.Serial('COM5')
print('Opened', hser.portstr)

#pyFlexSEA:
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass handle to pyFlexSEA

#Demo code - Multiple Read, Rigid:
#===============================

try:
	while True:
		os.system('cls') #Clear terminal
		print('\nPython + DLL Rigid Stream Demo\n')
		readRigid()
		sleep(0.025)
except KeyboardInterrupt:
	pass

#Closing:
sleep(0.1)
print('\nDone.\n')
hser.close
