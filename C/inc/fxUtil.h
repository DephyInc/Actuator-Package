#ifndef FXUTIL_H
#define FXUTIL_H

#include <iostream>
#include "device_wrapper.h"
#include "exo_struct.h"
#include "actpack_struct.h"
#include "netmaster_struct.h"
#include "bms_struct.h"

using namespace std;

/// \brief Prints ActPack data
///
///@param ActPack is the struct to print
void printDevice(struct ActPackState *actpack);

/// \brief Prints ActPack data
///
///@param ActPack is the struct to print
void printDevice(struct ExoState *exoState);

/// \brief Prints ActPack data
///
///@param ActPack is the struct to print
void printDevice(struct NetMasterState *netMasterState);

void printDevice(struct BMSState *bmsState);

#endif // READONLY_H
