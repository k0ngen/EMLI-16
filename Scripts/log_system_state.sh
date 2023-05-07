#!/bin/bash

# get the current time
current_time=$(date +%Y-%m-%d\ %H:%M:%S)

# run the command to measure temperature
ram=$(sudo ~/available_ram.sh |cut -d= -f1)

# append the data to the log file
echo "$current_time,$ram" >> DATALOGGIN.csv
