function openControlOutput( block )
% 'Compute' the output data for this simulation state

% Set the motor voltage to the value in this step
fprintf('Setting %d motor voltage to %d\n', block.Dwork(1).Data, block.InputPort(1).Data);
calllib('libfx_plan_stack', 'setMotorVoltage', block.Dwork(1).Data, block.InputPort(1).Data);

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
labels = {  'State time', 	    ...
			'accel x', 	'accel y', 	'accel z', 	...
			'gyro x', 	'gyro y',	'gyro z', 	...
			'encoder angle', 	...
			'motor voltage'		...
};

	success = [ -1, -1, -1, -1, -1, -1, -1, -1, -1 ];
	retData = [ -1, -1, -1, -1, -1, -1, -1, -1, -1 ];

	[ ptr, retData, success] = calllib('libfx_plan_stack', 'fxReadDevice', block.Dwork(1).Data, varsToStream, success, 9);
	%pause(.050);
	% Jump through some hoops to get access to the returned data
	ptrindex = libpointer('int32Ptr', zeros(1:9, 'int32'));
	ptrindex = ptr;
	setdatatype(ptrindex, 'int32Ptr', 1, 9);

	for i= 1:9
		if( success(i) ~= 0)
			fprintf("\t%14s\t%d\n", labels{i}, ptrindex.value(i) );
			block.OutputPort(i).Data = ptrindex.value(i);
		else
			fprintf("\t%14s\t------\n", labels{i} );
		end
	end
end
