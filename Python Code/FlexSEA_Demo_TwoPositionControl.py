# FlexSEA_Demo_PositionControl
#=-=-=-=-=-=-=-=-=-=-=-=
# Motor will switch between holding the starting position and another position.
# Major sensors will be displayed on the terminal.
# Hit Ctrl+C to exit
# 2018/01/10, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched

# User setup:
# COM = '/dev/ttyACM0' # for Linux/Raspbian
COM = 'COM3' # for windows
refreshRate = 0.005   # seconds, communication & FSM
displayDiv = 5       # We refresh the display every 50th packet
flexSEAScheduler = sched.scheduler(perf_counter, sleep)

# Current gains:
I_KP = 100
I_KI = 1

# position controller gains:
pos_KP = 20 # proportional gain
pos_KI = 6 # integral gain

# This is called by the timer:
def timerEvent():
	# Read data & display it:
	i = readActPack(0, 2, displayDiv)
	if i == 0:
		print('\nFSM State =', state)
	# Call state machine:
	stateMachineDemo1()
	flexSEAScheduler.enter(refreshRate, 1, timerEvent) # adds itself back onto schedule

# State machine
state = 'init'
fsmLoopCounter = 0
stateTime = 300
hold_position_a = 0
hold_position_b = 6000
def stateMachineDemo1():

	global state
	global fsmLoopCounter
	global hold_position_a
	global hold_position_b
	
	if state == 'init':
		# Set Control mode to Open
		print('Setting controller to Open...')
		setControlMode(CTRL_POSITION)
		setZGains(pos_KP, pos_KI, I_KP, I_KI)
		hold_position_a = myRigid.ex.enc_ang[0]
		setPosition(hold_position_a) # Start where we are
		
		# Transition:
		state = 'hold_a'

	elif state == 'hold_a':
		# Equilibrium position
		setPosition(hold_position_a)
	
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'hold_b'
			fsmLoopCounter = 0

	elif state == 'hold_b':
		setPosition(hold_position_b)
	
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'hold_a'
			fsmLoopCounter = 0

	else:
		# Invalid state - stay here and complain
		print('Invalid FSM state!')
		state = 'Invalid'

# Housekeeping before we quit:
def beforeExiting():
	print('closing com')
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
	

