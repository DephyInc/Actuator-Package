function openControlStart( block )
% Fill in the pre-states and configuration
fprintf('Simulation starting...\n');

% Load the FX_PLAN_STACK DLL
% Add relative path to library/header file
    disp('Loading library');
    addpath( '..\..\fx_plan_stack\lib64');
    addpath( '..\..\fx_plan_stack\include\flexseastack');
    loadlibrary('libfx_plan_stack', 'com_wrapper');
    if ~libisloaded( 'libfx_plan_stack' )
        fprintf('Could NOT load the DLL\n');
        return;
    else
        fprintf('Library is loaded!!! \n');
        % Initialize the FX environment
        calllib('libfx_plan_stack', 'fxSetup');
    end
    
    % Open the com port 
    % Hard coded to 'COM3' This should go into a DialogPrm
    com3 =  cellstr(['com3']);
    fprintf("Opening port %s\n", com3{1});
    calllib('libfx_plan_stack', 'fxOpen', com3{1}, 1);
    pause(.200);
    retCode = false;
    iterCount = 10;
    while ~retCode && iterCount > 0
        pause(.200);
        retCode = calllib('libfx_plan_stack', 'fxIsOpen', 1);
        if( ~retCode )
            fprintf("Could not open port %s (%d)\n", com3{1}, retCode);
        end
        iterCount = iterCount - 1;
    end
    if ~retCode
        fprintf('Could not open %s (%d)\n', com3{1}, retCode);
        return
    end
        
    % Get the device IDs (only one for this demo)
    deviceIds = [ -1, -1, -1 ];
    deviceIds = calllib('libfx_plan_stack', 'fxGetDeviceIds', deviceIds, 3);
    if( deviceIds( 1 ) ~= -1)
        block.Dwork(1).Data = deviceIds(1);
        fprintf("Using device id %d\n", block.Dwork(1).Data);
    else
        fprintf("Got no device ids\n");
        return;
    end

CTRL_OPEN = 1;

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

varsToStream = [ 		...
        FX_RIGID_STATETIME, 		...
        FX_RIGID_ACCELX,	FX_RIGID_ACCELY,	FX_RIGID_ACCELZ, 	...
        FX_RIGID_GYROX,  	FX_RIGID_GYROY,  	FX_RIGID_GYROZ,	...
        FX_RIGID_ENC_ANG,		...
        FX_RIGID_MOT_VOLT		...
];
outVars = [ 99, 99, 99, 99, 99, 99, 99, 99, 99];

    % Select the variables to stream and start streaming
    [retCode, outVars ] = calllib('libfx_plan_stack', 'fxSetStreamVariables', block.Dwork(1).Data,  varsToStream, 9 );
    retCode = calllib('libfx_plan_stack', 'fxStartStreaming', block.Dwork(1).Data, 100, false, 0 );
    if( ~retCode )
        fprintf("Couldn't start streaming...\n");
        return;
    else
        calllib('libfx_plan_stack', 'setControlMode', block.Dwork(1).Data, CTRL_OPEN);
        calllib('libfx_plan_stack', 'setMotorVoltage', block.Dwork(1).Data, 0);
    end
end