% FlexSEA Demo program

clearvars;
clc;
close all;
clear all;

deviceIds = [ -99, -99, -99 ];
ports = cellstr([ '', '', '' ]);

%shouldQuit = false;
%shouldQuit = onCleanup( @() signalHander(shouldQuit) )

% Check to see what COM ports to use
ports = readConfig();

% Set up the environment
[ errCode, deviceIds] = loadAndGetDevice( ports );
if( ~errCode )
	disp("Failed to initialize the FlexSEA environment\n");
else
	test = displayMenu();
	fprintf (" You chose test %d\n", test);

	% Run the selected test
	switch test
		case 0
			runReadOnly( 'libfx_plan_stack', deviceIds( 1 ) );
		case 1
			runOpenControl( 'libfx_plan_stack', deviceIds( 1 ) );
		case 2
			runCurrentControl( 'libfx_plan_stack', deviceIds( 1 ) );
		case 3
			runPositionControl( 'libfx_plan_stack', deviceIds( 1 ) );
		case 4
			runFindPoles( 'libfx_plan_stack', deviceIds(1));
		case 5
			runTwoDevicePosition( 'libfx_plan_stack', deviceIds);
		case 6
			RunLeaderFollower( 'libfx_plan_stack', deviceIds );
		otherwise
			disp('Unimplmented test');
	end
end

% Close COM ports
fprintf("Closing com ports\n");
for i = 1:length( ports )
	if( ports{i} )
		calllib('libfx_plan_stack', 'fxClose', i);
	end
end

if libisloaded( 'libfx_plan_stack' )
	disp('unloading library and cleaning up');
	calllib('libfx_plan_stack', 'fxCleanup');
end
unloadlibrary 'libfx_plan_stack'


function test = displayMenu()
% Display the test selection menu and wait for user to select one

	clc;
	disp( "Stop! Read our important safety information at https://dephy.com/start/ before running the scripts for the first time.\n\n");
	disp( "0) Read only");
	disp( "1) Open control");
	disp( "2) Current Control");
	disp( "3) Hold Position");
	disp( "4) Find Poles");
	disp( "5) Two Device Position Control. Temporarily NON-OPERATIONAL.  RUN AT YOUR OWN RISK.");
	disp( "6) Two Device Leader-Follower");

	test = input("Choose the test to run: ");
	clc;
end

function [ retCode, deviceIds] = loadAndGetDevice( ports )
% Load the FlexSEA DLL and prepare the environment
	disp('Loading library and Initializing');

	retCode = false;

	% if the FlexSEA DLL is loaded, unload it
	%  we want to use the latest version
	if libisloaded('libfx_plan_stack')
		unloadlibrary 'libfx_plan_stack'
	end

	% Add relative path to library/header file
	disp('Loading library');
	addpath( '..\libs\win64');
	addpath( '..\inc\flexseastack');
	loadlibrary('libfx_plan_stack', 'com_wrapper');
	if libisloaded( 'libfx_plan_stack' )
		% Initialize the FX environment
		calllib('libfx_plan_stack', 'fxSetup');

		% We need to loop until all of the ports are open
		for i = 1:length( ports )
			if( ports{i} )
				% Now open the COM port
				fprintf("Opening port %s\n", ports{i});
				calllib('libfx_plan_stack', 'fxOpen', ports{i}, i, 230400);
				pause(.200);
				retCode = false;
				iterCount = 10;
				while ~retCode && iterCount > 0
					pause(.200);
					retCode = calllib('libfx_plan_stack', 'fxIsOpen', i);
					if( ~retCode )
						fprintf("Could not open port %s\n", ports{i});
					end
					iterCount = iterCount - 1;
				end
			end
		end

		% Get the device IDs
		deviceIds = [ -3, -2, -2 ];
		deviceIds = calllib('libfx_plan_stack', 'fxGetDeviceIds', deviceIds, 3);
		if( deviceIds( 1 ) == -1)
			fprintf("Got no device ids\n");
		end
	else
		retCode = true;
	end
end

function runFindPoles( libHandle, devId)
	calllib('libfx_plan_stack', 'findPoles', devId, true);
end
%function shouldQuit = signalHander( ShouldQuit )
%    disp("CTRL-C Caught\n");
%    shouldQuit = true;
%end
