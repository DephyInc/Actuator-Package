function runPositionControl(libHandle, devId)

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

    outVars = [ 99, 99, 99, 99, 99, 99, 99, 99, 99 ];
    
    % Select the variables to stream
    [retCode, outVars ] = calllib(libHandle, 'fxSetStreamVariables', devId,  varsToStream, 9 );
    
    % Start streaming
    retCode = calllib(libHandle, 'fxStartStreaming', devId, 100, false, 0 );
    if( ~retCode)
        fprintf("Couldn't start streaming...\n");
    else
        % Determine the devices initial angle
        retries = 100;
        initialAngle = readDeviceVar( libHandle, devId, FX_RIGID_ENC_ANG);
        while( retries && isnan( initialAngle ) )
            pause(.100);
            initialAngle = readDeviceVar( libHandle, devId, FX_RIGID_ENC_ANG);
            retries = retries -1;
        end
        % Enable the controller 
        calllib(libHandle, 'setPosition', devId, initialAngle);
        calllib(libHandle, 'setControlMode', devId, CTRL_POSITION);
        calllib(libHandle, 'setPosition', devId, initialAngle);
        calllib(libHandle, 'setZGains', devId, 50, 3, 0, 0);
            
        % Now, hold this poisition against user turn
        for i = 100: -1: 0
            pause(.250);
            clc;
            fprintf("Holding device %d at position %d (%d)\n", devId, initialAngle, i);
            printDevice( libHandle, devId, varsToStream, labels, 9);
        end

        pause(.200);
        calllib(libHandle, 'setControlMode', devId, CTRL_NONE);
        pause(.200);
        calllib(libHandle, 'fxStopStreaming', devId);
    end
end

