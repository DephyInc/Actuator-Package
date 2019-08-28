#include "findpolesexample.h"
#include "cppFlexSEA.h"

#include <chrono>
#include <thread>
#include <iostream>

using namespace std;
using namespace std::literals::chrono_literals;

void runFindPoles(int devId)
{
    int blockUntilFound = 1;
    findPoles(devId, blockUntilFound);
    return;
}
