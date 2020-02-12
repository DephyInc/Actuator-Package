#ifndef DEVICE_WRAPPER_H
#define DEVICE_WRAPPER_H

#include <stdbool.h>
#include "actpack_struct.h"
#include "netmaster_struct.h"
#include "i2t_struct.h"

#ifdef __cplusplus
extern "C" 
{
#endif

typedef enum fxError 
{
	FxSuccess = 0,
	FxFailure,
	FxInvalidParam,
	FxInvalidDevice,
	FxNotStreaming,
	FxNoReadData

} FxError;

typedef enum fxControlMode
{
	FxPosition = 0,
	FxVoltage,
	FxCurrent,
	FxImpedance,
	FxNone

} FxControlMode;

typedef enum fxAppType
{
	FxInvalidApp = -1,
	FxActPack = 0,
	FxExo,
	FxNetMaster

} FxAppType;

struct ActPackState;
struct NetMasterState;

// Valid streaming frequencies 
#define NUM_TIMER_FREQS 11

static const int TIMER_FREQS_IN_HZ[NUM_TIMER_FREQS] = {1, 5, 10, 20, 33, 50, 100, 200, 300, 500, 1000};

// Max size of array returned by fxNumDevices
#define FX_MAX_DEVICES 10

#define MIN_UVLO 15000
#define MAX_UVLO 50000

#define MIN_CURRENT_OFFSET -15
#define MAX_CURRENT_OFFSET 15

/// Device ID is a 16-bit integer used to refer to a specific FlexSEA device 
///
/// Device ID is returned by fxOpen upon establishing a connection with a 
/// FlexSEA device, and is used by most of the functions in this library to 
/// specify which device to run that function on.

/// \brief Establish a connection with a FlexSEA device.
///
/// @param portName is the name of the serial port to open (e.g. "COM3")
/// 
/// @param baudRate is the baud rate used i.e. 115200, 230400, etc.
///
/// @param frequency is the frequency of communication with the FlexSEA device. 
/// This applies for streaming device data as well as sending commands to the 
/// device.
///
/// @param logLevel is the logging level for this device. 0 is most verbose and
/// 6 is the least verbose. Values greater than 6 are floored to 6.
///
/// @returns device ID (-1 if invalid/failed to open). 
/// 
/// @note Device ID is used by the functions in this API to specify which FlexSEA 
/// device to communicate with.
int fxOpen(const char* portName, 
		const unsigned int baudRate,
		const unsigned int logLevel);

/// \brief Check if the device with the given device ID is open.
///
/// @param deviceId is the ID of the device to check the open status of.
/// 
/// @returns true if open, false if not.
bool fxIsOpen(const unsigned int deviceId);

/// \brief Disconnect from a FlexSEA device with the given device ID.
/// @param deviceId is the ID of the device to close
/// 
/// @returns Error codes defined at top of the header
FxError fxClose(const unsigned int deviceId);

/// \brief Disconnect from all FlexSEA devices.
void fxCloseAll();

/// \brief Get the device ID of all connected FlexSEA devices. The device ID is
/// used by the functions in this API to specify which FlexSEA device to
/// communicate with.
///
/// @param idArray On return each element of the array will contain either a 
/// valid device ID or -1 (no device). This array should have at least as many 
/// elements as FlexSEA devices used.
/// 
/// @param size is the size of the idarray.
///
/// @returns Nothing. idarray is updated with device handles.
///
/// @note idArray should have at least as many elements as FlexSEA devices used.
void fxGetDeviceIds(int* const idArray, const unsigned int size);

/// \brief Start streaming data from a FlexSEA device.
///
/// @param deviceId is the device ID 
/// 
/// @param shouldLog If set true, the program logs all received data to a file.
/// The name of the file is formed as follows:
///
/// < FlexSEA model >_id< device ID >_< date and time >.csv
///
/// for example:
///
/// rigid_id3904_Tue_Nov_13_11_03_50_2018.csv
///
/// The file is formatted as a CSV file. The first line of the file will be 
/// headers for all columns. Each line after that will contain the data read 
/// from the device.
///
/// @returns Error codes defined at top of the header
FxError fxStartStreaming(const unsigned int deviceId, 
			const unsigned int frequency,
			const bool shouldLog);

/// \brief Stop streaming data from a FlexSEA device.
/// 
/// @param deviceId is the device ID 
/// 
/// @returns Error codes defined at top of the header
FxError fxStopStreaming(const unsigned int deviceId);

/// \brief Read the most recent data from a streaming FlexSEA device stream.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
FxError fxReadDevice(const unsigned int deviceId, ActPackState* readData);

/// \brief Read the most recent data from a streaming FlexSEA NetMaster device.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNoReadData if there is no data to read.
FxError fxReadNetMasterDevice(const unsigned int deviceId, NetMasterState* readData);


/// \brief Set the maximum read data queue size of a device.
/// 
/// @param deviceId is the device ID of the device to get the 
/// read data queue size from.
///
/// @param size is the size to set the read data queue size to.
///
/// @returns FxInvalidDevice if invalid device.
///		FxInvalidParam if size is invalid
FxError fxSetReadDataQueueSize(const unsigned int deviceId,
				const unsigned int size);

/// \brief Get the maximum read data queue size of a device.
/// 
/// @param deviceId is the device ID of the device to get the 
/// read data queue size from.
///
/// @returns size of the read data queue, or -1 if invalid device.
int fxGetReadDataQueueSize(const unsigned int deviceId);

/// \brief Read all data from a streaming FlexSEA device stream.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData is an array of size n which contains read results
///
/// @param n is the size of the readData y. Will only fill up to 
/// data read queue size. 
///
/// @returns The actual number of entries read. You will probably need
/// to use this number.
///
/// @note Will only fill readData array up to read data queue size.
int fxReadDeviceAll(const unsigned int deviceId, 
			ActPackState* readData, 
			const unsigned int n);

/// \brief Read all exo data from a streaming FlexSEA NetMaster device.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData is an array of size n which contains read results
///
/// @param n is the size of the readData y
///
/// @returns The actual number of entries read. You will probably need
/// to use this number.
///
/// @note Will only fill readData array up to read data queue size.
int fxReadNetMasterDeviceAll(const unsigned int deviceId, 
			NetMasterState* readData, 
			const unsigned int n);

/// \brief Sets the gains used by PID controllers on the FlexSEA device.
///
/// @param deviceId is the device ID.
///
/// @param kp : Proportional gain 
///
/// @param ki : Integral gain
///
/// @param kd : Differential gain (used in position control only)
///
/// @param K : Stiffness (used in impedance control only)
///
/// @param B : Damping (used in impedance control only)
///
/// @returns Error codes defined at top of the header
FxError fxSetGains(const unsigned int deviceId, 
			const unsigned int kp, 
			const unsigned int ki, 
			const unsigned int kd, 
			const unsigned int K, 
			const unsigned int B);

/// \brief Send a command to the device.
///
/// @param deviceId is the device ID.
///
/// @param controlMode is the control mode we will use to send this command,
/// defined at the top of the header
///
/// @param value is the value to use for the controlMode. 
/// CmPosition - encoder value/motor angle
/// CmCurrent - current in mA
/// CmVoltage - voltage in mV
/// CmImpedance - encoder value/motor angle
///
/// @returns Error codes defined at top of the header
FxError fxSendMotorCommand(const unsigned int deviceId, const FxControlMode controlMode, const int value);

/// \brief Get the device application type
/// @param deviceId is the device ID
///
/// @returns FxAppType defined at the top of the header

FxAppType fxGetAppType(const unsigned int deviceId);

/// \brief Set the UVLO to the desired value.
///
/// @param deviceId is the device ID
/// 
/// @param mV is the desired UVLO in mV
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxInvalidParam if mV exceeds MIN_UVLO or MAX_UVLO
///          FxSuccess otherwise.
///
FxError fxSetUVLO(const unsigned int deviceId, const unsigned int mV);

/// \brief Send a UVLO request to the specified device. The value is retrieved
/// asyncronously and must be checked by polling fxGetLastReceivedUVLO.
///
/// @param deviceId is the device ID
/// 
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
/// @note The UVLO value is retrieved asyncronously and must be checked by 
/// polling fxGetLastReceivedUVLO.
FxError fxRequestUVLO(const unsigned int deviceId);

/// \brief Check the last UVLO value which was received from the device. This 
/// UVLO value is updated asyncronously by making calls to fxRequestUVLO.
///
/// @param deviceId is the device ID
/// 
/// @returns The last received UVLO in mV. -1 if invalid device.
///
int fxGetLastReceivedUVLO(const unsigned int deviceId);

/// \brief Set the current offset to the desired value.
///
/// @param deviceId is the device ID
/// 
/// @param offset is the current offset. NOT in Amps.
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxInvalidParam if mV exceeds MIN_CURRENT_OFFSET or 
///          	MAX_CURRENT_OFFSET.
///          FxSuccess otherwise.
///
FxError fxSetCurrentOffset(const unsigned int deviceId, const int offset);

/// \brief Send a current offset request to the specified device. The value is 
/// retrieved asyncronously and must be checked by polling 
/// fxGetLastReceivedCurrentOffset.
///
/// @param deviceId is the device ID
/// 
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
/// @note The current offset is retrieved asyncronously and must be checked by 
/// polling fxGetLastReceivedCurrentOffset.
FxError fxRequestCurrentOffset(const unsigned int deviceId);

/// \brief Check the last current offset which was received from the device. 
/// This current offset is updated asyncronously by making calls to 
/// fxRequestCurrentOffset.
///
/// @param deviceId is the device ID
/// 
/// @returns The current offset last received from the device. -1 if invalid 
/// device but proper usage can also return -1.
///
/// @note Please try to ensure you have a valid device before making a call 
/// to this function. 
///
int fxGetLastReceivedCurrentOffset(const unsigned int deviceId);

/// \brief Set the i2t values to the desired values
///
/// @param deviceId is the device ID
/// 
/// @param i2tValsToWrite is the i2tVals struct containing the values to write
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
FxError fxSetI2T(const unsigned int deviceId, const i2tVals i2tValsToWrite);

/// \brief Send an i2t values request to the specified device. The value is 
/// retrieved asyncronously and must be checked by polling 
/// fxGetLastReceivedI2T.
///
/// @param deviceId is the device ID
/// 
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
/// @note The i2t values are retrieved asyncronously and must be checked by 
/// polling fxGetLastReceivedI2T
///
FxError fxRequestI2T(const unsigned int deviceId);

/// \brief Check the last i2t values which were received from the device. 
/// These i2t values are updated asyncronously by making calls to 
/// fxRequestI2T.
///
/// @param deviceId is the device ID
/// 
/// @returns The i2t values last received from the device. Will return a
/// default initialized i2tVals struct if deviceId is invalid.
///
i2tVals fxGetLastReceivedI2T(const unsigned int deviceId);

/// DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
///
/// \brief Find the motor poles
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId is invalid
///          FxSuccess otherwise
///
/// @note DO NOT USE THIS FUNCTION UNLESS YOU KNOW WHAT YOU ARE DOING
FxError fxFindPoles(const unsigned int deviceId);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // DEVICE_WRAPPER_H
