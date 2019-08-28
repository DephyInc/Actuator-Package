//C++ wrapper for the FlexSEA stack

//****************************************************************************
// Include(s)
//****************************************************************************

#include <iostream>

#include <stdlib.h>
#include <cppFlexSEA.h>
#include <chrono>
#include <thread>
#include <string>

using namespace std;

#include "cmd-ActPack.h"

//****************************************************************************
// Public Function Declarations
//****************************************************************************

void printDevice( int devId, int* fieldIds, string* fieldLabels, int n)
{

    if( n == 0 || !fieldIds || !fieldLabels)
    {
        cout << "printDevice: error with inputs" << endl;
        return;
    }

    uint8_t success[MAX_FLEXSEA_VARS];
    int32_t dataBuffer[MAX_FLEXSEA_VARS];
    int count = fxReadDeviceEx(devId, fieldIds, success, dataBuffer, n);


    cout << "FlexSEA Device Data: (" << devId << ")" << endl;
    const char TAB = '\t';
    for(int i = 0; i < n; ++i)
    {
        if(success[i])
            cout << TAB << fieldLabels[i] << " : " << dataBuffer[i] << endl;
        else
        {
            cout << TAB << fieldLabels[i] << " : " << "------" << endl;
        }
    }

    cout << endl;
    fflush(stdout);

    return;
}
