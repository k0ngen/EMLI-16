#!/bin/bash
load=$(top -bn1 | awk '/Cpu/ {print $2 + $4}')
rounded_load=$(printf "%.0f" $load)
echo "CPU load: $rounded_load %"
