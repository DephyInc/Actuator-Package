#FlexSEA_Demo_6: Using the new ActPack command
#Stream Rigid Data, Control motor in Open mode

import serial
from time import sleep
from pyFlexSEA import *
import os
from pyFlexSEA_commTimer import *

def timerEventReadActPack():
	readActPack(10) #Prints every 10th call

#"Main":
print('\nDemo code #6 - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

#Open serial port:
hser = serial.Serial('COM5')
print('Opened', hser.portstr)

#pyFlexSEA:
print('Initializing FlexSEA stack...')
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass handle to pyFlexSEA
sleep(0.1)

#Background: read Rigid at 100Hz:
print('Starting the background comm...')
t = commTimer(0.01, timerEventReadActPack)
t.start()
sleep(0.1)

print('Setting controller to Open...')
setControlMode(CTRL_OPEN)
setMotorVoltage(0)
sleep(0.1)

#Demo code - Multiple Read, Rigid:
#===============================

try:
	while True:
		setMotorVoltage(0)
		sleep(3)
		setMotorVoltage(1000)
		sleep(3)
except KeyboardInterrupt:
	pass

#Closing:
t.cancel()
sleep(0.5)
hser.close
print('\nDone.\n')
