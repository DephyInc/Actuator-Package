% FlexSEA Demo program

% Set up the environment
errCode = loadAndGetDevice();
if( ~errCode )
   disp("Failed to initialize the FlexSEA environment\n");
else
    test = displayMenu();
    fprintf (" You chose test %d\n", test);

    % Close COM ports
    calllib('libfx_plan_stack', 'fxClose', 1);

    disp('unloading library and cleaning up');
    calllib('libfx_plan_stack', 'fxCleanup');
    unloadlibrary 'libfx_plan_stack'
end

function test = displayMenu()
% Display the test selection menu and wait for user to select one

    disp( "0) Read only");
    disp( "1) Open speed");
    disp( "2) Current Control");
    disp( "3) Hold Position");
    disp( "4) Find Poles");
    disp( "5) Two Device Position Control");
    disp( "6) Two Device Leader-Follower");

    test = input("Choose the test to run: ");
    switch test
        case 0
            runReadOnly();
        otherwise
            disp('Unimplmented test');
    end;
end

function ports = readConfig()
  % Read the configuration file (com.txt) - 1 port per line

% Open the configuration file
fid = fopen('com.txt', 'r');
if( fid == -1)
    disp("Could not open configuration file\n");
    ports = '';
else
%    line = fgetl( fid );
%    while line ~= -1 
%        ports = line;
%        line = fgetl( fid );
    ports =  'com3';
end

% close the configuration file
fclose( fid );
end

function retCode = loadAndGetDevice()
% Load the FlexSEA DLL and prepare the environment
    disp('Loading library and Initializing');
    retCode = false;
    
    % if the FlexSEA DLL is loaded, unload it
    %  we want to use the latest version
    if libisloaded('libfx_plan_stack')
        unloadlibrary 'libfx_plan_stack'
    end
    
    % Add relative path to library/header file
    disp('adding paths');
    addpath( '..\fx_plan_stack\lib64');
    addpath( '..\fx_plan_stack\include\flexseastack');
    disp('Loading library');
    loadlibrary('libfx_plan_stack', 'com_wrapper');
    if libisloaded( 'libfx_plan_stack' );
        % Initialize the FX environment
        calllib('libfx_plan_stack', 'fxSetup');
    
        % Check to see what COM ports to use
        ports = readConfig();
        fprintf("Com ports found\n%6s\n", ports);
        
        % zzz We need to loop until all of the ports opens
        % Now open the COM port
        calllib('libfx_plan_stack', 'fxOpen', ports, 1);
        pause(1);
        retCode = false;
        iterCount = 10;
        fprintf("zzz port %s\n", ports);
        while ~retCode && iterCount > 0
            pause(1);
            retCode = calllib('libfx_plan_stack', 'fxIsOpen', 1);
            if( ~retCode )
                fprintf("Could not open port %s\n", ports);
            end
            iterCount = iterCount - 1;
        end
        
        % Get the device IDs
        deviceIds = [ -3, -2, -2 ];
        %fprintf("ZZZ START DEVICE IDS %d\n", deviceIds);
        deviceIds = calllib('libfx_plan_stack', 'fxGetDeviceIds', deviceIds, 3);
        if( deviceIds( 1 ) == -1)
            fprintf("zzz got no device ids %d\n", deviceIds);
        else
            fprintf("ZZZ GOT DEVICE IDS %d\n", deviceIds);
        end
    else
        retCode = true;
    end
end
