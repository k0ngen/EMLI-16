#!/bin/bash
timestamp=$(date +%s%N)
wlan_bytes=$(/home/pi/EMLI-16/Scripts/transferred_bytes.sh wlan0)

curl -XPOST "http://localhost:8086/write?db=system_state" --data-binary "transferred_wlan_bytes,name=rpi value=$wlan_bytes $timestamp"
