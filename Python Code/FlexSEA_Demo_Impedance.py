# FlexSEA_Demo_Impedance
#=-=-=-=-=-=-=-=-=-=-=-=
# Motor will toggle between two equilibrium positions. Forever.
# Major sensors will be displayed on the terminal.
# Hit Ctrl+C to exit
# 2017/10/02, Dephy, Inc.

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

deltaPos = 10000
# Current gains:
I_KP = 100
I_KI = 1

# Impedance gains (2 sets):
Z_K_a = 3
Z_B_a = 0
Z_K_b = 5
Z_B_b = 0

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
stateTime = 200
ePos1 = 0
ePos2 = 0
toggle = 0
def stateMachineDemo1():

	global state
	global fsmLoopCounter
	global ePos1
	global ePos2
	global toggle
	
	if state == 'init':
		
		# Set Control mode to Open
		print('Setting controller to Open...')
		setControlMode(CTRL_IMPEDANCE)
		setZGains(Z_K_a, Z_B_a, I_KP, I_KI)
		ePos1 = myRigid.ex.enc_ang[0]
		ePos2 = ePos1 + deltaPos
		setPosition(ePos1) # Start where we are
		
		# Transition:
		fsmLoopCounter = 0
		state = 'pos1'
		
	elif state == 'pos1':
		
		# Equilibrium position #1
		setPosition(ePos1)
		
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'pos2'
			fsmLoopCounter = 0
		
	elif state == 'pos2':
		
		# Equilibrium position #2
		setPosition(ePos2)
		
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'changeGains'
			fsmLoopCounter = 0
		
	elif state == 'changeGains':
		
		# New gains:
		if(toggle == 0):
			toggle = 1
			setZGains(Z_K_b, Z_B_b, I_KP, I_KI)
		else:
			toggle = 0
			setZGains(Z_K_a, Z_B_a, I_KP, I_KI)
		setPosition(ePos2)
		
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > 10):
			state = 'pos1'
			fsmLoopCounter = 0
		
	else:
		
		# Invalid state - stay here and complain
		print('Invalid FSM1 state!')
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
	

