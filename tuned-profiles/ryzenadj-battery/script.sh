#!/bin/bash
case "$1" in
    start)
        # Delay to let base profile settings apply first
        sleep 1
        /usr/bin/ryzenadj --stapm-limit=3000 --fast-limit=5000 --slow-limit=3000 2>/dev/null
        # Set 60Hz for battery - find logged-in graphical user
        for session in $(loginctl list-sessions --no-legend | awk '{print $1}'); do
            user=$(loginctl show-session "$session" -p Name --value 2>/dev/null)
            type=$(loginctl show-session "$session" -p Type --value 2>/dev/null)
            uid=$(id -u "$user" 2>/dev/null)
            if [ "$type" = "wayland" ] && [ -n "$uid" ]; then
                sudo -u "$user" XDG_RUNTIME_DIR="/run/user/$uid" WAYLAND_DISPLAY=wayland-0 kscreen-doctor output.eDP-1.mode.2 2>/dev/null
                break
            fi
        done
        ;;
esac
exit 0
