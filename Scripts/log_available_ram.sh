#!/bin/bash
timestamp=$(date +%s%N)
ram=$(/home/pi/EMLI-16/Scripts/available_ram.sh | cut -d= -f1)
curl -XPOST "http://localhost:8086/write?db=system_state" --data-binary "available_ram,name=rpi value=$ram $timestamp"
