#!/bin/bash
# RyzenAdj Power Stats - Direct sysfs reads (no daemon needed)
# Output: Laptop | CPU | Temp (e.g., "7.2 W | 3.5 W | 37°C")

STATE_FILE="/tmp/ryzenadj_rapl_state"
RAPL_PATH="/sys/class/powercap/intel-rapl:0/energy_uj"

# --- CPU Power (RAPL delta calculation) ---
get_cpu_power() {
    local curr_energy curr_time prev_energy prev_time
    curr_energy=$(cat "$RAPL_PATH" 2>/dev/null) || { echo "?"; return; }
    curr_time=$(date +%s%N)

    if [[ -f "$STATE_FILE" ]]; then
        read prev_energy prev_time < "$STATE_FILE"
        if [[ -n "$prev_energy" && -n "$prev_time" ]]; then
            local diff_energy=$((curr_energy - prev_energy))
            local diff_time=$((curr_time - prev_time))
            # Handle RAPL counter overflow (wraps at ~65.5 GJ)
            if [[ $diff_energy -lt 0 ]]; then
                local max_range=$(cat /sys/class/powercap/intel-rapl:0/max_energy_range_uj 2>/dev/null)
                [[ -n "$max_range" ]] && diff_energy=$((diff_energy + max_range))
            fi
            if [[ $diff_time -gt 0 && $diff_energy -ge 0 ]]; then
                # energy in uJ, time in ns -> watts = (uJ * 1000) / ns
                local watts=$(echo "scale=1; $diff_energy * 1000 / $diff_time" | bc 2>/dev/null)
                [[ -n "$watts" ]] && echo "${watts} W" || echo "?"
            else
                echo "?"
            fi
        else
            echo "..."
        fi
    else
        echo "..."
    fi
    echo "$curr_energy $curr_time" > "$STATE_FILE"
}

# --- Laptop Power (Battery voltage * current) ---
get_laptop_power() {
    local voltage current status watts
    voltage=$(cat /sys/class/power_supply/BAT1/voltage_now 2>/dev/null) || { echo "?"; return; }
    current=$(cat /sys/class/power_supply/BAT1/current_now 2>/dev/null) || { echo "?"; return; }
    status=$(cat /sys/class/power_supply/BAT1/status 2>/dev/null)

    if [[ $current -gt 0 ]]; then
        # voltage in uV, current in uA -> watts = (uV * uA) / 10^12
        watts=$(echo "scale=1; $voltage * $current / 1000000000000" | bc 2>/dev/null)
        if [[ "$status" == "Charging" ]]; then
            echo "+${watts} W"
        else
            echo "${watts} W"
        fi
    else
        echo "AC"
    fi
}

# --- CPU Temperature (k10temp) ---
get_cpu_temp() {
    local hwmon temp
    for hwmon in /sys/class/hwmon/hwmon*; do
        if [[ "$(cat "$hwmon/name" 2>/dev/null)" == "k10temp" ]]; then
            temp=$(cat "$hwmon/temp1_input" 2>/dev/null)
            if [[ -n "$temp" ]]; then
                echo "$((temp / 1000))°C"
                return
            fi
        fi
    done
    echo "?"
}

# Output: Laptop | CPU | Temp
echo "$(get_laptop_power) | $(get_cpu_power) | $(get_cpu_temp)"
