# RyzenAdj Power Monitor & Auto-Limiter for KDE Plasma

This solution provides:
1.  **Dual Power Monitoring:** Displays live wattage for CPU/APU and the entire laptop battery.
2.  **Auto-Power Management:** Automatically switches power limits and screen refresh rates when unplugged/plugged.
3.  **Security Bypass:** Runs as a systemd service to handle root-level hardware access while displaying safe data to the user.

## Features
*   **On Battery:** 
    *   CPU Limit: 3W (Silent/Cool)
    *   Refresh Rate: 60Hz
*   **Plugged In:** 
    *   CPU Limit: 33W (Performance)
    *   Refresh Rate: 120Hz
*   **Persistence:** Runs automatically at boot.

---

## 1. The Backend Script (`power_feeder.py`)

Located at: `/home/labonsky/Projects/ryzenadj/power_feeder.py`

This script runs as **root**. It monitors:
*   `/sys/class/powercap/...` (CPU Power)
*   `/sys/class/power_supply/BAT1/...` (Battery Status)

It writes safe output files for the widgets:
*   `~/ryzenadj_watts` (CPU Power)
*   `~/laptop_watts` (Total Power)

And executes system commands:
*   `ryzenadj` (Power Limits)
*   `kscreen-doctor` (Refresh Rate - executed as user `labonsky`)

## 2. The System Service

Located at: `/etc/systemd/system/ryzenadj-feeder.service`

Ensures the backend script runs at startup.

### Management Commands:
```bash
sudo systemctl status ryzenadj-feeder.service
sudo systemctl restart ryzenadj-feeder.service
sudo journalctl -u ryzenadj-feeder.service -f  # View logs
```

## 3. The Frontend Widgets (KDE Plasma)

We use two "Command Output" widgets on the KDE Panel.

### Widget 1: CPU Power
*   **Command:** `/home/labonsky/Projects/ryzenadj/show_watts.sh`
*   **Interval:** 1000 ms

### Widget 2: Total Laptop Power
*   **Command:** `/home/labonsky/Projects/ryzenadj/show_laptop_watts.sh`
*   **Interval:** 1000 ms

---

## Wrapper Scripts
These helper scripts prevent errors if the data files are missing during boot.

*   `/home/labonsky/Projects/ryzenadj/show_watts.sh`
*   `/home/labonsky/Projects/ryzenadj/show_laptop_watts.sh`

## Dependencies
*   `ryzenadj` (installed in `/usr/local/bin/`)
*   `kscreen-doctor` (KDE standard tool)
*   `python3`