#ifndef DATAFORMATS_H
#define DATAFORMATS_H

#define FORMAT_32U	0
#define FORMAT_32S	1
#define FORMAT_16U	2
#define FORMAT_16S	3
#define FORMAT_8U	4
#define FORMAT_8S	5
#define FORMAT_QSTR 6
#define NULL_PTR	7

const int FORMAT_SIZE_MAP[] = {4, 4, 2, 2, 1, 1, -1, -1};

#endif // DATAFORMATS_H
