# FlexSEA_Example_UserRW
#=-=-=-=-=-=-=-=-=-=-=-=
# Demonstration of the User R/W feature
# Major sensors will be displayed on the terminal.
# Hit Ctrl+C to exit
# 2018/05/29, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched

# User setup:
COM = comPortFromFile()
refreshRate = 0.005		# seconds, communication & FSM
displayDiv = 5			# We refresh the display every 50th packet
flexSEAScheduler = sched.scheduler(perf_counter, sleep)

# This is called by the timer:
def timerEvent():
	global myUserRW
	# Read data & display it:
	#i = readActPack(0, 2, displayDiv)
	i = 0
	if i == 0:
		#print('\nFSM State =', state)
		print('User Read[0] =', myUserRW.r[0])
	# Call state machine:
	stateMachineDemo1()
	flexSEAScheduler.enter(refreshRate, 1, timerEvent) # adds itself back onto schedule

# State machine
state = 'init'
fsmLoopCounter = 0
stateTime = 300

def stateMachineDemo1():

	global state
	global fsmLoopCounter
	
	if state == 'init':
		
		#Skip a few cycles to make sure we are receiving replies
		
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > 2):
			fsmLoopCounter = 0
			state = 'writeVal'

	elif state == 'writeVal':
		# Write an incrementing value

		fsmLoopCounter += 1
		if(fsmLoopCounter > 100):
			fsmLoopCounter = 0
			# Transition:
			state = 'readVal'
		
		writeUser(0,fsmLoopCounter)
		writeUser(1,10)
		writeUser(2,20)
		writeUser(3,30)
		
	elif state == 'readVal':
		# Read user values

		fsmLoopCounter += 1
		if(fsmLoopCounter > 10):
			fsmLoopCounter = 0
			# Transition:
			state = 'writeVal'
		
		readUser()

	else:
		# Invalid state - stay here and complain
		print('Invalid FSM state!')
		state = 'Invalid'

# Housekeeping before we quit:
def beforeExiting():
	print('closing com')
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
setPyFlexSEASerialPort(hser) #Pass com handle to pyFlexSEA
sleep(0.1)

# Background: read Rigid and call FSM at 100Hz:
print('Starting the background comm...')

# Main while() loop:
#===================
try:
	while True:
		flexSEAScheduler.enter(refreshRate, 1, timerEvent)
		flexSEAScheduler.run()
		sleep(60*60*24) # arbitrary sleep time
except (KeyboardInterrupt, SystemExit):
	beforeExiting()
	sys.exit()
	

