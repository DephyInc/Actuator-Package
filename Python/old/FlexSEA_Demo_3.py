#FlexSEA_Demo_3: importing FlexSEA libs from other module.
#Same demo as script #2: simple Rigid Read

import serial
from time import sleep
from pyFlexSEA import *

#"Main":
print('\nDemo code #3 - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

#Open serial port:
hser = serial.Serial('COM5')
print('Opened', hser.portstr)

#pyFlexSEA:
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass handle to pyFlexSEA

#Demo code - Single Read, Rigid:
#===============================
demo2()

#Closing:
sleep(0.1)
print('\nDone.\n')
hser.close
