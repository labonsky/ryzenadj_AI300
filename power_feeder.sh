#!/bin/bash
# Reads energy values and writes to a temp file readable by user
TEMP_FILE="/tmp/ryzenadj_power.txt"

# Create file and set permissions so user can read it
touch "$TEMP_FILE"
chmod 666 "$TEMP_FILE"

while true; do
    cat /sys/class/powercap/intel-rapl:0/energy_uj > "$TEMP_FILE"
    sleep 1
done
