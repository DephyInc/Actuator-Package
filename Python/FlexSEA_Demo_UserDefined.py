# FlexSEA_Demo_UserDefined
#=-=-=-=-=-=-=-=-=-=-=-=
# User can write their own code to be executed each cycle
# Major sensors will still be displayed in the terminal.
# Hit Ctrl+C to exit
# 2017/10/13, Dephy, Inc.

import serial
from time import perf_counter, sleep
from pyFlexSEA import *
import os
import sys
import sched # python task scheduler library

# User setup:
#COM = '/dev/ttyACM0' for linux / raspberry pi use
COM = 'COM3'
refreshRate = 0.005   # seconds, communication & FSM
displayDiv = 50       # We refresh the display every 50th packet
flexSEAScheduler = sched.scheduler(perf_counter, sleep) # global scheduler

# This is called by the timer:
def timerEvent():
	# Read data & display it:
	i = readActPack(0, 2, displayDiv)
	if i == 0:
		print('\nFSM State =', state)
	# Call state machine:
	MAIN_LOOP_FUNCTION()
	flexSEAScheduler.enter(refreshRate, 1, MAIN_LOOP_FUNCTION) # adds itself back onto schedule, with priority 1

#########################################################################################
#################### USER DEFINED PERSISTENT VARIABLES GO HERE ##########################

# global values:
# any variable you want to persist across loop iterations
# should be defined with the keyword 'global' inside a function, 
# and initialized outside of any functions
loop_counter = 0
top_speed = 0
max_accel_x = 0
min_accel_x = 0
was_motor_angel_equal_to_tau = False
tau = 6283185 #6.283185

############################ USER DEFINED CODE GOES HERE ################################
def MAIN_LOOP_FUNCTION(): # function called once every cycle
	# change and modify the code in here as you please
	global loop_counter
	global top_speed
	global max_accel_x
	global min_accel_x
	global was_motor_angel_equal_to_tau

	i = readActPack(0, 2, displayDiv)

	setControlMode(CTRL_OPEN)
	setMotorVoltage(0)
	
	if myRigid.ex.enc_ang[0] == tau:
		was_motor_angel_equal_to_tau = True

	if myRigid.mn.accel.x > max_accel_x:
		max_accel_x = myRigid.mn.accel.x

	if myRigid.mn.accel.x < min_accel_x:
		min_accel_x = myRigid.mn.accel.x

	if myRigid.ex.enc_ang_vel[0] > top_speed:
		top_speed = myRigid.ex.enc_ang_vel[0]

	for i in range(1000):
		wastingTime = i + 5 # do some random calculations
		wastingTime2 = i**2 - 6

	loop_counter += 1
	# end main function
	flexSEAScheduler.enter(refreshRate, 1, MAIN_LOOP_FUNCTION) # add itself back onto scheduler

def EXITING(): # function called once when exiting script
	print("top_speed :", top_speed)
	print("max_accel_x :", max_accel_x)
	print("min_accel_x", min_accel_x)
	print("did motor angle equal tau? ", was_motor_angel_equal_to_tau)

########################### DON'T CHANGE CODE BELOW THIS LINE ###########################
#########################################################################################

# Housekeeping before we quit:
def beforeExiting():
	EXITING()
	print('closing com')
	setControlMode(0)
	sleep(0.5)
	hser.close()
	sleep(0.5)
	print('\n\nDone.\n')

print('\nDemo code - Python project with FlexSEA-Stack DLL')
print('====================================================\n')

# Open serial port:
hser = serial.Serial(COM)
print('Opened', hser.portstr)

print('Initializing FlexSEA stack...')
initPyFlexSEA()
setPyFlexSEASerialPort(hser) #Pass com handle to pyFlexSEA
sleep(0.1)

# Background: read Rigid and call FSM at 100Hz:
print('Starting the background comm...')
sleep(0.1)

# Main while() loop:
#===================
try:
	while True:
		flexSEAScheduler.enter(refreshRate, 1, MAIN_LOOP_FUNCTION)
		flexSEAScheduler.run()
		sleep(60*60*24) # arbitrary sleep time
except (KeyboardInterrupt, SystemExit):
	beforeExiting()
	sys.exit()
