/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-system' System commands & functions
	Copyright (C) 2016 Dephy, Inc. <http://dephy.com/>

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*****************************************************************************
	[Lead developper] Jean-Francois (JF) Duval, jfduval at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] flexsea_global_structs: contains all the data structures
	used across the project
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-10-19 | jfduval | Initial release
	*
****************************************************************************/

#ifndef INC_FLEXSEA_GLOBAL_STRUCT_H
#define INC_FLEXSEA_GLOBAL_STRUCT_H

#ifdef __cplusplus
extern "C" {
#endif

//****************************************************************************
// Include(s)
//****************************************************************************

#include <stdint.h>

//****************************************************************************
// Definition(s):
//****************************************************************************

//****************************************************************************
// Structure(s):
//****************************************************************************

/*Note: most structures will have two versions. The original, aka 'raw'
version has multiple data types, and is used by the different boards.
It includes a sub-structure named decoded_X that contains decoded values
(physical units, not ticks). The decoded values are always int32*/

//Output the length of an array:
#define ARRLEN(x)					((int32_t)sizeof(x)/(int32_t)sizeof((x)[0]))
//Limit x to be an index for the array y
#define LIMINDX(x,y)				(x = (x<0)?0:((x>=ARRLEN(y)?ARRLEN(y)-1:x)))
//Limit x to be between a and b:
#define LIMIT(x,a,b)				(x = (x)<=(a)?(a):((x)>=(b)?(b):(x)))
#define LININTERP(x1,y1,x2,y2,x)	((y1)+(((x)-(x1))*((y2)-(y1)))/((x2)-(x1)))
#define MINVAL(a,b)					((a<b)?a:b)
#define MAXVAL(a,b)					((a>b)?a:b)

//Gains
struct gains_s
{
	 uint16_t g0, g1, g2, g3, g4, g5;
};

struct diffarr_s
{
	int32_t vals[50];
	int32_t curval;
	int32_t indx;
	int32_t curdif;
	int32_t avg;
};

//Generic controller
struct gen_ctrl_s
{
	//Gains:
	struct gains_s gain;

	//Value wanted and setpoint value:
	int32_t actual_val;
	int32_t setpoint_val;
	int32_t actual_vel;
	struct diffarr_s actual_vals;

	//Errors:
	int32_t error;						//Current error
	int32_t error_prev;					//Past error
	int32_t error_sum;					//Integral
	int32_t error_dif;					//Differential

	//trapezoidal time
	int64_t trap_t;
};

//Position controller
struct pos_ctrl_s
{
	//Gains:
	struct gains_s gain;

	//Value wanted and setpoint value:
	int32_t pos;
	int32_t setp;
	int32_t posi;
	int32_t posf;
	int32_t spdm;
	int32_t acc;

	//Errors:
	int32_t error;						//Current error
	int32_t error_prev;					//Past error
	int32_t error_sum;					//Integral
	int32_t error_dif;					//Differential

	//trapezoidal time
	int64_t trap_t;
};

//Main data structure for all the controllers:
struct ctrl_s
{
	uint8_t active_ctrl;
	int32_t pwm;
	struct gen_ctrl_s generic;
	struct gen_ctrl_s current;
	struct pos_ctrl_s position;
	struct gen_ctrl_s impedance;
};

//Encoder:
struct enc_s
{
	int32_t count;
	int32_t count_last;
	int32_t count_dif;
	uint32_t config;
	int32_t vel;
};
//ToDo: only used by Execute's QEI. Will disappear soon.

//Inner structure for the IMU:

struct decoded_xyz_s
{
	 int32_t x;
	 int32_t y;
	 int32_t z;
};

struct xyz_s
{
	 int16_t x;
	 int16_t y;
	 int16_t z;
};

//FlexSEA-Execute:

struct decoded_execute_s
{
	struct decoded_xyz_s gyro;  //deg/s
	struct decoded_xyz_s accel; //mg

	int32_t strain;				//%
	int32_t current;			//mA
	int32_t volt_batt;			//mV
	int32_t volt_int;			//mV
	int32_t temp;				//Celsius x10
	int32_t analog[8];			//mV
};

struct execute_s
{
	struct xyz_s gyro;
	struct xyz_s accel;

	uint16_t strain;
	uint16_t analog[8];
	int32_t current;
	int32_t* enc_ang;
	int32_t* enc_ang_vel;

	uint8_t volt_batt;			//+VB
	uint8_t volt_int;			//+VG
	uint8_t temp;
	uint8_t pwro;
	uint8_t status1;
	uint8_t status2;
	int32_t sine_commut_pwm;

	struct ctrl_s ctrl;

	//Decoded values:
	struct decoded_execute_s decoded;
};

//FlexSEA-Manage:

struct decoded_manage_s
{
	struct decoded_xyz_s gyro;	//deg/s
	struct decoded_xyz_s accel;	//mg

	int32_t analog[8];			//mV
};

struct manage_s
{
	struct xyz_s gyro;
	struct xyz_s accel;

	uint16_t analog[8];
	uint16_t digitalIn;

	uint8_t status1;

	uint8_t sw1;
	uint8_t sampling;

	//Pointer to Battery structure:
	struct battery_s *battPtr;

	//Decoded values:
	struct decoded_manage_s decoded;
};

//FlexSEA-Strain:

struct decoded_strain_s
{
	int32_t strain[6];
};

//Strain - single channel
struct strain_1ch_s
{
	//Config:
	uint8_t offset;
	uint8_t gain;
	uint8_t oref;

	//Raw ADC values:
	uint16_t strain_raw[4];
	uint16_t strain_mem[5];
	uint16_t vo1;
	uint16_t vo2;

	//Filtered value:
	uint16_t strain_filtered;
};

//Strain - 6 channels
struct strain_s
{
	//One structure per channel:
	struct strain_1ch_s ch[6];
	uint8_t compressedBytes[9];
	uint8_t preDecoded;

	//Decoded values:
	struct decoded_strain_s decoded;
};

//FlexSEA-Battery:

struct decoded_battery_s
{
	int32_t voltage;	//mV
	int32_t current;	//mA
	int32_t power;		//mW
	int32_t temp;		//C*10
};

struct battery_s
{
	uint16_t voltage;
	int16_t current;
	uint8_t temp;
	uint8_t pushbutton;
	uint8_t status;

	uint8_t rawBytes[8];

	//Decoded values:
	struct decoded_battery_s decoded;
};

//Special structure for the RIC/NU Knee. 'execute_s' + extra sensors.

struct decoded_ricnu_s
{
	int32_t ext_strain[6];
};

struct ricnu_s
{
	//Execute:
	struct execute_s *ex;

	//Two encoders:
	int32_t enc_motor;
	int32_t enc_joint;

	//Extra sensors (Strain):
	struct strain_s *st;

	//Battery board:
	struct battery_s *batt;

	//Decoded values (ext_strain only)
	struct decoded_ricnu_s decoded;

	int16_t gen_var[6];
};

//FlexSEA-Gossip:

struct decoded_gossip_s
{
	struct decoded_xyz_s gyro;     //deg/s
	struct decoded_xyz_s accel;    //mg
	struct decoded_xyz_s magneto;  //uT
};

struct gossip_s
{
	struct xyz_s gyro;
	struct xyz_s accel;
	struct xyz_s magneto;

	uint16_t capsense[4];

	uint16_t io[2];
	uint8_t status;

	//Decoded values:
	struct decoded_gossip_s decoded;
};

//Commands, tools, specialty, etc.:

//In Control Tool:
struct in_control_s
{
	uint8_t controller;
	int32_t setp;
	int32_t actual_val;
	int32_t error;
	int32_t output;
	int16_t pwm;
	uint8_t mot_dir;
	int16_t current;
	uint16_t combined;	//[CTRL2:0][MOT_DIR][PWM]

	int32_t r[4];
	int32_t w[4];
};

struct user_data_s
{
	int32_t r[4];
	int32_t w[4];
};

//IMU data & config
struct imu_s
{
	 struct xyz_s accel;
	 struct xyz_s gyro;
	 struct xyz_s magneto;
	 uint32_t config;
};

//Generic angular sensor
struct angsense_s
{
	int64_t angs_clks[11]; //clicks
	int64_t vels_cpms[2]; //clicks per ms
	int64_t vels_ctrl_cpms[2];

	int32_t ang_clks; //clicks
	int32_t ang_deg; //degrees

	int32_t vel_cpms; //clicks per ms
	int32_t vel_ctrl_cpms;
	int32_t vel_rpm; //rotations per minute

	//16-bits version for the joint encoder:
	int16_t ang_clks_16b;
	int16_t vel_cpms_16b;
};

//AS504x Magnetic encoders:
struct as504x_s
{
	struct diffarr_s raw_angs_clks;
	struct diffarr_s raw_vels_cpms;
	int32_t filt_vel_cpms;

	int32_t signed_ang;
	int32_t signed_ang_vel;

	int32_t ang_abs_clks; 			//absolute (0-16383) angle in clicks
	int32_t ang_comp_clks;			//compensated absolute angle in clicks
	int32_t ang_comp_clks_for_cur;	//compensated absolute angle in clicks
	int32_t num_rot; 				//number of full encoder rotations

	struct angsense_s raw;
	struct angsense_s filt;
	int32_t last_angtimer_read;
	int32_t counts_since_last_ang_read;
	int32_t last_ang_read_period;
	int32_t samplefreq; 			//sampling frequency of the sensor
};

//circular buffer
#define CIRCBUFFLOATLEN 10
struct circbuf_float_s
{
	float x[CIRCBUFFLOATLEN];
	int16_t i;
	float curval;
};

//filter
struct filt_float_s
{
	struct circbuf_float_s x;
	struct circbuf_float_s y;
	int16_t cutoff;
	int16_t cutoff_indx;
	int16_t cntr;
	float newvalsum;
	float curval;
	float curdiff;
};

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern struct execute_s exec1, exec2, exec3, exec4;
extern struct ricnu_s ricnu_1;
extern struct manage_s manag1, manag2;
extern struct strain_s strain1;
extern struct in_control_s in_control_1;
extern struct gossip_s gossip1, gossip2;
extern struct battery_s batt1;
extern struct user_data_s user_data_1;

//****************************************************************************
// Prototype(s):
//****************************************************************************

void initializeGlobalStructs();
void init_diffarr(struct diffarr_s *);
void update_diffarr(struct diffarr_s *, int32_t, int32_t);
int32_t get_diffarr(struct diffarr_s *, int32_t);
int32_t get_diffarr_elmnt(struct diffarr_s *, int32_t);
void update_diffarr_avg(struct diffarr_s *, int32_t);

void init_circbuf_float(struct circbuf_float_s *);
void update_circbuf_float(struct circbuf_float_s *, float);
float get_circbuf_float_val(struct circbuf_float_s *, int16_t);
void init_filt_float(struct filt_float_s *, int16_t);
void update_filt_float(struct filt_float_s *, float);
void update_filt_float_cutoff(struct filt_float_s *, int16_t);

#ifdef __cplusplus
}
#endif

#endif	//INC_FLEXSEA_GLOBAL_STRUCT_H
