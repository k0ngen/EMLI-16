#!/bin/bash
bytes=$(ifconfig $1 | grep "RX packets" | awk '{print $5}')
echo $bytes
