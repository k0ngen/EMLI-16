#!/bin/bash
timestamp=$(date +%s%N)
temperature=$(/home/pi/EMLI-16/Scripts/temperature.sh)
curl -XPOST "http://localhost:8086/write?db=system_state" --data-binary "temperature,name=rpi value=$temperature $timestamp"
