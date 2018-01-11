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

#ifndef INC_ANALYZE_GAIT_H
#define INC_ANALYZE_GAIT_H	
	
//****************************************************************************
// Include(s)
//****************************************************************************

#include "exoDef.h"
#include "main.h"
#include "flexsea_global_structs.h"

//****************************************************************************
// Public Function Prototype(s):
//****************************************************************************

void init_analyzegait(void);
void analyzegait_fsm(void);
int16_t get_svm_res(void);
void set_svm_res(void);
	
//****************************************************************************
// Definition(s):
//****************************************************************************

#define MAX_SHANK_VEL_SUM			1000000000

//****************************************************************************
// Structure(s)
//****************************************************************************

//****************************************************************************
// Shared variable(s)
//****************************************************************************

extern int32_t ank_ang_deg;
extern int32_t ank_vel_rad_s;
extern gaitState_t ag_state;
extern int32_t shank_vel;
extern struct diffarr_s min_df_angs;
extern struct diffarr_s min_df_ang_times;
extern struct diffarr_s min_df_swg_angs;
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
