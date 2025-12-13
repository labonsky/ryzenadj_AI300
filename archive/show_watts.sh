#!/bin/bash
if [ -f /home/labonsky/ryzenadj_watts ]; then
    /usr/bin/cat /home/labonsky/ryzenadj_watts
else
    echo "No Data"
fi
