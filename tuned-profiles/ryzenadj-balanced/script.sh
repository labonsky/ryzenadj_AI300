#!/bin/bash
case "$1" in
    start)
        /usr/local/bin/ryzenadj --stapm-limit=5000 --fast-limit=10000 --slow-limit=5000 2>/dev/null
        sudo -u labonsky XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-0 kscreen-doctor output.eDP-1.mode.2 2>/dev/null
        ;;
esac
exit 0
