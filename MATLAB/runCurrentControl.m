function runCurrentControl( libHandle, devId)
% Run the Current Control demo

CTRL_NONE    = 0;
CTRL_CURRENT = 3;

% field ids
FX_RIGID_STATETIME = 2;
FX_RIGID_ENC_ANG = 9;
FX_RIGID_MOT_CURR = 12;

labels = {  'State time', 	    ...
			'encoder angle', 	...
			'motor current'		...
};

varsToStream = [ 		...
	FX_RIGID_STATETIME, 		...
	FX_RIGID_ENC_ANG,		...
	FX_RIGID_MOT_CURR		...
];

	[retCode, outVars ] = calllib(libHandle, 'fxSetStreamVariables', devId,  varsToStream, 3 );

	% Start streaming
	retCode = calllib(libHandle, 'fxStartStreaming', devId, 100, false, 0 );
	if( ~retCode)
		fprintf("Couldn't start streaming...\n");
	else

		holdCurrent = 500;

		fprintf('Setting controller to current control mode...')
		calllib(libHandle, 'setControlMode', devId, CTRL_CURRENT );
		calllib(libHandle, 'setGains', devId, 100, 20, 0, 0 );
		calllib(libHandle, 'setMotorCurrent', devId, holdCurrent );

		loopCount = 50;
		while( loopCount )
			pause(.200);
			clc;
			fprintf("Holding current %d\n", holdCurrent);
			printDevice(libHandle, devId, varsToStream, labels, 3);
			loopCount = loopCount - 1;
		end

		fprintf('Ramping down the current...\n')
		% Ramp down the holding current
		n = 50;
		for i=1:50
			pause(.400);
			calllib(libHandle, 'setMotorCurrent', devId, (holdCurrent * (n - i) / n));
		end

		% Wait for motor to spin down
		calllib(libHandle, 'setMotorCurrent', devId, 0);
		i = 20;
		while( i )
			lastAngle = readDeviceVar( libHandle, devId, FX_RIGID_ENC_ANG);
			if( ~isnan( lastAngle ))
				i = i - 1;
			else
				i = 0;
			end
		end

		pause(.200);
		i = 20;
		while( i )
			currentAngle = readDeviceVar( libHandle, devId, FX_RIGID_ENC_ANG);
			if( ~isnan(currentAngle) )
				i = i -1;
			else
				i = 0;
			end
		end

		while( abs(currentAngle - lastAngle) > 100)
			temp = readDeviceVar( libHandle, devId, FX_RIGID_ENC_ANG);
			if( ~isnan( temp ))
				lastAngle = currentAngle;
				currentAngle = temp;
			end
		end
	end
	calllib(libHandle, 'setControlMode', devId, CTRL_NONE );
	pause(.200);
	calllib(libHandle, 'fxStopStreaming', devId);
end
