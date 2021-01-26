function setup (block )
% setup callback for the OPEN control simulation

block.NumDialogPrms = 0;    % There are no program inputs
block.NumInputPorts = 1;    % We have one input to the block
block.NumOutputPorts = 9;   % Nine outputs from the block
                            % One for each variable to stream

%block.SetPreCompInpPortInfoToDynamic;
block.SampleTimes = [ -1 0];

% Input port properties (Motor voltage)
block.InputPort(1).Dimensions = 1;
block.InputPort(1).DataTypeID = 6;         % (INT32)
block.InputPort(1).Complexity = 'Real';
block.InputPort(1).SamplingMode = 'Sample';
block.InputPort(1).DirectFeedThrough = 1;

% Set up the output ports (one per variable to stream)
% Output properties for STATE TIME variable
block.OutputPort(1).Dimensions = 1;
block.OutputPort(1).DataTypeID = 6;         % (INT32)
block.OutputPort(1).Complexity = 'Real';    % Non-complex inputs
block.OutputPort(1).SamplingMode = 'Sample';

% Output properties for ACCELERATION X variable
block.OutputPort(2).Dimensions = 1;
block.OutputPort(2).DataTypeID = 6;         % (INT32)
block.OutputPort(2).Complexity = 'Real';
block.OutputPort(2).SamplingMode = 'Sample';

% Output properties for Acceleration Y variable
block.OutputPort(3).Dimensions = 1;
block.OutputPort(3).DataTypeID = 6;         % (INT32)
block.OutputPort(3).Complexity = 'Real';
block.OutputPort(3).SamplingMode = 'Sample';

% Output properties for ACCELERATION Z variable
block.OutputPort(4).Dimensions = 1;
block.OutputPort(4).DataTypeID = 6;         % (INT32)
block.OutputPort(4).Complexity = 'Real';
block.OutputPort(4).SamplingMode = 'Sample';

% Output properties for GYRO X variable
block.OutputPort(5).Dimensions = 1;
block.OutputPort(5).DataTypeID = 6;         % (INT32)
block.OutputPort(5).Complexity = 'Real';
block.OutputPort(5).SamplingMode = 'Sample';

% Output properties for GYRO Y variable
block.OutputPort(6).Dimensions = 1;
block.OutputPort(6).DataTypeID = 6;         % (INT32)
block.OutputPort(6).Complexity = 'Real';
block.OutputPort(6).SamplingMode = 'Sample';

% Output properties for GYRO Z variable
block.OutputPort(7).Dimensions = 1;
block.OutputPort(7).DataTypeID = 6;         % (INT32)
block.OutputPort(7).Complexity = 'Real';
block.OutputPort(7).SamplingMode = 'Sample';

% Output properties for ENCODER ANGLE variable
block.OutputPort(8).Dimensions = 1;
block.OutputPort(8).DataTypeID = 6;         % (INT32)
block.OutputPort(8).Complexity = 'Real';
block.OutputPort(8).SamplingMode = 'Sample';

% Output properties for MOTOR VOLTAGE variable
block.OutputPort(9).Dimensions = 1;
block.OutputPort(9).DataTypeID = 6;         % (INT32)
block.OutputPort(9).Complexity = 'Real';
block.OutputPort(9).SamplingMode = 'Sample';

% There is no state saved between simulation steps
block.SimStateCompliance = 'HasNoSimState';

% Register the callbacks needed
block.RegBlockMethod('Outputs',              @openControlOutput);     % Compute the output parameters
block.RegBlockMethod('Terminate',            @openControlTerminate);  % Clean up what we have done
block.RegBlockMethod('PostPropagationSetup', @openConfiguration);     % Initialize work vectors (memory)
block.RegBlockMethod('Start',                @openControlStart);      % Start the simulation


end