cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
set(CMAKE_BUILD_TYPE Debug)
project(geodesic_comparison)

find_package(PCL 1.2 REQUIRED)

find_package(Eigen3 REQUIRED)
include_directories(EIGEN3_INCLUDE_DIR)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
add_library(geodesic_lib SHARED geodesic.h geodesic.cpp integral.h integral.cpp dijkstra.h dijkstra.cpp)

add_executable (geodesic_function geodesic_function.cpp)
add_executable (function_comparison function_comparison.cpp)
target_link_libraries (geodesic_function geodesic_lib ${PCL_LIBRARIES})
target_link_libraries (function_comparison geodesic_lib ${PCL_LIBRARIES})
