cmake_minimum_required(VERSION 2.8.3) 
project(flexsea_c_scripts)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include(${CMAKE_CURRENT_SOURCE_DIR}/../fx_plan_stack/plan_definitions.cmake)

include_directories(
	.
	${CMAKE_CURRENT_SOURCE_DIR}/../include
	${CMAKE_CURRENT_SOURCE_DIR}/../fx_plan_stack/include/flex_lib
	${CMAKE_CURRENT_SOURCE_DIR}/../fx_plan_stack/include/flexseastack
	${CMAKE_CURRENT_SOURCE_DIR}/../fx_plan_stack/serial/include
	${CMAKE_CURRENT_SOURCE_DIR}/../flexsea-core/flexsea-comm/inc
	${CMAKE_CURRENT_SOURCE_DIR}/../flexsea-core/flexsea-dephy/inc
	${CMAKE_CURRENT_SOURCE_DIR}/../flexsea-core/flexsea-shared/inc
	${CMAKE_CURRENT_SOURCE_DIR}/../flexsea-core/flexsea-system/inc
	${CMAKE_CURRENT_SOURCE_DIR}/../flexsea-core/flexsea-projects/inc
	${CMAKE_CURRENT_SOURCE_DIR}/../flexsea-core/flexsea-projects/ActPack/inc
)

set(CSCRIPT_SRCS
	main.cpp
	cppFlexSEA.cpp
	read_all_example.cpp
	open_speed_example.cpp
	current_control.cpp
	hold_position_example.cpp
	findpolesexample.cpp
	two_dev_position_example.cpp
	leaderfollower.cpp
	utils.h
)

add_executable(main ${CSCRIPT_SRCS})

# only look for a freshly built plan stack library since we're already set up to compile this find_program
# should not be an issues to have a freshly compiled plan stack to prevent confusion
find_library(fx_plan_stack_LIBRARY fx_plan_stack_static ${CMAKE_CURRENT_SOURCE_DIR}/../fx_plan_stack/build/libs)

# link plan stack library to our application
target_link_libraries(main ${fx_plan_stack_LIBRARY})

# there are windows and linux specific libraries that also need to be linked in
if(WIN32)
	target_link_libraries(main setupapi hid)
else()
	target_link_libraries(main pthread)
endif()