#!/bin/bash
temperature=$(vcgencmd measure_temp | grep -o -P "=.*'" | tail -c +2 | head -c +2)
echo $temperature
