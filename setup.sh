#!/bin/bash
cd mesh_reconstruction
mkdir build
cd build
make clean
cmake ..
make -j5
cd ../../geodesic_comparison
mkdir build
cd build
make clean
cmake ..
make -j5
cd ../../mirror_ws
source /opt/ros/indigo/setup.bash
rm -rf build devel
catkin_make
cd ..