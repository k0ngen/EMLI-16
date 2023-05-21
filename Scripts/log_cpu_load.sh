#!/bin/bash
timestamp=$(date +%s%N)
cpu_load=$(/home/pi/EMLI-16/Scripts/cpu_load.sh)
curl -XPOST "http://localhost:8086/write?db=system_state" --data-binary "cpu_load,name=rpi value=$cpu_load $timestamp"
