#ifndef TEST_ALL_FX_USER_H
#define TEST_ALL_FX_USER_H

#include "unity.h"
#include "../inc/flexsea_cmd_user.h"

#define TEST_PL_LEN		4
#define FILLER			0

void prepTxCmdTest(void);
void flexsea_user_test(void);

//Prototypes for public functions defined in individual test files:
void test_ankle2dof(void);

#endif	//TEST_ALL_FX_SYSTEM_H
