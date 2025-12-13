#!/bin/bash
# Check power state at boot and apply correct tuned profile

AC_ONLINE=$(cat /sys/class/power_supply/AC*/online 2>/dev/null || cat /sys/class/power_supply/ADP*/online 2>/dev/null || echo "0")

if [ "$AC_ONLINE" = "1" ]; then
    /usr/sbin/tuned-adm profile ryzenadj-ac
    echo "Boot: AC detected, applied ryzenadj-ac profile"
else
    /usr/sbin/tuned-adm profile ryzenadj-battery
    echo "Boot: Battery detected, applied ryzenadj-battery profile"
fi
