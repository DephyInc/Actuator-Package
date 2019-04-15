import os, sys, math
from time import sleep, time, strftime
import numpy as np

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/Actuator-Package/Python'
sys.path.append(pardir)
from flexseapython.pyFlexsea import *
from flexseapython.pyFlexsea_def import *
from flexseapython.fxUtil import *
from DataLogger import dataLogger
from time import sleep, time
# from Dephy_HelperFcns import *

labels = ["State time", 											\
"accel x", "accel y", "accel z", "gyro x", "gyro y", "gyro z", 		\
"encoder angle", "ankle angle","motor voltage","motor current"
]

varsToStream = [ 							\
	FX_STATETIME, 							\
	FX_ACCELX, FX_ACCELY, FX_ACCELZ, 		\
	FX_GYROX,  FX_GYROY,  FX_GYROZ,			\
	FX_ENC_ANG,	FX_ANKLE_ANG,				\
	FX_MOT_VOLT, FX_MOT_CURR				\
]

# New setMotorCurrent function: Sets the current setpoint for the given device (includes side)
# params:
#       devId       : the id of the device 
#       side        : the left/right side exoskeleton (KAI 10/31/2018)
#       cur         : the current to use as setpoint in milliAmps
# returns: 
#       setCurrent  : the set current with proper sign (based on left/right leg) 
def setMotorCurrent2(devId, side, cur):
    # right leg = negative current, left leg = positive current
	if side=='left':
		setCurrent = abs(int(cur))
	elif side == 'right':
		setCurrent = -abs(int(cur))
	setMotorCurrent(devId, setCurrent)
	return setCurrent

def TaughtController(devId,side):
	if side == 'left':         # coefficients for left exo motor angle v. encoder angle polynomial
		coeffs = np.array([-2.26006253984436e-10,	5.84644577910681e-06,	-0.0569851132170757,	264.927913762747,	-520650.705741319])
		slackOffset = -10	 # degrees, dorsiflexion is slack (more negative)
	elif side == 'right':      # coefficients for right exo motor angle v. encoder angle polynomial
		coeffs = np.array([2.54829306464931e-10,	-7.94082038752176e-06,	0.0929641517018376,		-467.885863600082,	803661.327037271])
		slackOffset = 25     # degrees, dorsiflexion is more slack (more positive)
	
	check_flag = 0
	# remove slack using current control before reading motor position
	while check_flag == 0:
		streamFreq = 500 # try and reduce to 200
		fxSetStreamVariables(devId, varsToStream)
		streamSuccess = fxStartStreaming(devId, streamFreq, True, 0)
		print(streamSuccess)
		print('***')
		print('Setting controller to current for ' + side + ' side...')
		setControlMode(devId, CTRL_CURRENT)
		holdCurrent = 750 
		setGains(devId, 100, 20, 0, 0)
		setCurrent = setMotorCurrent2(devId, side, holdCurrent) # Start the current, holdCurrent is in mA, setMotorCurrent2 takes in a side argument (defined above)
		print("Holding Current: {} mA...".format(setCurrent))
		
		sleep(2)
		data = fxReadDevice(devId, varsToStream)
		printData(labels, data)

		initialAngle = fxReadDevice(devId, [FX_ENC_ANG])[0]	 # get initial angle
		timeout = 100
		timeoutCount = 0
		while(initialAngle == None):
			timeoutCount = timeoutCount + 1
			if(timeoutCount > timeout):
				print("Timed out waiting for valid encoder value...")
				sys.exit(1)
			else:
				sleep(0.2) # make it mat
				fxReadDevice(devId, [FX_ENC_ANG])[0]

		##### Zeroing routine: 
		## Read current ankle encoder value 
		## Calculate desired motor encoder value from polynomial interpolation (np.polyval)
		## Compare to current motor encoder value 
		## Add zeroing offset to polynomial coefficients 
		sleep(2)
		ankleData = np.zeros((1,1))   
		motorData = np.zeros((1,1))
		## Median filter to get rid of data spiking effects
		for i in range(0,3):
			ankle = fxReadDevice(devId, [FX_ANKLE_ANG])[0]
			motor = fxReadDevice(devId, [FX_ENC_ANG])[0]
			ankleData = np.vstack((ankleData, np.array(ankle)))
			motorData = np.vstack((motorData, np.array(motor)))
		initialAngle = np.floor(np.median(ankleData)) # median of last three encoder readings
		initialMotor = np.floor(np.median(motorData)) # median of last three encoder readings
		initialMotor_des = np.floor(np.polyval(coeffs,initialAngle))  # calculate desired motor position from polynomial coefficients
		zeroing = initialMotor - initialMotor_des  # calculate difference between current motor position and desired motor position
		coeffs_zeroed = np.copy(coeffs)	
		coeffs_zeroed[4] = coeffs_zeroed[4]+zeroing   # shift coefficients to meet current motor encoder value
		initialMotor_shift = np.floor(np.polyval(coeffs_zeroed,initialAngle))     # check the interpolation worked correctly

		print('Initial Angle: ' + str(initialAngle))
		print('Initial Motor Actual: ' + str(initialMotor))
		print('Initial Motor Desired: ' + str(initialMotor_des))
		print('Offset to zero ' + side + ' side: ' + str(zeroing))
		print('Initial Motor: ' + str(initialMotor) + ', Initial Motor Desired (shifted): ' + str(initialMotor_shift))
		check = input("Is this correct? ")

		### If check is correct, proceed to Position Control
		if check == 'y':
			check_flag = 1
			sleep(2)		
			# begin Position control
			motorData = np.zeros((1,1))
			## Median filter to get rid of data spiking effects
			for i in range(0,3):
				motor = fxReadDevice(devId, [FX_ENC_ANG])[0]
				motorData = np.vstack((motorData, np.array(motor)))
			initialMotor = np.median(motorData)
			print('***')
			print('Setting controller to position, Initial Motor: ' + str(initialMotor))
			input('Press Enter to Continue...')

			setControlMode(devId, CTRL_POSITION)
			setPosition(devId, initialMotor)
			zGain1 = 200
			zGain2 = 1
			setGains(devId, zGain1, zGain2, 0, 0)
			print("You're in Position Control! P Gain: " + str(zGain1) + ", I Gain: " + str(zGain2))

			# Initialize variables
			dl 			= dataLogger('pos_follow_' + strftime("%Y%m%d-%H%M%S") + '.txt')	# Filename
			i 			= 0		# Loop counter
			data_vec 	= 0		# Data vector
			t0 			= time()
			tf			= 30

			try:				
				try:
					#while(time()-t0<tf):	# run for a certain length of time
					while True:				# run indefinitely until keyboard press
						i += 1
						t = time() - t0
						sleep(0.001)	
						data = fxReadDevice(devId, varsToStream)

						# Attempt at catching "Failed to Read Device Data" (doesn't work!)
						if data[0] == None or data[1]==None or data[2]==None or data[3]==None or data[4]==None or data[5]==None or data[6]==None or data[7]==None or data[8]==None or data[9]==None or data[10]==None:
							input("Pause")

						# three point (rolling) median average to remove data spiking effects
						if i == 1:
							data = fxReadDevice(devId, varsToStream)
							data_prev0 = np.array(data)
						elif i == 2:
							data = fxReadDevice(devId, varsToStream)
							data_prev1 = data_prev0
							data_prev0 = np.array(data) 
						else:
							data = fxReadDevice(devId, varsToStream)
							data_prev2 = data_prev1
							data_prev1 = data_prev0
							data_prev0 = np.array(data)

							data_prev = np.vstack((data_prev2, data_prev1, data_prev0))	# stack previous data points into 3 x n matrix
							data_med = np.median(data_prev,axis=0)						# take median of columns	

							ankleAngle = data_med[varsToStream.index(FX_ANKLE_ANG)]
							motorAngle = data_med[varsToStream.index(FX_ENC_ANG)]
							motorCurrent = data_med[varsToStream.index(FX_MOT_CURR)]
							desiredMotor = np.floor(np.polyval(coeffs_zeroed,ankleAngle) + slackOffset*45.5111) # Slack offset converted to motor counts

                            # Data to record
							data_vec = [i] + [t] + [desiredMotor] + data_med.tolist() + data + coeffs_zeroed.tolist() + [zeroing] + [slackOffset] + [zGain1] + [zGain2]
							dl.appendData(data_vec)

                            # set position
							setPosition(devId, desiredMotor)

							# safety check
							if abs(motorCurrent) > 9000: # 9 amps
								print('Error: Amperage too high.')
								# Save sensor data
								dl.writeOut()
								# Turn off Position Control
								finalAngle= fxReadDevice(devId, [FX_ENC_ANG])[0]	
								setPosition(devId, finalAngle)
								setControlMode(devId, CTRL_NONE)
								sleep(1)
								fxStopStreaming(devId)	
								break
				except: 
					# Summary
					print('')
					print('Iterations:   %20.2f'   % i)
					print('Elapsed Time: %20.2f s' % t)
					print('Mean freq:    %20.2f Hz'  % ((i + 0.0)/(time()-t0)))
					# Save sensor data
					dl.writeOut()
                    # Turn off Position Control
					finalAngle= fxReadDevice(devId, [FX_ENC_ANG])[0]	
					setPosition(devId, finalAngle)
					setControlMode(devId, CTRL_NONE)
					sleep(1)
					fxStopStreaming(devId)	

			except:	
				# Summary
				print('')
				print('Iterations:   %20.2f'   % i)
				print('Elapsed Time: %20.2f s' % t)
				print('Mean freq:    %20.2f Hz'  % ((i + 0.0)/(time()-t0)))
				# Save sensor data
				dl.writeOut()
                # Turn off Position Control
				finalAngle= fxReadDevice(devId, [FX_ENC_ANG])[0]	
				setPosition(devId, finalAngle)
				setControlMode(devId, CTRL_NONE)
				sleep(1)
				fxStopStreaming(devId)
		else: 
			check_flag = 0

if __name__ == '__main__':
	ports = sys.argv[1:2] # 1:3 for 2 devices
	print(ports)
	devId = loadAndGetDevice(ports)[0]
	# Choose side on startup
	ex0=0
	while ex0==0:
		side_tmp = input("Which leg? L/R?")
		if side_tmp=='L' or side_tmp=='l' or side_tmp=='Left' or side_tmp=='LEFT' or side_tmp=='left':
			side = 'left'
			ex0 = 1
		elif side_tmp=='R' or side_tmp=='r' or side_tmp=='Right' or side_tmp=='RIGHT' or side_tmp=='right':
			side = 'right'
			ex0 = 1
		else: 
			print("Incorrect choice. Please choose L or R.")
	print(side)

	try:
		TaughtController(devId,side)	
	except Exception as e:
		print("broke: " + str(e))
		pass	
	# right leg = negative current, left leg = positive current
	# if side=='left':
	# 	setCurrent = abs(int(cur))
	# elif side == 'right':
	# 	setCurrent = -abs(int(cur))
	# setMotorCurrent(devId, setCurrent)
	# return setCurrent