/****************************************************************************
	[Project] FlexSEA: Flexible & Scalable Electronics Architecture
	[Sub-project] 'flexsea-user' User projects
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
	[Lead developper] Luke Mooney, lmooney at dephy dot com.
	[Origin] Based on Jean-Francois Duval's work at the MIT Media Lab 
	Biomechatronics research group <http://biomech.media.mit.edu/>
	[Contributors]
*****************************************************************************
	[This file] user-ex-MotorTestBench: User code running on Execute
*****************************************************************************
	[Change log] (Convention: YYYY-MM-DD | author | comment)
	* 2016-12-06 | jfduval | New release
	*
****************************************************************************/

#ifdef INCLUDE_UPROJ_DPEB21

#ifdef BOARD_TYPE_FLEXSEA_EXECUTE
	
#ifndef INC_ANALYZE_GAIT_H
#define INC_ANALYZE_GAIT_H	
	
//****************************************************************************
// Include(s)
//****************************************************************************

#include "main.h"
#include "flexsea_global_structs.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_analyzegait(void);
void analyzegait_fsm (void);
int get_ank_ang_indx(int32_t);
	
//****************************************************************************
// Definition(s):
//****************************************************************************
#define ARRLEN(x)    ((int32_t)sizeof(x)/(int32_t)sizeof((x)[0])) //ouput the length of an array
#define LIMINDX(x,y) (x = (x<0)?0:((x>=ARRLEN(y)?ARRLEN(y)-1:x))) //limit x to be an index for the array y
#define LIMIT(x,a,b)   (x = (x)<=(a)?(a):((x)>=(b)?(b):(x))) //limit x to be between a and b
#define LININTERP(x1,y1,x2,y2,x)  ((y1)+(((x)-(x1))*((y2)-(y1)))/((x2)-(x1)))    
#define MINVAL(a,b)     ((a<b)?a:b)
#define MAXVAL(a,b)     ((a>b)?a:b)

//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern int16_t ana_indx;
extern int32_t ank_ang_deg;
extern int32_t ank_vel_rad_s;
extern int32_t exo_torq;
extern int32_t ag_state;
extern int32_t shank_vel;
extern struct diffarr_s min_df_angs;
extern struct diffarr_s min_df_ang_times;
extern struct diffarr_s pow_pf_times;
extern int32_t ag_min_df_time;
extern int32_t avg_min_df_ang;
extern int32_t ag_min_df_ang;
extern int32_t ag_max_cpf_ang;
extern int32_t cont_steps;
extern int32_t num_recorded_steps;
extern int32_t ag_step_t;
extern int32_t ag_st;
extern struct diffarr_s ag_step_times;

#endif //INC_ANALYZE_GAIT_H

#endif	//BOARD_TYPE_FLEXSEA_EXECUTE
#endif 	//INCLUDE_UPROJ_DPEB21
