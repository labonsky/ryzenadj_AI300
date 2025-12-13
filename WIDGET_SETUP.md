# RyzenAdj Power Monitor for KDE Plasma

This solution provides:
1. **Power Monitoring:** Displays live CPU power, total laptop power, and CPU temperature
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
- `~/cpu_temp` - CPU temperature (Tctl)

### Service Management

```bash
sudo systemctl status ryzenadj-feeder.service
sudo systemctl restart ryzenadj-feeder.service
sudo journalctl -u ryzenadj-feeder.service -f
```

## 2. KDE Plasma Widget

### Quick Install (RPM package)

After installing the RPM, run:

```bash
/usr/share/ryzenadj/install-widget.sh
```

Then add the widget to your panel:
1. Right-click on your KDE panel → "Add Widgets..."
2. Search for "Command Output"
3. Drag it to your panel

### Manual Install (from source)

```bash
cd widget && ./install-widget.sh
```

**Output format:** `Laptop | CPU | Temp` (e.g., `7.2 W | 3.5 W | 37°C`)

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

- `ryzenadj` (RPM: `/usr/bin/`, source: `/usr/local/bin/`)
- `tuned` (Fedora default)
- `python3`

## Version

Widget included in `ryzenadj-ryzen_smu-ai300-krackan-PP` RPM v0.19.1+
