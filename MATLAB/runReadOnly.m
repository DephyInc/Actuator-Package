
function runReadOnly( libHandle, deviceId )
% Read the FlexSEA Parameters and display them
    disp('Read Only test');

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
FX_RIGID_GEN_VAR_BASE = 18;
FX_RIGID_GEN_VAR_9 = (FX_RIGID_GEN_VAR_BASE + 9);

    labels = {  'State time',        ...
                'accel x', 	'accel y', 	'accel z', 	...
                'gyro x', 	'gyro y',	'gyro z', 	...
                'encoder angle',     ...
                'ankle angle',	     ...
                'motor voltage'      ...
};

varsToStream = [                ...
    FX_RIGID_STATETIME,         ...
    FX_RIGID_ACCELX,	FX_RIGID_ACCELY,	FX_RIGID_ACCELZ, ...
    FX_RIGID_GYROX,  	FX_RIGID_GYROY,  	FX_RIGID_GYROZ,	 ...
    FX_RIGID_ENC_ANG,	        ...
    FX_RIGID_GEN_VAR_9,         ...
    FX_RIGID_MOT_VOLT	        ...
];

    outVars = [ 99, 99, 99, 99, 99, 99, 99, 99, 99, 99 ];

    % Select the variables to stream
    [retCode, outVars ] = calllib(libHandle, 'fxSetStreamVariables', deviceId,  varsToStream, 10 );

    % Start streaming
    retCode = calllib(libHandle, 'fxStartStreaming', deviceId, 100, false, 0 );
    if( ~retCode)
        fprintf("Couldn't start streaming...\n");
    else

        for loopCount = 50:-1:0
            pause(.500);
            clc;
            fprintf("Streaming data from device %d (%d)\n", deviceId, loopCount );
            printDevice( libHandle, deviceId, varsToStream, labels, 10);
        end
    end
    calllib(libHandle, 'fxStopStreaming', deviceId);
end
