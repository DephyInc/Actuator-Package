
function printDevice( libHandle, devId, vars, labels, n)
% Read the variables from the device and print them
    success = [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ];
    retData = [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ];

    % Read the values from the device
    [ ptr, retData, success] = calllib(libHandle, 'fxReadDevice', devId, vars, success, n);

    % Jump through some hoops to get access to the returned data
    ptrindex = libpointer('int32Ptr', zeros(1:10, 'int32'));
    ptrindex = ptr;
    setdatatype(ptrindex, 'int32Ptr', 1, 10);
    
    % Print the data or failure indication
    for i = 1:length( vars )
        if( success(i) ~= 0)
            fprintf("\t%14s\t%d\n", labels{i}, ptrindex.value(i) );
        else
            fprintf("\t%14s\t------\n", labels{i} );
        end
    end
end