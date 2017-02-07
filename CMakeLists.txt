cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
set(CMAKE_BUILD_TYPE Debug)
project(geodesic_comparison)

find_package(PCL 1.2 REQUIRED)

find_package(Eigen3 REQUIRED)
include_directories(include/ EIGEN3_INCLUDE_DIR ${PCL_INCLUDE_DIRS})

link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
add_library(geodesic_lib SHARED include/geodesic.h src/geodesic.cpp include/integral.h src/integral.cpp include/dijkstra.h src/dijkstra.cpp)

add_executable (geodesic_function src/geodesic_function.cpp)
add_executable (function_comparison src/function_comparison.cpp)
target_link_libraries (geodesic_function geodesic_lib ${PCL_LIBRARIES})
target_link_libraries (function_comparison geodesic_lib ${PCL_LIBRARIES})
