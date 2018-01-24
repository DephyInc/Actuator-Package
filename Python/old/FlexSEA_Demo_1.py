import ctypes
from ctypes import *
from ctypes import cdll
import serial
from time import sleep

#Constants:
FLEXSEA_PLAN_1 = 10
FLEXSEA_MANAGE_1 = 20
FLEXSEA_EXECUTE_1 = 40
COMMSTR_LEN = 48
CTRL_NONE = 0
CTRL_OPEN = 1

#Variables used to send packets:
nb = c_ushort(0)
packetIndex = c_ushort(0)
arrLen = c_ubyte(10)
commStr = (c_ubyte * COMMSTR_LEN)()

#Set Control Mode:
def setControlMode(ctrlMode):
	flexsea.ptx_cmd_ctrl_mode_w(FLEXSEA_EXECUTE_1, byref(nb), commStr, ctrlMode);
	ser.write(commStr)

#Set Motor Voltage:
def setMotorVoltage(mV):
	flexsea.ptx_cmd_ctrl_o_w(FLEXSEA_EXECUTE_1, byref(nb), commStr, mV);
	ser.write(commStr)

#"Main":
print('\nDemo code - Python project with FlexSEA-Stack DLL')
print('==================================================\n')
flexsea = cdll.LoadLibrary('lib/FlexSEA-Stack-Plan.dll')

#Init stack:
flexsea.initFlexSEAStack_minimalist(FLEXSEA_PLAN_1);

#Open serial port:
ser = serial.Serial('COM5')
print('Opened', ser.portstr, '\n')

#Demo code - open speed ramp:
#============================
motVolt = int(input("What peak voltage (mV) do you want? "))
setControlMode(CTRL_OPEN)
sleep(0.1)
minSpeed = 500
delay = 0.0015
#Up
for i in range(minSpeed, motVolt):
	setMotorVoltage(i)
	sleep(delay)
#Down
for i in range(minSpeed, motVolt):
	setMotorVoltage(motVolt-i+minSpeed)
	sleep(delay)
setMotorVoltage(0)

#Closing:
sleep(0.1)
setControlMode(CTRL_NONE)
sleep(0.1)
print('\nDone.\n')
ser.close
