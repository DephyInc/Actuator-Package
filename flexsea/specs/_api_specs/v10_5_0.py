# pylint: disable=duplicate-code

import ctypes as c

from flexsea import firmware as fw

v10_5_0 = {
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
        # "get_field_data_types": {
        #     "name": "fxGetDeviceDataTypes",
        #     "argTypes": [c.c_uint, c.POINTER(c.c_uint8), c.POINTER(c.c_uint8)],
        #     "returnType": c.c_int,
        # },
        "get_max_device_name_length": {
            "name": "fxGetMaxDeviceNameLength",
            "argTypes": [],
            "returnType": c.c_int,
        },
        "get_device_name": {
            "name": "fxGetDeviceTypeNameWrapper",
            "argTypes": [c.c_uint, c.c_char_p],
            "returnType": c.c_int,
        },
        "get_max_device_side_length": {
            "name": "fxGetMaxDeviceSideNameLength",
            "argTypes": [],
            "returnType": c.c_int,
        },
        "get_side": {
            "name": "fxGetDeviceSideNameWrapper",
            "argTypes": [c.c_uint, c.c_char_p],
            "returnType": c.c_int,
        },
        "get_libs_version": {
            "name": "fxGetLibsVersion",
            "argTypes": [
                c.POINTER(c.c_uint16),
                c.POINTER(c.c_uint16),
                c.POINTER(c.c_uint16),
            ],
            "returnType": c.c_int,
        },
        "get_max_field_name_length": {
            "name": "fxGetMaxDataLabelLength",
            "argTypes": [],
            "returnType": c.c_int,
        },
        "get_fields": {
            "name": "fxGetDataLabelsWrapper",
            "argTypes": [c.c_uint, c.POINTER(c.POINTER(c.c_char)), c.POINTER(c.c_int)],
            "returnType": c.c_int,
        },
        "get_max_data_elements": {
            "name": "fxGetMaxDataElements",
            "argTypes": [],
            "returnType": c.c_int,
        },
        "read": {
            "name": "fxReadDevice",
            # "argTypes": [c.c_uint, c.POINTER(c.c_uint32), c.POINTER(c.c_int)],
            "argTypes": [c.c_uint, c.POINTER(c.c_int32), c.POINTER(c.c_int)],
            "returnType": c.c_int,
        },
        "read_all": {
            "name": "fxReadDeviceAllWrapper",
            "argTypes": [c.c_uint, c.POINTER(c.POINTER(c.c_int32)), c.POINTER(c.c_int)],
            "returnType": None,
        },
        "request_uvlo": {
            "name": "fxRequestUVLO",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "read_uvlo": {
            "name": "fxGetLastReceivedUVLO",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "set_uvlo": {
            "name": "fxSetUVLO",
            "argTypes": [c.c_uint, c.c_uint],
            "returnType": c.c_int,
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
        "start_streaming_with_safety": {
            "name": "fxStartStreamingWithSafety",
            "argTypes": [c.c_uint, c.c_uint, c.c_bool, c.c_uint16],
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
        "get_num_utts": {
            "name": "fxGetNumUtts",
            "argtypes": [],
            "returnType": c.c_int,
        },
        "set_utts": {
            "name": "fxSetUTT",
            "argTypes": [c.c_uint, c.POINTER(c.c_int), c.c_uint, c.c_byte],
            "returnType": c.c_int,
        },
        "reset_utts": {
            "name": "fxSetUTTsToDefault",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "save_utts": {
            "name": "fxSaveUTTToMemory",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "request_utts": {
            "name": "fxRequestUTT",
            "argTypes": [
                c.c_uint,
            ],
            "returnType": c.c_int,
        },
        "get_last_received_utts": {
            "name": "fxGetLastReceivedUTT",
            "argTypes": [c.c_uint, c.POINTER(c.c_int), c.c_uint],
            "returnType": c.c_int,
        },
    },
}
