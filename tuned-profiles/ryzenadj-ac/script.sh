#!/bin/bash
case "$1" in
    start)
        /usr/local/bin/ryzenadj --stapm-limit=53000 --fast-limit=53000 --slow-limit=35000 2>/dev/null
        sudo -u labonsky XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-0 kscreen-doctor output.eDP-1.mode.1 2>/dev/null
        ;;
esac
exit 0
