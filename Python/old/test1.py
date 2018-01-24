import ctypes
from ctypes import *
from ctypes import cdll
import serial

#Constants:
FLEXSEA_PLAN_1 = 10
FLEXSEA_MANAGE_1 = 20
COMMSTR_LEN = 48

print('\nDemo code - Python project with FlexSEA-Stack DLL')
print('==================================================\n')
flexsea = cdll.LoadLibrary('lib/FlexSEA-Stack-Plan.dll')

#Init stack:
flexsea.initFlexSEAStack_minimalist(FLEXSEA_PLAN_1);

#Open serial port:
ser = serial.Serial('COM5')
print('Opened', ser.portstr)

#Generate a packet:
nb = c_ushort(0)
print('original nb:', nb.value)
packetIndex = c_ushort(0)
arrLen = c_ubyte(10)
commStr = (c_ubyte * COMMSTR_LEN)()

flexsea.ptx_cmd_tools_comm_test_w(FLEXSEA_MANAGE_1, byref(nb), commStr, 1, arrLen, packetIndex, 0);
print('nb after fct call:', nb.value)

serialData = bytearray(48)
print('commStr contains: ', end='')
for k in range(0,COMMSTR_LEN-1):
	print(commStr[k], end=',')
	serialData[k] = commStr[k]
print('...')

#ser.write(serialData)
ser.write(commStr)

#Closing:
print('\nDone.\n')
ser.close
