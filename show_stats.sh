#!/bin/bash
CPU=$(cat /home/labonsky/ryzenadj_watts 2>/dev/null || echo "?")
BAT=$(cat /home/labonsky/laptop_watts 2>/dev/null || echo "?")
TEMP=$(cat /home/labonsky/cpu_temp 2>/dev/null || echo "?")
echo "$CPU | $BAT | $TEMP"
