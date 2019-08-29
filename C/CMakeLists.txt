cmake_minimum_required(VERSION 2.8.3) 
project(flexsea_c_scripts)

if(WIN32)
	set(PLAT_DIR "win")
elseif(UNIX AND NOT APPLE)
	set(PLAT_DIR "unix")
else()
	message(FATAL_ERROR " host OS not supported, exiting now!")
endif()

if(CMAKE_SIZEOF_VOID_P EQUAL 8)
	set(PLAT_DIR "${PLAT_DIR}64")
else()
	set(PLAT_DIR "${PLAT_DIR}32")
endif()

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

set(SRCS
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

add_executable(main ${SRCS})

find_library(fx_plan_stack_LIBRARY fx_plan_stack_static ${CMAKE_CURRENT_SOURCE_DIR}/../fx_plan_stack/build/libs)

#target_link_libraries(main pthread)
target_link_libraries(main ${fx_plan_stack_LIBRARY})
if(WIN32)
	target_link_libraries(main setupapi hid)
endif()