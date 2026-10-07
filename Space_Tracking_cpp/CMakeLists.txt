cmake_minimum_required(VERSION 3.10)
project(SpaceTracking CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB SOURCES "*.cpp")
add_executable(space_tracking ${SOURCES})
