import time
import os
import subprocess

# CPU/APU Power Paths
RAPL_PATH = "/sys/class/powercap/intel-rapl:0/energy_uj"
OUTPUT_PATH_CPU = "/home/labonsky/ryzenadj_watts"

# Battery Paths (Total System Power)
BAT_VOLTAGE = "/sys/class/power_supply/BAT1/voltage_now"
BAT_CURRENT = "/sys/class/power_supply/BAT1/current_now"
BAT_STATUS  = "/sys/class/power_supply/BAT1/status"
OUTPUT_PATH_BAT = "/home/labonsky/laptop_watts"

# Power Commands
RYZENADJ_BIN = "/usr/local/bin/ryzenadj"
CMD_LOW_POWER  = [RYZENADJ_BIN, "--stapm-limit=5000", "--fast-limit=10000", "--slow-limit=5000"]
CMD_HIGH_POWER = [RYZENADJ_BIN, "--stapm-limit=53000", "--fast-limit=53000", "--slow-limit=35000"]

# Screen Commands (Run as user 'labonsky')
# Mode 2 = 60Hz, Mode 1 = 120Hz (based on kscreen-doctor output)
CMD_SCREEN_60HZ  = ["sudo", "-u", "labonsky", "XDG_RUNTIME_DIR=/run/user/1000", "WAYLAND_DISPLAY=wayland-0", "kscreen-doctor", "output.eDP-1.mode.2"]
CMD_SCREEN_120HZ = ["sudo", "-u", "labonsky", "XDG_RUNTIME_DIR=/run/user/1000", "WAYLAND_DISPLAY=wayland-0", "kscreen-doctor", "output.eDP-1.mode.1"]

# State Tracking
current_power_mode = None # 'AC' or 'BAT'

def read_file_int(path):
    try:
        with open(path, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def read_file_str(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return ""

def write_output(path, content):
    try:
        with open(path, 'w') as f:
            f.write(content)
        os.chmod(path, 0o666)
    except:
        pass

def apply_power_limits(mode):
    global current_power_mode
    if mode == current_power_mode:
        return # No change needed
    
    print(f"Switching power mode to: {mode}")
    try:
        if mode == 'BAT':
            # 1. Set CPU Limits
            subprocess.call(CMD_LOW_POWER)
            # 2. Set Screen to 60Hz
            subprocess.call(CMD_SCREEN_60HZ)
        else:
            # 1. Set CPU Limits
            subprocess.call(CMD_HIGH_POWER)
            # 2. Set Screen to 120Hz
            subprocess.call(CMD_SCREEN_120HZ)
            
        current_power_mode = mode
    except Exception as e:
        print(f"Failed to apply limits: {e}")

last_energy = read_file_int(RAPL_PATH)
last_time = time.time()

while True:
    time.sleep(1)
    
    # --- Part 1: CPU/APU Power ---
    curr_energy = read_file_int(RAPL_PATH)
    curr_time = time.time()
    
    diff_energy = curr_energy - last_energy
    diff_time = curr_time - last_time
    
    if diff_time > 0:
        watts_cpu = (diff_energy / 1000000.0) / diff_time
        write_output(OUTPUT_PATH_CPU, f"{watts_cpu:.1f} W")
            
    last_energy = curr_energy
    last_time = curr_time

    # --- Part 2: Total Laptop Power (Battery) & Auto-Adjustment ---
    voltage = read_file_int(BAT_VOLTAGE)
    current = read_file_int(BAT_CURRENT)
    status = read_file_str(BAT_STATUS)
    
    # Determine Mode
    if status == "Discharging":
        apply_power_limits('BAT')
    else:
        # Charging, Full, Not charging (AC)
        apply_power_limits('AC')

    # Write Widget Output
    if current > 0:
        watts_bat = (voltage * current) / 1000000000000.0
        if status == "Discharging":
            write_output(OUTPUT_PATH_BAT, f"{watts_bat:.1f} W")
        elif status == "Charging":
            write_output(OUTPUT_PATH_BAT, f"+{watts_bat:.1f} W")
        else:
            write_output(OUTPUT_PATH_BAT, f"{watts_bat:.1f} W")
    else:
        write_output(OUTPUT_PATH_BAT, "AC Mode")