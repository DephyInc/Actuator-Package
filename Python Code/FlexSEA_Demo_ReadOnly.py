# FlexSEA_Demo_ReadOnly
#=-=-=-=-=-=-=-=-=-=-=-=
# The motor won't move.
# Major sensors will be displayed in the terminal.
# Hit Ctrl+C to exit
# 2017/10/02, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched

# User setup:
#COM = '/dev/ttyACM0' # for Linux/Raspbian
COM = 'COM3' # for windows
refreshRate = 0.004   # seconds, communication & FSM
displayDiv = 50       # we refresh the display every 50th packet
flexSEAScheduler = sched.scheduler(perf_counter, sleep) # global scheduler

# this is called by the timer:
lastTimeStamp = 0
timeStamp = perf_counter()
f = 1/refreshRate
def timerEventReadActPack():
	global lastTimeStamp
	global timeStamp
	global f
	lastTimeStamp = timeStamp
	timeStamp = perf_counter()
	i = readActPack(0, 2, displayDiv)
	f = f*0.99 + 0.01/(timeStamp-lastTimeStamp) # leaky integral refresh rate
	if i == 0:
		print('\nRefresh rate =', f)
		print("--> press 'control+c' to quit")
	flexSEAScheduler.enter(refreshRate, 1, timerEventReadActPack) # adds itself back onto schedule, with priority 1

# housekeeping before we quit:
def beforeExiting():
	print("closing com")
	setControlMode(0)
	sleep(0.5)
	hser.close()
	sleep(0.5)
	print('\nDone.\n')

# "Main":
print('\nDemo code - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

# Open serial port:
hser = serial.Serial(COM)
print('Opened', hser.portstr)

# pyFlexSEA:
print('Initializing FlexSEA stack...')
initPyFlexSEA()
setPyFlexSEASerialPort(hser) # Pass com handle to pyFlexSEA
sleep(0.1)

# Background: read Rigid at 100Hz:
print('Starting the background comm...')

# Main while() loop:
#===================
try:
	while True:
		flexSEAScheduler.enter(refreshRate, 1, timerEventReadActPack)
		flexSEAScheduler.run()
		sleep(60*60*24) # arbitrary sleep time
except (KeyboardInterrupt, SystemExit):
	beforeExiting()
	sys.exit()
	