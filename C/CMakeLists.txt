cmake_minimum_required(VERSION 2.8.3) 
project(flexsea_c_scripts)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

include_directories(
	"${CMAKE_CURRENT_SOURCE_DIR}/inc"
	"${CMAKE_CURRENT_SOURCE_DIR}/../inc"
	"${CMAKE_CURRENT_SOURCE_DIR}/src"
)

set(CSCRIPT_SRCS
	main.cpp
	"${CMAKE_CURRENT_SOURCE_DIR}/src/readonly.cpp"
	"${CMAKE_CURRENT_SOURCE_DIR}/src/fxUtil.cpp"
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/open_speed_example.cpp"
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/current_control.cpp"
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/hold_position_example.cpp"
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/findpolesexample.cpp"
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/two_dev_position_example.cpp"
	# "${CMAKE_CURRENT_SOURCE_DIR}/src/leaderfollower.cpp"
	"${CMAKE_CURRENT_SOURCE_DIR}/inc/utils.h"
)

add_executable(main ${CSCRIPT_SRCS})

# build the executable
#set(COMM_TEST_SRCS communication_tester.cpp)
#add_executable(communication_tester ${COMM_TEST_SRCS})

if(WIN32)
	# only look for a freshly built plan stack library since we're already set up to compile this find_program
	# should not be an issues to have a freshly compiled plan stack to prevent confusion
	find_library(fx_plan_stack_LIBRARY fx_plan_stack_static ${CMAKE_CURRENT_SOURCE_DIR}/../libs/win32)

	# link plan stack library to our application
	target_link_libraries(main ${fx_plan_stack_LIBRARY})
	#	target_link_libraries(communication_tester ${fx_plan_stack_LIBRARY})

	# there are windows and linux specific libraries that also need to be linked in
	target_link_libraries(main setupapi hid)
	#target_link_libraries(communication_tester setupapi hid)
elseif( "${CMAKE_SIZEOF_VOID_P}" EQUAL "8" AND UNIX) # 64 bit Linux
	# only look for a freshly built plan stack library since we're already set up to compile this find_program
	# should not be an issues to have a freshly compiled plan stack to prevent confusion
	find_library(fx_plan_stack_LIBRARY fx_plan_stack_static ${CMAKE_CURRENT_SOURCE_DIR}/../libs/linux)

	# link plan stack library to our application
	target_link_libraries(main ${fx_plan_stack_LIBRARY})

	target_link_libraries(main pthread)	
else()
	# only look for a freshly built plan stack library since we're already set up to compile this find_program
	# should not be an issues to have a freshly compiled plan stack to prevent confusion
	find_library(fx_plan_stack_LIBRARY fx_plan_stack_static ${CMAKE_CURRENT_SOURCE_DIR}/../libs/raspberryPi)

	# link plan stack library to our application
	target_link_libraries(main ${fx_plan_stack_LIBRARY})

	target_link_libraries(main pthread)
endif()
