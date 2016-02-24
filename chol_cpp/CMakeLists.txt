cmake_minimum_required(VERSION 3.3)
project(cholesky)
find_package( PkgConfig )
pkg_check_modules( EIGEN3 REQUIRED eigen3 )
include_directories( ${EIGEN3_INCLUDE_DIRS} )
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -I ${EIGEN3_INCLUDE_DIRS}")

set(SOURCE_FILES main.cpp)
add_executable(cholesky ${SOURCE_FILES})
