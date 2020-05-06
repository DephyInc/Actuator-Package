#ifndef READONLY_H
#define READONLY_H

struct ActPackState;

void runReadAll(int devId, bool* shouldQuit);
void displayState(ActPackState &exoState);

#endif // READONLY_H
