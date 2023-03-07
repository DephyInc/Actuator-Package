# pylint: disable=duplicate-code

import ctypes as c

from flexsea import firmware as fw
from flexsea.specs.device_specs import all_devices as fxd

read_functions = {
    "actpack": {
        "name": "fxReadDevice",
        "argTypes": [c.c_uint, c.POINTER(fxd.ActPackState)],
        "returnType": c.c_int,
        "all_name": "fxReadDeviceAll",
        "all_argTypes": [c.c_uint, c.POINTER(fxd.ActPackState), c.c_uint],
        "all_returnType": c.c_int,
    },
    "exo": {
        "name": "fxReadDevice",
        "argTypes": [c.c_uint, c.POINTER(fxd.EB60State)],
        "returnType": c.c_int,
        "all_name": "fxReadDeviceAll",
        "all_argTypes": [c.c_uint, c.POINTER(fxd.EB60State), c.c_uint],
        "all_returnType": c.c_int,
    },
}


v7_2_6 = {
    "commands": {
        "is_open": {
            "name": "fxIsOpen",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_bool,
        },
        "is_streaming": {
            "name": "fxIsStreaming",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_bool,
        },
        "open": {
            "name": "fxOpen",
            "argTypes": [c.c_char_p, c.c_uint, c.c_uint],
            "returnType": c.c_int,
        },
        "close": {
            "name": "fxClose",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "start_streaming": {
            "name": "fxStartStreaming",
            "argTypes": [c.c_uint, c.c_uint, c.c_bool],
            "returnType": c.c_int,
        },
        "stop_streaming": {
            "name": "fxStopStreaming",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "set_gains": {
            "name": "fxSetGains",
            "argTypes": [
                c.c_uint,
                c.c_uint,
                c.c_uint,
                c.c_uint,
                c.c_uint,
                c.c_uint,
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "send_motor_command": {
            "name": "fxSendMotorCommand",
            "argTypes": [c.c_uint, c.c_int, c.c_int],
            "returnType": c.c_int,
        },
        "find_poles": {
            "name": "fxFindPoles",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "activate_bootloader": {
            "name": "fxActivateBootloader",
            "argTypes": [c.c_uint, c.c_uint8],
            "returnType": c.c_int,
        },
        "is_bootloader_activated": {
            "name": "fxIsBootloaderActivated",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "request_firmware_version": {
            "name": "fxRequestFirmwareVersion",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "get_last_received_firmware_version": {
            "name": "fxGetLastReceivedFirmwareVersion",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": fw.Firmware,
        },
        "get_device_type_value": {
            "name": "fxGetAppType",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "get_read_data_queue_size": {
            "name": "fxGetReadDataQueueSize",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "set_read_data_queue_size": {
            "name": "fxSetReadDataQueueSize",
            "argTypes": [c.c_uint, c.c_uint],
            "returnType": c.c_uint,
        },
    },
    "read_functions": read_functions,
}
