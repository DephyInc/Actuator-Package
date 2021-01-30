function openConfiguration( block )
% Set up any memory required
fprintf('Configuring Work vectors (memory)\n');

block.NumDworks = 1;

% Initialize a work vector to hold the device ID
block.Dwork(1).Name = 'DeviceID';
block.Dwork(1).Dimensions = 1;
block.Dwork(1).DataTypeID = 6; % (INT32)
block.Dwork(1).Complexity = 'Real';
block.Dwork(1).UsedAsDiscState = false; % No saved state
block.Dwork(1).Usage = 'DWork';

end
