#!/bin/bash
if [ -f /home/labonsky/laptop_watts ]; then
    /usr/bin/cat /home/labonsky/laptop_watts
else
    echo "Waiting..."
fi
