function openControlTerminate( block )
% Clean up after simulation

fprintf('Terminating simulation\n');
CTRL_NONE = 0;

    % Stop the motor and disable the control mode and
    fprintf('Cleaning up simulation\n');
    calllib('libfx_plan_stack', 'setMotorVoltage', block.Dwork(1).Data, 0);
    pause(.200);
    calllib('libfx_plan_stack', 'setControlMode', block.Dwork(1).Data, CTRL_NONE);
    pause(.200);
    calllib('libfx_plan_stack', 'fxStopStreaming', block.Dwork(1).Data);
    fprintf('Closing com port\n');
    pause(.200);
    calllib('libfx_plan_stack', 'fxClose', 1);

    % Ensure we clean up the DLL environment
    fprintf('Closing DLL\n');
    calllib('libfx_plan_stack', 'fxCleanup');
    pause(.200);

    % Unload the FX_PLAN_STACK DLL
    if libisloaded('libfx_plan_stack')
        fprintf('Unloading library\n');
        unloadlibrary 'libfx_plan_stack'
    end
end