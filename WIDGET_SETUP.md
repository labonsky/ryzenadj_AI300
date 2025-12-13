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

## 1. Power Monitoring

The `show_stats.sh` script reads directly from sysfs (no daemon needed):

- **CPU Power:** From RAPL energy counters (delta calculation)
- **Laptop Power:** From battery voltage × current
- **CPU Temp:** From k10temp hwmon

The `99-ryzenadj-rapl.rules` udev rule makes RAPL readable without root.

## 2. KDE Plasma Widget

### Quick Install (RPM package)

After installing the RPM, run:

```bash
/usr/share/ryzenadj/install-widget.sh
```

Then add and configure the widget:
1. Right-click on your KDE panel → "Add Widgets..."
2. Search for "Command Output"
3. Drag it to your panel
4. Right-click the widget → "Configure..."
5. In the Command field, paste: `/usr/libexec/ryzenadj/show_stats.sh`
6. Set interval to `1000` (1 second refresh)
7. Click Apply

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
- `bc` (for calculations in show_stats.sh)

## Version

Widget included in `ryzenadj-ryzen_smu-ai300-krackan-PP` RPM v0.19.4+
