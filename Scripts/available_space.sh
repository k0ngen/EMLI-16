#!/bin/bash
info=$(df -H / --output=pcent | tail -n +2)
percent=$(echo $info | awk '{print $1}' | tr -d '%')
echo $percent

