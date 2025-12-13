# RyzenAdj Power Monitor for KDE Plasma

This solution provides:
1. **Power Monitoring:** Displays live wattage for CPU and total laptop power
2. **Auto-Power Management:** Via tuned profiles with udev auto-switching

## Power Profiles

| Profile | STAPM | Fast | Slow | Screen |
|---------|-------|------|------|--------|
| Battery | 5W | 10W | 5W | 60Hz |
| AC | 53W | 53W | 35W | 120Hz |

Power management is handled by **tuned** (see `tuned-profiles/`).

---

## 1. Power Monitoring Service

The `power_feeder.py` script runs as root and writes power data to user-readable files:

- `~/ryzenadj_watts` - CPU power consumption
- `~/laptop_watts` - Total laptop power (battery discharge)

### Service Management

```bash
sudo systemctl status ryzenadj-feeder.service
sudo systemctl restart ryzenadj-feeder.service
sudo journalctl -u ryzenadj-feeder.service -f
```

## 2. KDE Plasma Widgets

Use two "Command Output" widgets on the KDE Panel:

### Widget 1: CPU Power
- **Command:** `/home/labonsky/Projects/ryzenadj/show_watts.sh`
- **Interval:** 1000 ms

### Widget 2: Total Laptop Power
- **Command:** `/home/labonsky/Projects/ryzenadj/show_laptop_watts.sh`
- **Interval:** 1000 ms

## 3. Power Profile Switching

Power profiles are managed by **tuned** with automatic switching via udev:

```bash
# Check current profile
tuned-adm active

# Manual switching
sudo tuned-adm profile ryzenadj-battery
sudo tuned-adm profile ryzenadj-ac

# KDE GUI also works (Power Saver / Balanced / Performance)
```

See `tuned-profiles/install.sh` for installation.

## Dependencies

- `ryzenadj` (installed in `/usr/local/bin/`)
- `tuned` (Fedora default)
- `python3`
