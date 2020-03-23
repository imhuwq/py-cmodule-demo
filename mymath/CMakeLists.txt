project(mymath)
cmake_minimum_required(VERSION 3.10)

set(Python3_USE_STATIC_LIBS FALSE)
#set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python3 COMPONENTS Interpreter Development)

set(SOURCES "")
set(INCLUDES "")
set(LIBRARIES "")

list(APPEND SOURCES mymath.c)
list(APPEND INCLUDES ${Python3_INCLUDE_DIRS})
list(APPEND LIBRARIES ${Python3_LIBRARIES})

include_directories(${INCLUDES})
add_library(mymath SHARED ${SOURCES})
target_link_libraries(mymath PUBLIC ${LIBRARIES})

set_target_properties(mymath PROPERTIES OUTPUT_NAME "mymath" PREFIX "")
