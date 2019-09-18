function RunLeaderFollower( libHandle, deviceIds )
% Run the leader/follower test on the frst two devices

disp('Run Leader/Follower test');

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

% Motor & Control commands:
CTRL_NONE     = 0;
CTRL_POSITION = 2;
CTRL_CURRENT  = 3;

labels = {  'State time', 	    ...
            'accel x', 	'accel y', 	'accel z', 	...
            'gyro x', 	'gyro y',	'gyro z', 	...
            'encoder angle', 	...
            'motor voltage'		...
};

varsToStream = [ 		...
	FX_RIGID_STATETIME, 		...
    FX_RIGID_ACCELX,	FX_RIGID_ACCELY,	FX_RIGID_ACCELZ, 	...
    FX_RIGID_GYROX,  	FX_RIGID_GYROY,  	FX_RIGID_GYROZ,	...
	FX_RIGID_ENC_ANG,		...
	FX_RIGID_MOT_VOLT		...
];
VarEncAngle = [ FX_RIGID_ENC_ANG ];

    % Make sure to reserve space for the outputs
    outVars  = zeros( 9, 'int32' );
    success1 = zeros( 9, 'int32' );
    success2 = zeros( 9, 'int32' );
    retData  = zeros( 9, 'int32' );
    
    initialAngle1 = 0;
    initialAngle2 = 0;
    
    % Select the variables to stream
    [retCode1, outVars ] = calllib(libHandle, 'fxSetStreamVariables', deviceIds(1),  varsToStream, 9 );
    [retCode2, outVars ] = calllib(libHandle, 'fxSetStreamVariables', deviceIds(2),  varsToStream, 9 );
    
    % Start streaming
    retCode1 = calllib(libHandle, 'fxStartStreaming', deviceIds(1), 100, false, 0 );
    retCode2 = calllib(libHandle, 'fxStartStreaming', deviceIds(2), 100, false, 0 );
    if( ~(retCode1 &&  retCode2) )
        fprintf("Couldn't start streaming...\n");
    else
        retries = 10;
        while ( retries )
            pause(.500);
            
            % Get the initial positions of the two devices
            % Note: We are only interested in the Encoder Angle at this
            % point. So only retrieve that from the devices
            initialAngle1 = readDeviceVar( libHandle, deviceIds(1), FX_RIGID_ENC_ANG);
            initialAngle2 = readDeviceVar( libHandle, deviceIds(2), FX_RIGID_ENC_ANG);
            if( ~isnan( initialAngle1 ) && ~isnan( initialAngle2 ) )
                retries = 0;
            end
        end
        
        % If we got the initial angles, proceed
        if( ~isnan( initialAngle1 ) && ~isnan( initialAngle2 ))
            fprintf("Turning on position control for device %d to follow %d\n", deviceIds(1), deviceIds(2));
            % set first device to current controller with 0 current (0 torque)
            calllib(libHandle, 'setControlMode', deviceIds(1), CTRL_CURRENT);
            calllib(libHandle, 'setGains', deviceIds(1), 100, 20, 0, 0);
            calllib(libHandle, 'setMotorCurrent', deviceIds(1), 0);

            % set position controller for second device
            calllib(libHandle, 'setPosition', deviceIds(2), initialAngle2);
            calllib(libHandle, 'setControlMode', deviceIds(2), CTRL_POSITION);
            calllib(libHandle, 'setPosition', deviceIds(2), initialAngle2);
            calllib(libHandle, 'setGains', deviceIds(2), 50, 3, 0, 0);

            loopCount = 50;
            while( loopCount )
                pause(.350);
                angle1 = readDeviceVar( libHandle, deviceIds(1), FX_RIGID_ENC_ANG);
                if( ~isnan( initialAngle1 ) )
                    diff = angle1 - initialAngle1;
                    calllib(libHandle, 'setPosition', deviceIds(2), initialAngle2 + (3 * diff));
                
                    % Now, for each device get ALL of the values and display them
                    clc;
                    fprintf("Device %d following device %d  (%d)\n", deviceIds(1), deviceIds(2), loopCount);
                    fprintf("Streaming data from device %d\n", deviceIds(1) );
                    printDevice( libHandle, deviceIds(1), varsToStream, labels, 9)
                    fprintf("Streaming data from device %d %d)\n", deviceIds(2), loopCount );
                    printDevice( libHandle, deviceIds(2), varsToStream, labels, 9)
                    loopCount = loopCount -1;
                end
            end
        end
    end
    
    % Clean up
    fprintf("Turning off position control\n");
    calllib(libHandle, 'setControlMode', deviceIds(1), CTRL_NONE);
    calllib(libHandle, 'setControlMode', deviceIds(2), CTRL_NONE);
    pause(.200);
    calllib(libHandle, 'fxStopStreaming', deviceIds(1));
    calllib(libHandle, 'fxStopStreaming', deviceIds(2));
end