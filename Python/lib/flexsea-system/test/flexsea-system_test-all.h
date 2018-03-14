#ifndef TEST_ALL_FX_SYSTEM_H
#define TEST_ALL_FX_SYSTEM_H

//#include "main.h"
#include "unity.h"
#include "../inc/flexsea_system.h"

#define TEST_PL_LEN		4
#define FILLER			0

extern uint8_t test_tmpPayload[PAYLOAD_BUF_LEN];
extern uint8_t test_transferBuf[COMM_STR_BUF_LEN];
extern uint8_t test_cmdCode, test_cmdType;
extern uint16_t test_len;

void prepTxCmdTest(void);
void flexsea_system_test(void);

//Prototypes for public functions defined in individual test files:
void test_flexsea_system(void);
void test_flexsea_cmd_control_1(void);
void test_flexsea_cmd_control_2(void);
void test_flexsea_cmd_data(void);
void test_flexsea_cmd_external(void);
void test_flexsea_cmd_sensors(void);

#endif	//TEST_ALL_FX_SYSTEM_H
