#ifndef NETMASTER_STRUCT_H
#define NETMASTER_STRUCT_H

#define NUM_NETNODES 8

struct NetNodeState
{
	int accelx;
	int accely;
	int accelz;
	int gyrox;
	int gyroy;
	int gyroz;
	int pressure;
	int status;
};

struct NetMasterState
{
	int netmaster;
	int id;
	int timestamp;
	int genvar[4];
	int status;
	NetNodeState netNode[8];
};



#endif // NETMASTER_STRUCT_H

