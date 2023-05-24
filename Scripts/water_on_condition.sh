#!/bin/bash
current_timestamp=$(date +%s%N)
latest_watering=$(python3 /home/pi/EMLI-16/Scripts/get_latest_watering.py)
hour_in_nano=$((3600 * 1000000000))
time=$(expr $current_timestamp - $hour_in_nano)

if [ $latest_watering -ge $time ];
then
	echo "The latest watering is too recent"
	exit
fi

moisture=$(python3 /home/pi/EMLI-16/Scripts/get_soil_moisture.py)
threshold=50
if [ $moisture -lt $threshold ];
then
	python3 /home/pi/EMLI-16/Scripts/water_plant.py
	echo "The plant was watered"
else
	echo "No watering as the soil is moist"
fi

