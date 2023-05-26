#!/bin/bash
source /opt/ros/humble/setup.bash
source /home/pi/ros2_ws/install/setup.bash
ros2 run emli_package emli_sub_node
ros2 run emli_package emli_farmer_node
ros2 run emli_package emli_light_node
ros2 run emli_package emli_moisture_node
ros2 run emli_package emli_water_alarm_node
ros2 run emli_package emli_pump_alarm_node
ros2 run emli_package emli_pub_node