# FlexSEA_Demo_CurrentControl
#=-=-=-=-=-=-=-=-=-=-=-=
# Motor will attempt to maintain the same current draw.
# Initial settings for current control should cause the motor to turn slowly
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
I_KP = 20
I_KI = 1

# controller gains:
##Z_K = 0
##Z_B = 0

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
holdCurrent = 1000
def stateMachineDemo1():

	global state
	global holdCurrent
	
	if state == 'init':
		# Set Control mode to Open
		print('Setting controller to Open...')
		setControlMode(CTRL_CURRENT)
		##setZGains(Z_K, Z_B, I_KP, I_KI)
		setZGains(I_KP, I_KI, 0, 0)
		##holdPosition = myRigid.ex.enc_ang[0]
		setMotorCurrent(holdCurrent) # Start the current 
		
		# Transition:
		state = 'hold'

	elif state == 'hold':
		pass # just chill in this state

		##setMotorCurrent(holdCurrent)

	else:
		# Invalid state - stay here and complain
		print('Invalid FSM state!')
		state = 'Invalid'

# Housekeeping before we quit:
def beforeExiting():
	print('closing com')
	setMotorCurrent(0)
	readActPack(0, 2, displayDiv) ## call once more to pass settings to flexSEA
	sleep(1)
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
	

