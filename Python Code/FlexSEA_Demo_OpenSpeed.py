# FlexSEA_Demo_OpenSpeed
#=-=-=-=-=-=-=-=-=-=-=-=
# Motor will ramp up, spin, then ramp down. Forever.
# Major sensors will be displayed on the terminal.
# Hit Ctrl+C to exit
# 2017/10/03, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched # python task scheduler library

# User setup:
#COM = '/dev/ttyACM1' # for Linux/Raspbian
COM = 'COM3' # for windows
refreshRate = 0.01   # seconds, communication & FSM
displayDiv = 5       # we refresh the display every 5th packet
flexSEAScheduler = sched.scheduler(perf_counter, sleep) # global scheduler

# This is called by the timer:
def timerEvent():
	# Read data & display it:
	i = readActPack(0, 2, displayDiv)
	if i == 0:
		print('\nFSM State =', state)
	# Call state machine:
	stateMachineDemo1()
	flexSEAScheduler.enter(refreshRate, 1, timerEvent) # adds itself back onto schedule, with priority 1

# State machine
state = 'init'
fsmLoopCounter = 0
stateTime = 200
gain = 15
deadBand = 350 # Peak Motor voltage = gain*stateTime + deadBand (3350mV in this case)

def stateMachineDemo1():

	global state
	global fsmLoopCounter
	
	if state == 'init':
		
		# Set Control mode to Open
		print('Setting controller to Open...')
		setControlMode(CTRL_OPEN)
		setMotorVoltage(0)
		
		# Transition:
		fsmLoopCounter = 0
		state = 'hold'
		
	elif state == 'hold':
		
		# Setpoint = 0mV
		setMotorVoltage(0)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'rampUp'
			fsmLoopCounter = 0
		
	elif state == 'rampUp':
		
		# Setpoint ramps up from 0 to stateTime
		setMotorVoltage(deadBand + gain*fsmLoopCounter)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'plateau'
			fsmLoopCounter = 0
		
	elif state == 'plateau':
		
		# Plateau at constant speed
		setMotorVoltage(deadBand + gain*stateTime)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'rampDown'
			fsmLoopCounter = 0
		
	elif state == 'rampDown':
		
		# Setpoint ramps up from 0 to stateTime
		setMotorVoltage(gain*stateTime + deadBand - gain*fsmLoopCounter)
		
		# Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'hold'
			fsmLoopCounter = 0
		
	else:
		
		# Invalid state - stay here and complain
		print('Invalid FSM1 state!')
		state = 'Invalid'

# Housekeeping before we quit:
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
setPyFlexSEASerialPort(hser) # pass com handle to pyFlexSEA
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
	

