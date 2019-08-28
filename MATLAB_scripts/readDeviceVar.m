function data = readDeviceVar( libHandle, devId, var )
% Read a single variable from a device. Returns NaN on failure

    retData = [ -1 ];
    success = [ -1 ];
    
    varToRead= [ var];
    [ ptr, retData, success] = calllib(libHandle, 'fxReadDevice', devId, varToRead, success, 1);
    ptrindex = libpointer('int32Ptr', zeros(1, 'int32'));
    ptrindex = ptr;
    setdatatype(ptrindex, 'int32Ptr', 1, 1);

    % If the read succeeded, return the value read
    if( success(1) ~= 0)
        data = ptrindex.value(1);
    else
        data = NaN;
    end
end