#include "readonly.h"

/*void displayState(ActPackState& state)
{

	//get the Log labels
	char labels[ACTPACK_STRUCT_DEVICE_FIELD_COUNT][ACTPACK_LABEL_MAX_CHAR_LENGTH];
	ActPackGetLabels(labels);
	char dataString[ACTPACK_LABEL_MAX_CHAR_LENGTH+15];//the label plus the colon and data being displayed

	//display everything starting from the state time.  We don't need the id...
	for(int index=ACTPACK_STATE_TIME_POS;index<ACTPACK_STRUCT_DEVICE_FIELD_COUNT;index++)
	{
		strcpy(dataString,"");

		if(strnlen(labels[index],ACTPACK_LABEL_MAX_CHAR_LENGTH)<=6)
		{
			sprintf(dataString,"%s:\t\t%i\n",labels[index],state.deviceData[index]);
		}else if((strnlen(labels[index],ACTPACK_LABEL_MAX_CHAR_LENGTH)<=12))
		{
			sprintf(dataString,"%s:\t%i\n",labels[index],state.deviceData[index]);
		} else
		{
			sprintf(dataString,"%s:\t%i\n",labels[index],state.deviceData[index]);
		}
		cout<<dataString;
	}
	cout<<"\n\n";

}*/

void init_actPackState(ActPackState* state)
{
	//make a temp buffer of all zeros to load
	uint32_t tempDeviceStateBuffer[ACTPACK_STRUCT_DEVICE_FIELD_COUNT];
	memset(tempDeviceStateBuffer,0,sizeof(uint32_t)*ACTPACK_STRUCT_DEVICE_FIELD_COUNT);

	//set struct with the data from the zero buffer
	ActPackSetData(state,tempDeviceStateBuffer,0);

}

void runReadOnly(int devId, bool *shouldQuit)
{
	cout << "\n Running the READ-ALL Demo\n" << endl;
	//
	// Start streaming the data
	//
	if(fxStartStreaming(devId, 200, true) != FxSuccess )
	{
		cout << "Streaming failed ..." << endl;
		return;
	}


	//get the app type
	FxAppType apptype;
	apptype=fxGetAppType(devId);

	switch(apptype)
	{
		case FxActPack:
			cout << "Your device is an ActPack.";
			break;
		case FxExo:
			cout << "Your device is an Exo or ActPack Plus.";
			break;
		case FxNetMaster:
			cout << "Your device is a NetMaster.  ";
			break;
		case FxBMS:
			cout << "Your device is a BMS.  ";
			break;
		default:
			cout << "Unknown device Type.  Exiting... ";
			return;
	}

	cout << "Press any key to continue...\n";
	getchar();

	// Read and display the data
	struct ActPackState actPackState;
	struct ExoState exoState;
	struct NetMasterState netMasterState;
	struct BMSState bmsState;

	init_actPackState(&actPackState);
	//while(!(*shouldQuit))
	int reps=TIME/TIME_STEP;
	for(int index=0;index<reps ;index++)
	{

		this_thread::sleep_for(100ms);
		clearScreen();
		if (apptype == FxActPack)
		{
			fxReadDevice(devId, &actPackState);
			printDevice(&actPackState);
			cout << endl;
		}else if (apptype==FxExo)
		{
			fxReadExoDevice(devId,&exoState);
			printDevice(&exoState);

		}else if (apptype == FxNetMaster)
		{
			fxReadNetMasterDevice(devId, &netMasterState);
			printDevice(&netMasterState);
		} else if (apptype == FxBMS)
		{
			fxReadBMSDevice(devId, &bmsState);
			printDevice(&bmsState);
		}
	}

	fxStopStreaming(devId);
}
