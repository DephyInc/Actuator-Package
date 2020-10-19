#ifndef UTILS_H
#define UTILS_H

#include <iostream>
// Avoiding calls to system would be a good idea
// It's slow, assumes that there is a shell, that these shells use the same nomenclature and poses a security risk
// A cross system approach like ncurses could be nice

void inline clearScreen()
{
	#ifdef _WIN32
	system("cls");
	#elif unix || __unix || __unix__
	system("clear");
	#else
	while(0); // Pass
	#endif
}

#endif //UTILS_H
