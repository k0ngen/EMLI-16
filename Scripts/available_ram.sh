#!/bin/bash
total=$(free -m | awk 'NR==2{printf "%s\n", $2}')
available=$(free -m | awk 'NR==2{printf "%s\n", $7}')
percentage=$(echo "scale=2; $available/$total*100" | bc)
echo $percentage
