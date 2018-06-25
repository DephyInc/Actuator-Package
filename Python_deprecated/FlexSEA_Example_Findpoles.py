# FlexSEA_Example_Findpoles
#=-=-=-=-=-=-=-=-=-=-=-=
# This script will send a FindPoles calibration command to Ex
# Make sure that the motor can freely move before calling this
# Hit Ctrl+C to exit
# 2018/02/21, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched

# User setup:
COM = comPortFromFile()
refreshRate = 0.005   # seconds, communication & FSM
displayDiv = 5       # We refresh the display every 50th packet

# "Main":
print('\nExample Code - Send Findpoles() to Ex')
print('=======================================\n')

# Open serial port:
hser = serial.Serial(COM)
print('Opened', hser.portstr)

# pyFlexSEA:
print('Initializing FlexSEA stack...')
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass com handle to pyFlexSEA
sleep(0.1)

# Main while() loop:
#===================

#Disable FSM2 (doing it twice to be sure):
print('Disabling FSM2...')
actPackFSM2(0)
sleep(0.1)
actPackFSM2(0)
sleep(0.1)

#Send calibration command
print('Finding poles...')
findPoles(1)
