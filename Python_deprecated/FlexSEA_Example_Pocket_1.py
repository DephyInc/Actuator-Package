# FlexSEA_Example_Pocket_1
#=-=-=-=-=-=-=-=-=-=-=-=-=
# Major sensors will be displayed on the terminal.
# Right motor toggles between two speeds
# Left motor toggles between two positions
# Hit Ctrl+C to exit
# 2018/03/15, Dephy, Inc.

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

# position controller gains:
pos_KP = 800 		# proportional gain
pos_KI = 5 		# integral gain
deltaPos = 300		# Position difference

# This is called by the timer:
def timerEvent():
	# Read data & display it:
	i = readPocket(0, 2, displayDiv)
	if i == 0:
		print('\nFSM State =', state)
	# Call state machine:
	stateMachineDemo1()
	flexSEAScheduler.enter(refreshRate, 1, timerEvent) # adds itself back onto schedule

# State machine
state = 'init'
fsmLoopCounter = 0
stateTime = 400
hold_position_a = 0
hold_position_b = 0

def stateMachineDemo1():

	global state
	global fsmLoopCounter
	global hold_position_a
	global hold_position_b
	
	if state == 'init':
		
		#Skip a few cycles to make sure we are receiving replies
		
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > 2):
			fsmLoopCounter = 0
			state = 'setController'

	elif state == 'setController':
		# Set Control mode to Position
		print('Setting controllers: Right = Open, Left = Position...')
		setControlMode(CTRL_OPEN, RIGHT)
		setControlMode(CTRL_POSITION, LEFT)
		setZGains(pos_KP, pos_KI, 0, 0, LEFT)
		hold_position_a = myPocket.ex[LEFT].enc_ang[0]
		hold_position_b = hold_position_a + deltaPos
		setPosition(hold_position_a, LEFT) # Start where we are
		
		# Transition:
		state = 'hold_a'

	elif state == 'hold_a':
		#CW, Position A
		setMotorVoltage(200, RIGHT)
		setPosition(hold_position_b, LEFT)
	
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'hold_b'
			fsmLoopCounter = 0

	elif state == 'hold_b':
		#CCW, Position B
		setMotorVoltage(-200, RIGHT)
		setPosition(hold_position_a, LEFT)
	
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
	

