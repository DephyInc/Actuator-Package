#FlexSEA_Demo_8: Using the new ActPack command
#Stream Rigid Data, Control motor in Open mode
#Includes a high-level State Machine

import serial
from time import sleep
from pyFlexSEA import *
import os
from pyFlexSEA_commTimer import *

#This is called by the timer:
def timerEventReadActPack():
	i = readActPack(0, 2, 5)
	if i == 0:
		print('\nFSM State =', state)

#State machine
state = 'init'
fsmLoopCounter = 0
stateTime = 3000
deadBand = 350
def stateMachineDemo1():

	global state
	global fsmLoopCounter
	
	if state == 'init':
		
		#Set Control mode to Open
		print('Setting controller to Open...')
		setControlMode(CTRL_OPEN)
		setMotorVoltage(0)
		
		#Transition:
		fsmLoopCounter = 0
		state = 'hold'
		
	elif state == 'hold':
		
		#Setpoint = 0mV
		setMotorVoltage(0)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'rampUp'
			fsmLoopCounter = 0
		
	elif state == 'rampUp':
		
		#Setpoint ramps up from 0 to stateTime
		setMotorVoltage(deadBand + fsmLoopCounter)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'plateau'
			fsmLoopCounter = 0
		
	elif state == 'plateau':
		
		#Plateau at constant speed
		setMotorVoltage(deadBand + stateTime)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'rampDown'
			fsmLoopCounter = 0
		
	elif state == 'rampDown':
		
		#Setpoint ramps up from 0 to stateTime
		setMotorVoltage(stateTime + deadBand - fsmLoopCounter)
		
		#Transition:
		fsmLoopCounter += 1
		if(fsmLoopCounter > stateTime):
			state = 'hold'
			fsmLoopCounter = 0
		
	#Sleep to slow down loop time: (~1kHz)
	sleep(0.001)

def beforeExiting():
	setControlMode(0)
	sleep(0.25)
	t.cancel()
	sleep(0.5)
	hser.close
	print('\nDone.\n')

#"Main":
print('\nDemo code #8 - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

#Open serial port:
hser = serial.Serial('COM5')
print('Opened', hser.portstr)

#pyFlexSEA:
print('Initializing FlexSEA stack...')
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass handle to pyFlexSEA
sleep(0.1)

#Background: read Rigid at 100Hz:
print('Starting the background comm...')
t = commTimer(0.01, timerEventReadActPack)
t.start()
sleep(0.1)

#Main while() loop:
#===================

try:
	while True:
		
		stateMachineDemo1()
		
except KeyboardInterrupt:
	pass

#Closing:
beforeExiting()
