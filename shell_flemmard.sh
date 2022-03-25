#!/bin/sh

cd ~/turtlebot3_ws
colcon build --symlink-install
source ~/.bashrc
ros2 run nav2_simple_commander main