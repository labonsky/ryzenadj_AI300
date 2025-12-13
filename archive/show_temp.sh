#!/bin/bash
if [ -f /home/labonsky/cpu_temp ]; then
    /usr/bin/cat /home/labonsky/cpu_temp
else
    echo "No Data"
fi
