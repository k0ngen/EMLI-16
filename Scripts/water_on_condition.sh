#!/bin/bash
moisture=$(python3 /home/pi/EMLI-16/Scripts/get_soil_moisture.py)
threshold=50
if [ $moisture -lt $threshold ];
then
	python3 /home/pi/EMLI-16/Scripts/water_plant.py
else
	echo "No watering as the soil is moist"
fi

