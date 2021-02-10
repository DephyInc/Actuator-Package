/************************************************************
 
TOP-SECRET DEPHY EXO FUNCTIONS

Do not send this to external clients

*************************************************************/

#ifndef EXO_WRAPPER_H
#define EXO_WRAPPER_H

#include <stdbool.h>
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

///Enum to identify led  color on exo batter
typedef enum fxBatteryColor
{
	fxNoColor = 	-1,	///color unknown
	fxGreen=	0,		///Green LED
	fxYellow=	1,		///Yellow LED
	fxRed=		2		///Red LED

} FxBatteryColor;

struct ExoState;

////////////////////// For UTTs //////////////////////////////
#define UTT_NUM_VALS 15

#define UTT_0_MIN 42
#define UTT_0_MAX 42
#define UTT_1_MIN -10000
#define UTT_1_MAX 10000
#define UTT_2_MIN -10000
#define UTT_2_MAX 10000
#define UTT_3_MIN -10000
#define UTT_3_MAX 10000
#define UTT_4_MIN -10000
#define UTT_4_MAX 10000
#define UTT_5_MIN -10000
#define UTT_5_MAX 10000
#define UTT_6_MIN -10000
#define UTT_6_MAX 10000
#define UTT_7_MIN -10000
#define UTT_7_MAX 10000
#define UTT_8_MIN -10000
#define UTT_8_MAX 10000
#define UTT_9_MIN -10000
#define UTT_9_MAX 10000
#define UTT_10_MIN -10000
#define UTT_10_MAX 10000
#define UTT_11_MIN -10000
#define UTT_11_MAX 10000
#define UTT_12_MIN -10000
#define UTT_12_MAX 10000
#define UTT_13_MIN -10000
#define UTT_13_MAX 10000
#define UTT_14_MIN -10000
#define UTT_14_MAX 10000
static const int UTT_VAL_LIMITS[UTT_NUM_VALS][2] {{UTT_0_MIN,UTT_0_MAX},
 						{UTT_1_MIN,UTT_1_MAX},
						{UTT_2_MIN,UTT_2_MAX},
						{UTT_3_MIN,UTT_3_MAX},
						{UTT_4_MIN,UTT_4_MAX},
						{UTT_5_MIN,UTT_5_MAX},
						{UTT_6_MIN,UTT_6_MAX},
						{UTT_7_MIN,UTT_7_MAX},
						{UTT_8_MIN,UTT_8_MAX},
						{UTT_9_MIN,UTT_9_MAX},
						{UTT_10_MIN,UTT_10_MAX},
						{UTT_11_MIN,UTT_11_MAX},
						{UTT_12_MIN,UTT_12_MAX},
						{UTT_13_MIN,UTT_13_MAX},
						{UTT_14_MIN,UTT_14_MAX}};

/// \brief Read the most recent data from a streaming FlexSEA Exo stream.
/// Must call fxStartStreaming before calling this.
/// 
/// @param deviceId is the device ID of the device to read from.
///
/// @param readData contains the most recent data from the device
///
/// @returns FxNotStreaming if device is not streaming when this is called.
///          FxInvalidDevice if deviceId is invalid or is not an Exo device.
FxError fxReadExoDevice(const unsigned int deviceId, ExoState* readData);

/// \brief Read all exo data from a streaming FlexSEA device stream.
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
int fxReadExoDeviceAll(const unsigned int deviceId, 
			ExoState* readData, 
			const unsigned int n);

// \brief Get the Exo side (Left or Right). Only valid for an Exo device.
///
/// @param deviceId is the device ID
///
/// @returns FxExoSide defined at the top of the header. FxInvalidSide if 
/// not an Exo device or deviceId is invalid.
FxExoSide fxGetSide(const unsigned int deviceId);

/// \brief Run the belt calibration routine
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId is invalid
///          FxSuccess otherwise
FxError fxRunBeltCalibration(const unsigned int deviceId);

/// \brief Enable augmentation in an exo device. Enabled by default.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise
FxError fxEnableAugmentation(const unsigned int deviceId);


/// \brief Disable augmentation in an exo device. Enabled by default.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise
FxError fxDisableAugmentation(const unsigned int deviceId);

/// \brief Set the UTT values to the desired values.
///
/// @param deviceId is the device ID
/// 
/// @param uttToSet is an array of UTT values to set. Up to UTT_NUM_VALS
///
/// @param n is the size of the uttToSet array
///
/// @param singleUTTIndex is the index for a single value write. -1 = full array.
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxInvalidParam if any UTTs exceed the thresholds defined at the
///              top of this header.
///          FxSuccess otherwise.
///
/// @note Only UTTs up to UTT_NUM_VALS will be set.
///
FxError fxSetUTT(const unsigned int deviceId, 
			const int* uttToSet,
			const unsigned int n,
			char singleUTTIndex);

/// \brief Save the UTT values to the desired values. This involves writing
/// to the device's non-volatile memory.
///
/// @param deviceId is the device ID
/// 
/// @param uttToSave is an array of UTT values to save. Up to UTT_NUM_VALS
///
/// @param n is the size of the uttToSave array
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxInvalidParam if any UTTs exceed the thresholds defined at the
///              top of this header.
///          FxSuccess otherwise.
///
/// @note Only UTTs up to UTT_NUM_VALS will be saved.
///
FxError fxSaveUTT(const unsigned int deviceId, 
			const int* uttToSave,
			const unsigned int n);

/// \brief Send a UTT values request to the specified device. The value is 
/// retrieved asyncronously and must be checked by polling 
/// fxGetLastReceivedUTT.
///
/// @param deviceId is the device ID
/// 
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
/// @note The i2t values are retrieved asyncronously and must be checked by 
/// polling fxGetLastReceivedUTT.
///
FxError fxRequestUTT(const unsigned int deviceId);

/// \brief Check the last UTT values which were received from the device. 
/// These UTT values are updated asyncronously by making calls to 
/// fxRequestUTT.
///
/// @param deviceId is the device ID
///
/// @param readUTTBuffer is an array of UTT values to save. Ideally at least
/// UTT_NUM_VALS in size.
///
/// @param n is the size of the uttToSave array. Ideally at least UTT_NUM_VALS.
///
/// 
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
/// @note Only UTTs up to UTT_NUM_VALS will be read.
///
FxError fxGetLastReceivedUTT(const unsigned int deviceId, 
				int* readUTTBuffer,
				const unsigned int n);

/// \brief Send a start training command to the specified exo device.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
FxError fxStartTraining(const unsigned int deviceId);

/// \brief Send a stop training command to the specified exo device.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
FxError fxStopTraining(const unsigned int deviceId);

/// \brief Send a start substate training command to the specified exo device.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
FxError fxStartSubTraining(const unsigned int deviceId);

/// \brief Send a stop substate training command to the specified exo device.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
FxError fxStopSubTraining(const unsigned int deviceId);

/// \brief Set the prog walk params to the requested values
///
/// @param deviceId is the device ID
///
/// @param FxExoControllerType defined at the top of the header
///
/// @param FxExoTrainingType defined at the top of the header
///
/// @param FxExoControllerMode defined at the top of the header
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxInvalidParam if any prog walk params are invalid
///          FxSuccess otherwise.
///
FxError fxSetProgWalkParams(const unsigned int deviceId,
                               const FxExoControllerType exoControllerType,
                               const FxExoTrainingType exoTrainingType,
                               const FxExoControllerMode exoControlMode);

/// \brief Send a prog walk parameters request to the specified device. The
/// parameters are retrieved asyncronously and must be checked by polling
/// fxGetLastReceivedProgWalkParams.
///
/// @param deviceId is the device ID
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxSuccess otherwise.
///
/// @note The prog walk parameters are retrieved asyncronously and must be checked by
/// polling fxGetLastReceivedProgWalkParams.
///
FxError fxRequestProgWalkParams(const unsigned int deviceId);

/// \brief Check the last prog walk parameters which were received from the
/// device. These parameters are updated asyncronously by making calls to
/// fxRequestProgWalkParams.
///
/// @param deviceId is the device ID
///
/// @param FxExoControllerType defined at the top of the header
///
/// @param FxExoTrainingType defined at the top of the header
///
/// @param FxExoControllerMode defined at the top of the header
///
/// @returns FxInvalidDevice if deviceId does not correspond an exo device.
///          FxFailure if any of the prog walk params are invalid
///          FxSuccess otherwise.
///
FxError fxGetLastReceivedProgWalkParams(const unsigned int deviceId,
                                       FxExoControllerType* exoControllerType,
                                       FxExoTrainingType* exoTrainingType,
                                       FxExoControllerMode* exoControlMode);

///
/// \param deviceId is the device ID
/// \return The percentage of battery life remaining
double fxGetBatteryLife(const unsigned int deviceId);

///
/// \param deviceId  is the device ID
/// \return the current color code of the Exo
fxBatteryColor fxGetBatteryColor(const unsigned int deviceId);

///
/// \param movement the movement parameter to translate
/// \return the string corresponding to the movement enumeration
const char* fxGetMovement(int movement);

#ifdef __cplusplus
} // extern "C"
#endif

#endif // EXO_WRAPPER_H
