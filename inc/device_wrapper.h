#ifndef DEVICE_WRAPPER_H
#define DEVICE_WRAPPER_H

#include <stdbool.h>
#include <string>
#include "actpack_struct.h"
#include "netmaster_struct.h"
#include "cellscreener_struct.h"
#include "battcycler_struct.h"
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

} FxError;

typedef enum fxControlMode
{
	FxPosition	= 0, //Position - Send a position setpoint
	FxVoltage	= 1, //Voltage - Open Control Command
	FxCurrent	= 2, //Current - Send a current Setpoint command
	FxImpedance	= 3, //Impedance - Send an impedance command. Position setpoints but with stiffness and damping coefficients
	FxNone		= 4, //No controller type. Shutoff command.
	FxCustom	= 5,
	FxMeasRes	= 6,
	FxStalk		= 7, //Send an stalking command. It uses the position controller to stalk an ankle angle at a certain distance

} FxControlMode;

typedef enum fxAppType
{
	FxInvalidApp = -1,
	FxActPack = 0,
	FxExo,
	FxNetMaster,
	FxBMS,
	FxHabsolute,
	FxCellScreener,
	FxBattCycler

} FxAppType;

struct ActPackState;	//Contains Actuator Pack Data
struct NetMasterState;	//Contains Network Data from NetNodes
struct BMSState;		//Contains Battery Management System Data
struct HabsoluteState;	//Contains Ankle position data
struct CellScreenerState;
struct BattCyclerState;

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
/// @param idArray is an array to hold the returned device IDs. The return value
/// of this function is the number of connected FlexSEA devices (numDevices). 
/// On return each element of the array up till numDevices will contain a valid
/// device ID.
/// 
/// @param size is the size of the idarray. Should be large enough to contain 
/// device IDs for all devices you plan to use at once, or FX_MAX_DEVICES.
///
/// @returns number of connected FlexSEA devices
///
/// @note idArray should have at least as many elements as FlexSEA devices used.
int fxGetDeviceIds(int* const idArray, const unsigned int size);

/// \brief Start streaming data from a FlexSEA device and optionally log the
/// streamed data. The data logger can impact performance if you are sending 
/// many commands in quick succession.
///
/// @param deviceId is the device ID 
/// 
/// @param shouldLog If set true, the program logs all received data to a file.
/// Enabling the data logging can impact performance if you are sending many
/// commands in quick succession.
/// 
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
///
/// @note The data logger can impact performance if you are sending many 
/// commands in quick succession.
FxError fxStartStreaming(const unsigned int deviceId, 
			const unsigned int frequency,
			const bool shouldLog);

/// \brief Stop streaming data from a FlexSEA device.
/// 
/// @param deviceId is the device ID 
/// 
/// @returns Error codes defined at top of the header
FxError fxStopStreaming(const unsigned int deviceId);

/// \brief check if streaming data from a FlexSEA device.
///
/// @param deviceId is the device ID
///
/// @returns true if streaming.  false if not streaming
bool fxIsStreaming(const unsigned int deviceId);
/// \brief Read the most recent data from a streaming FlexSEA device stream.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not an ActPack
///          device.
FxError fxReadDevice(const unsigned int deviceId, ActPackState* readData);

/// \brief Read the most recent data from a streaming FlexSEA NetMaster device.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not a NetMaster
///          device.
FxError fxReadNetMasterDevice(const unsigned int deviceId, NetMasterState* readData);

/// \brief Read the most recent data from a streaming FlexSEA BMS device.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not a BMS device.
FxError fxReadBMSDevice(const unsigned int deviceId, BMSState* readData);

/// \brief Read the most recent data from a streaming FlexSEA Habsolute device.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not a Habsolute device.
FxError fxReadHabsoluteDevice(const unsigned int deviceId, HabsoluteState* readData);

/// \brief Read the most recent data from a streaming FlexSEA CellScreener device.
/// Must call fxStartStreaming before calling this.
///
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not a CellScreener device.
FxError fxReadCellScreenerDevice(const unsigned int deviceId, CellScreenerState* readData);

/// \brief Read the most recent data from a streaming FlexSEA BattCycler device.
/// Must call fxStartStreaming before calling this.
///
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not a BattCycler device.
FxError fxReadBattCyclerDevice(const unsigned int deviceId, BattCyclerState* readData);

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

/// \brief Read all exo data from a streaming FlexSEA BMS device.
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
int fxReadBMSDeviceAll(const unsigned int deviceId, 
			BMSState* readData, 
			const unsigned int n);

/// \brief Read all exo data from a streaming FlexSEA Habsolute device.
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
int fxReadHabsoluteDeviceAll(const unsigned int deviceId, 
			HabsoluteState* readData, 
			const unsigned int n);

/// \brief Read all data from a streaming FlexSEA CellScreener device.
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
int fxReadCellScreenerDeviceAll(const unsigned int deviceId,
							 CellScreenerState* readData,
							 const unsigned int n);

/// \brief Read all data from a streaming FlexSEA BattCycler device.
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
int fxReadBattCyclerDeviceAll(const unsigned int deviceId,
								BattCyclerState* readData,
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
/// @param ff : Feed Forward gain
///
/// @returns Error codes defined at top of the header
FxError fxSetGains(const unsigned int deviceId, 
			const unsigned int kp,
			const unsigned int ki,
			const unsigned int kd,
			const unsigned int K,
			const unsigned int B,
			const unsigned int ff);

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

/// \brief
///
/// @param flag is the value of the flag you wish to set
///
/// @param time is duration of time this flag should be
/// present in millisecond.
FxError fxSendEventFlags(int flag, int time);

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

/// \brief Sends new Ankle Torque points to device (Read/Write)
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId is invalid
/////          FxSuccess otherwise
///
FxError fxSetAnkleTorquePoints(const unsigned int deviceId, int16_t *newAnkleTorque, const uint8_t controller, const uint8_t points);

/// \brief Reads new Ankle Torque points to device (pure read)
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId is invalid
/////          FxSuccess otherwise
///
FxError fxReadAnkleTorquePoints(const unsigned int deviceId, const uint8_t points);

/// \brief Returns the last points read by the stack
///
/// @param deviceId is the device ID
///
/// @returns pointer to array
///
int16_t * fxGetLastReceivedAnkleTorquePoints(const unsigned int deviceId);

/// \brief Activates target bootloader
///
/// @param
/// deviceId - device ID
/// target - target bootloader
///
/// @returns FxInvalidDevice if deviceId is invalid
/////          FxSuccess otherwise
///
FxError fxActivateBootloader(const unsigned int deviceId, const uint8_t target);

/// \brief Returns target bootloader status
///
/// @param
/// deviceId - device ID
///
/// @returns true if activated, false if not.
///
FxError fxIsBootloaderActivated(const unsigned int deviceId);

///
/// \param deviceId The ID of the device
/// \param isValid Will be true if the gain is valid
/// \param highestTimingGain the highest gain recived since power on of device
/// \return
double fxGetTimingGain(const unsigned int deviceId, bool *isValid, double *highestTimingGain);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // DEVICE_WRAPPER_H
