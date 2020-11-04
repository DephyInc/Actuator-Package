#ifndef READONLY_H
#define READONLY_H


#include "fxUtil.h"

#include <chrono>
#include <thread>
#include <iostream>
#include "utils.h"
#include "device_wrapper.h"
#include "exo_wrapper.h"

#define TIME_STEP .1 //in seconds
#define TIME 8

using namespace std;
using namespace std::literals::chrono_literals;

void runReadOnly(int devId, bool* shouldQuit);


#endif // READONLY_H
