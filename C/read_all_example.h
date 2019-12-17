#ifndef READ_ALL_EXAMPLE_H
#define READ_ALL_EXAMPLE_H

typedef struct actPackState ActPackState;

void runReadAll(int devId, bool* shouldQuit);
void displayState(ActPackState &exoState);

#endif // READ_ALL_EXAMPLE_H
