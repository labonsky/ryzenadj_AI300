import time
import os

# CPU/APU Power Paths
RAPL_PATH = "/sys/class/powercap/intel-rapl:0/energy_uj"
OUTPUT_PATH_CPU = "/home/labonsky/ryzenadj_watts"

# Battery Paths (Total System Power)
BAT_VOLTAGE = "/sys/class/power_supply/BAT1/voltage_now"
BAT_CURRENT = "/sys/class/power_supply/BAT1/current_now"
BAT_STATUS  = "/sys/class/power_supply/BAT1/status"
OUTPUT_PATH_BAT = "/home/labonsky/laptop_watts"

# Note: Power profile switching is now handled by tuned + udev rules
# This script only monitors and writes power data for widgets

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

    # --- Part 2: Total Laptop Power (Battery) ---
    voltage = read_file_int(BAT_VOLTAGE)
    current = read_file_int(BAT_CURRENT)
    status = read_file_str(BAT_STATUS)

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
