/************************************************************

TOP-SECRET DEPHY EXO FUNCTIONS

Do not send this to external clients

*************************************************************/

#ifndef EXO_WRAPPER_H
#define EXO_WRAPPER_H

#include "device_wrapper.h"

#define TOTAL_DEFINED_MOVEMENTS 5 ///Total movements that can be defined by the exo such as walking, running etc.

#ifdef __cplusplus
extern "C"
{
#endif

typedef enum fxExoSide
{
	FxInvalidSide = -1,
	FxLeft = 0,
	FxRight

} FxExoSide;

typedef enum fxExoControllerType
{
	FxInvalidControllerType = -1,
	FxStable,
	FxExperimental

} FxExoControllerType;

typedef enum fxExoTrainingType
{
	FxInvalidTrainingType = -1,
	FxWalkingOnly,
	FxWalkingAndRunning

} FxExoTrainingType;

typedef enum fxExoControllerMode
{
	FxInvalidControllerMode = -1,
	FxFullController,
	FxDemoController

} FxExoControllerMode;

///Enum to identify led color on exo battery
typedef enum fxBatteryColor
{
	fxNoColor = -1,   ///Color unknown
	fxGreen = 0,    ///Green LED
	fxYellow = 1,    ///Yellow LED
	fxRed = 2        ///Red LED

} FxBatteryColor;

typedef enum fxTrainingState
{
	fxLoadTrainingData = 0,    ///Training data is loading
	fxRunTrainings = 1,    ///Training is currently running
	fxSaveTrainingData = 2,    ///Training data is being saved
	fxFinishedTraining = 3        ///Training is complete

} FxTrainingState;

struct EB5xState;

////////////////////// For UTTs //////////////////////////////

#define UTT_NUM_VALS 15

#define UTT_0_MIN 42
#define UTT_0_MAX 42
#define UTT_1_MIN (-10000)
#define UTT_1_MAX 10000
#define UTT_2_MIN (-10000)
#define UTT_2_MAX 10000
#define UTT_3_MIN (-10000)
#define UTT_3_MAX 10000
#define UTT_4_MIN (-10000)
#define UTT_4_MAX 10000
#define UTT_5_MIN (-10000)
#define UTT_5_MAX 10000
#define UTT_6_MIN (-10000)
#define UTT_6_MAX 10000
#define UTT_7_MIN (-10000)
#define UTT_7_MAX 10000
#define UTT_8_MIN (-10000)
#define UTT_8_MAX 10000
#define UTT_9_MIN (-10000)
#define UTT_9_MAX 10000
#define UTT_10_MIN (-10000)
#define UTT_10_MAX 10000
#define UTT_11_MIN (-10000)
#define UTT_11_MAX 10000
#define UTT_12_MIN (-10000)
#define UTT_12_MAX 10000
#define UTT_13_MIN (-10000)
#define UTT_13_MAX 10000
#define UTT_14_MIN (-10000)
#define UTT_14_MAX 10000

static const int UTT_VAL_LIMITS[UTT_NUM_VALS][2]{{UTT_0_MIN,  UTT_0_MAX},
												 {UTT_1_MIN,  UTT_1_MAX},
												 {UTT_2_MIN,  UTT_2_MAX},
												 {UTT_3_MIN,  UTT_3_MAX},
												 {UTT_4_MIN,  UTT_4_MAX},
												 {UTT_5_MIN,  UTT_5_MAX},
												 {UTT_6_MIN,  UTT_6_MAX},
												 {UTT_7_MIN,  UTT_7_MAX},
												 {UTT_8_MIN,  UTT_8_MAX},
												 {UTT_9_MIN,  UTT_9_MAX},
												 {UTT_10_MIN, UTT_10_MAX},
												 {UTT_11_MIN, UTT_11_MAX},
												 {UTT_12_MIN, UTT_12_MAX},
												 {UTT_13_MIN, UTT_13_MAX},
												 {UTT_14_MIN, UTT_14_MAX}};

/// \brief Read the most recent data from a streaming FlexSEA Exo stream.
/// Must call fxStartStreaming before calling this.
///
/// \param deviceId is the device ID of the device to read from.
///
/// \param readData contains the most recent data from the device
///
/// \returns FxNotStreaming if device is not streaming when this is called.
///			FxInvalidDevice if deviceId is invalid or is not an Exo device.
FxError fxReadExoDevice(unsigned int deviceId, EB5xState *readData);

/// \brief Read all exo data from a streaming FlexSEA device stream.
/// Must call fxStartStreaming before calling this.
///
/// \param deviceId is the device ID of the device to read from.
///
/// \param readData is an array of size n which contains read results
///
/// \param n is the size of the readData y
///
/// \returns The actual number of entries read. You will probably need
/// to use this number.
///
/// \note Will only fill readData array up to read data queue size.
int fxReadExoDeviceAll(unsigned int deviceId,
					   EB5xState *readData,
					   unsigned int n);

// \brief Get the Exo side (Left or Right). Only valid for an Exo device.
///
/// \param deviceId is the device ID
///
/// \returns FxExoSide defined at the top of the header. FxInvalidSide if
/// not an Exo device or deviceId is invalid.
FxExoSide fxGetSide(unsigned int deviceId);

/// \brief Run the belt calibration routine
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId is invalid
///			FxSuccess otherwise
FxError fxRunBeltCalibration(unsigned int deviceId);

/// \brief Set the UTT values to the desired values.
///
/// \param deviceId is the device ID
///
/// \param uttToSet is an array of UTT values to set. Up to UTT_NUM_VALS
///
/// \param n is the size of the uttToSet array
///
/// \param singleUTTIndex is the index for a single value write. -1 = full array.
///
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxInvalidParam if any UTTs exceed the thresholds defined at the
///			top of this header.
///			FxSuccess otherwise.
///
/// \note Only UTTs up to UTT_NUM_VALS will be set.
///
FxError fxSetUTT(unsigned int deviceId,
				 int *uttToSet,
				 unsigned int n,
				 char singleUTTIndex);

/// \brief Save the UTT values to the desired values. This involves writing
/// to the device's non-volatile memory.
///
/// \param deviceId is the device ID
///
/// \param uttToSave is an array of UTT values to save. Up to UTT_NUM_VALS
///
/// \param n is the size of the uttToSave array
///
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxInvalidParam if any UTTs exceed the thresholds defined at the
///			top of this header.
///			FxSuccess otherwise.
///
/// \note Only UTTs up to UTT_NUM_VALS will be saved.
///
FxError fxSaveUTT(unsigned int deviceId,
				  const int *uttToSave,
				  unsigned int n);

/// @brief Saves the UTT's currently on the device to EEPROM
/// @param deviceId the ID of the device
/// @return FxInvalidDevice if deviceId does not correspond an exo device.
///			FxInvalidParam if any UTTs exceed the thresholds defined at the
///			top of this header.
///			FxSuccess otherwise.
FxError fxSaveUTTToMemory(const unsigned int deviceId);

/// \brief Send a UTT values request to the specified device. The value is
/// retrieved asynchronously and must be checked by polling
/// fxGetLastReceivedUTT.
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
///
/// \note The i2t values are retrieved asynchronously and must be checked by
/// polling fxGetLastReceivedUTT.
///
FxError fxRequestUTT(unsigned int deviceId);

/// \brief Check the last UTT values which were received from the device.
/// These UTT values are updated asynchronously by making calls to
/// fxRequestUTT.
///
/// \param deviceId is the device ID
///
/// \param readUTTBuffer is an array of UTT values to save. Ideally at least
/// UTT_NUM_VALS in size.
///
/// \param n is the size of the uttToSave array. Ideally at least UTT_NUM_VALS.
///
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
///
/// \note Only UTTs up to UTT_NUM_VALS will be read.
///
FxError fxGetLastReceivedUTT(unsigned int deviceId,
							 int *readUTTBuffer,
							 unsigned int n);

/// \brief Send a start training command to the specified exo device.
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
///
FxError fxStartTraining(unsigned int deviceId);

/// \brief Request device use saved training data.  When this is set, boots will not train at
/// startup.
/// \param deviceId the ID of the device
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
FxError fxUseSavedTraining(unsigned int deviceId);

/// \brief Request device NOT use saved training data.  When this is set, boots will train at
/// startup.
/// \param deviceId The ID of the device
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
FxError fxDoNotUseSaveTraining(unsigned int deviceId);

/// \brief Get the total steps remaining until training is complete.  -1 if data incomplete.
/// \param deviceId The ID of the device
/// \param trainingStepsRemaining
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
FxError fxGetStepsRemaining(unsigned int deviceId, int *trainingStepsRemaining);


/// \brief Check if device is currently using saved training data.  If true, device
/// will not run training at startup.
/// \param deviceId The ID of the device
/// \param usingSavedTrainingData will be true of saved training data will be used on startup.
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
FxError fxIsUsingSavedTrainingData(unsigned int deviceId, bool *usingSavedTrainingData);

/// \brief Request updated training data from the device.  Training data is asynchronous
/// and will only update on request.
/// \param deviceId the ID of the device
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
FxError fxUpdateTrainingData(unsigned int deviceId);

/// \brief Get the last state of training sent by the device
/// \param deviceId the ID of the device
/// \param trainingState the last training state transmitted by the device
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxSuccess otherwise.
FxError fxGetTrainingState(unsigned int deviceId, fxTrainingState *trainingState);

/// \brief Check the last prog walk parameters which were received from the
/// device. These parameters are updated asyncronously by making calls to
/// fxRequestProgWalkParams.
///
/// \param deviceId is the device ID
///
/// \param FxExoControllerType defined at the top of the header
///
/// \param FxExoTrainingType defined at the top of the header
///
/// \param FxExoControllerMode defined at the top of the header
///
/// \returns FxInvalidDevice if deviceId does not correspond an exo device.
///			FxFailure if any of the prog walk params are invalid
///			FxSuccess otherwise.
///
FxError fxGetLastReceivedProgWalkParams(unsigned int deviceId,
										FxExoControllerType *exoControllerType,
										FxExoTrainingType *exoTrainingType,
										FxExoControllerMode *exoControlMode);

///
/// \param deviceId is the device ID
/// \return The percentage of battery life remaining
double fxGetBatteryLife(unsigned int deviceId);

///
/// \param deviceId  is the device ID
/// \return the current color code of the Exo
fxBatteryColor fxGetBatteryColor(unsigned int deviceId);

///
/// \param movement the movement parameter to translate
/// \return the string corresponding to the movement enumeration
const char *fxGetMovement(int movement);

/// \brief Send a Exo Control Read request to the specified device. The value is
/// retrieved asynchronously and must be checked by polling
/// fxGetLastReceivedExoControl.
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond to a connected device.
///			FxSuccess otherwise.
///
/// \note The values are retrieved asynchronously and must be checked by
/// polling fxGetLastReceivedExoControl
///
FxError fxRequestExoControl(unsigned int deviceId);

/// \brief Send a Exo Control Power On Write to the specified device. The device will
/// reply, and the value is retrieved asynchronously and must be checked by polling
/// fxGetLastReceivedExoControl (if desired)
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond to a connected device.
///			FxSuccess otherwise.
///
/// \note The values are retrieved asynchronously and must be checked by
/// polling fxGetLastReceivedExoControl
///
FxError fxSetExoControlPowerOn(unsigned int deviceId);

/// \brief Send a Exo Control Power Off Write to the specified device. The device will
/// reply, and the value is retrieved asynchronously and must be checked by polling
/// fxGetLastReceivedExoControl (if desired)
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond to a connected device.
///			FxSuccess otherwise.
///
/// \note The values are retrieved asynchronously and must be checked by
/// polling fxGetLastReceivedExoControl
///
FxError fxSetExoControlPowerOff(unsigned int deviceId);

/// \brief Send a Exo Control Trial Start Write to the specified device. The device will
/// reply, and the value is retrieved asynchronously and must be checked by polling
/// fxGetLastReceivedExoControl (if desired)
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond to a connected device.
///			FxSuccess otherwise.
///
/// \note The values are retrieved asynchronously and must be checked by
/// polling fxGetLastReceivedExoControl
///
FxError fxSetExoControlTrialStart(unsigned int deviceId);

/// \brief Send a Exo Control Trial Stop Write to the specified device. The device will
/// reply, and the value is retrieved asynchronously and must be checked by polling
/// fxGetLastReceivedExoControl (if desired)
///
/// \param deviceId is the device ID
///
/// \returns FxInvalidDevice if deviceId does not correspond to a connected device.
///			FxSuccess otherwise.
///
/// \note The values are retrieved asynchronously and must be checked by
/// polling fxGetLastReceivedExoControl
///
FxError fxSetExoControlTrialStop(unsigned int deviceId);

/// \brief Get the last Exo Control data read from the device
/// \param deviceId The ID of the device
/// \returns struct exoCommandStruct
struct exoCommandStruct fxGetLastReceivedExoControl(const unsigned int deviceId);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // EXO_WRAPPER_H
