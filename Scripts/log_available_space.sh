#!/bin/bash
timestamp=$(date +%s%N)
space=$(/home/pi/EMLI-16/Scripts/available_space.sh)
curl -XPOST "http://localhost:8086/write?db=system_state" --data-binary "available_space,name=rpi value=$space $timestamp"
