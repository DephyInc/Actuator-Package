function runTwoDevicePosition(libHandle, devIds)

CTRL_NONE     = 0;
CTRL_POSITION = 2;

% field ids
FX_RIGID_STATETIME = 2;
FX_RIGID_ACCELX = 3;
FX_RIGID_ACCELY = 4;
FX_RIGID_ACCELZ = 5;
FX_RIGID_GYROX  = 6;
FX_RIGID_GYROY  = 7;
FX_RIGID_GYROZ  = 8;
FX_RIGID_ENC_ANG = 9;
FX_RIGID_MOT_VOLT = 13;
FX_RIGID_BATT_VOLT = 14;

labels = [  "State time", ...
			"accel x", "accel y", "accel z", ...
			"gyro x", "gyro y", "gyro z", 	 ...
			"encoder angle",                ...
			"motor voltage"					...
];

varsToStream = [ 							...
	FX_RIGID_STATETIME, 					...
	FX_RIGID_ACCELX, FX_RIGID_ACCELY, FX_RIGID_ACCELZ, 	...
	FX_RIGID_GYROX,  FX_RIGID_GYROY,  FX_RIGID_GYROZ,	...
	FX_RIGID_ENC_ANG,						...
	FX_RIGID_MOT_VOLT						...
];

	% Select the variables to stream
	[retCode1, outVars ] = calllib(libHandle, 'fxSetStreamVariables', devIds(1),  varsToStream, 9 );
	[retCode2, outVars ] = calllib(libHandle, 'fxSetStreamVariables', devIds(2),  varsToStream, 9 );

	% Start streaming
	retCode1 = calllib(libHandle, 'fxStartStreaming', devIds(1), 100, false, 0 );
	retCode2 = calllib(libHandle, 'fxStartStreaming', devIds(2), 100, false, 0 );
	if( ~(retCode1 &&  retCode2) )
		fprintf("Couldn't start streaming...\n");
	else
		% Determine the initial positions
		initialAngle1 = readDeviceVar( libHandle, devIds(1), FX_RIGID_ENC_ANG);
		initialAngle2 = readDeviceVar( libHandle, devIds(2), FX_RIGID_ENC_ANG);
		while( isnan(initialAngle1) && isnan(initialAngle2))
			pause(.500);
			initialAngle1 = readDeviceVar( libHandle, devIds(1), FX_RIGID_ENC_ANG);
			initialAngle2 = readDeviceVar( libHandle, devIds(2), FX_RIGID_ENC_ANG);
		end

		% Set position control for both devices
		calllib(libHandle, 'setPosition', devIds(1), initialAngle1);
		calllib(libHandle, 'setControlMode', devIds(1), CTRL_POSITION);
		calllib(libHandle, 'setPosition', devIds(1), initialAngle1);
		calllib(libHandle, 'setGains', devIds(1), 50, 3, 0, 0);

		calllib(libHandle, 'setPosition', devIds(2), initialAngle2);
		calllib(libHandle, 'setControlMode', devIds(2), CTRL_POSITION);
		calllib(libHandle, 'setPosition', devIds(2), initialAngle2);
		calllib(libHandle, 'setGains', devIds(2), 50, 3, 0, 0);

		for i  = 100: -1: 0
			pause(.200);
			clc;
			fprintf("Holding device position on two devices\n");
			fprintf("Streaming data from device %d (%d)\n", devIds(1), i);
			printDevice( libHandle, devIds(1), varsToStream, labels, 9);
			fprintf("Streaming data from device %d (%d)\n", devIds(2), i);
			printDevice( libHandle, devIds(2), varsToStream, labels, 9);
		end
	end
	% Turn off position control
	calllib(libHandle, 'setControlMode', devIds(1), CTRL_NONE);
	calllib(libHandle, 'setControlMode', devIds(2), CTRL_NONE);
	pause(.200);
	calllib(libHandle, 'fxStopStreaming', devIds(1));
	calllib(libHandle, 'fxStopStreaming', devIds(2));
end
