# Claude Code Project Context

This file provides context for Claude Code to quickly understand and work with this project.

## Project Overview

**RyzenAdj fork with AMD Ryzen AI 300 (Krackan Point) support** - Power management suite for Fedora/KDE.

| Component | Purpose |
|-----------|---------|
| ryzenadj | CLI tool to adjust CPU power limits |
| ryzen_smu | Kernel module for SMU communication (DKMS) |
| tuned profiles | Fedora power profiles with auto-switching |
| KDE widget | Power monitoring (Laptop \| CPU \| Temp) |

## Key File Locations

### Source Files
```
/home/labonsky/Projects/ryzenadj/
├── lib/api.c                          # PM table size fix (0x650005 → 0xD80)
├── show_stats.sh                      # Widget script (RAPL + battery + temp)
├── rpm/ryzenadj-ryzen_smu-ai300-krackan-PP.spec  # RPM spec
├── tuned-profiles/
│   ├── ryzenadj-battery/script.sh     # 10W/5W, 60Hz
│   ├── ryzenadj-ac/script.sh          # 53W/35W, 120Hz
│   ├── ryzenadj-balanced/script.sh    # Same as battery
│   ├── 99-ryzenadj-power.rules        # udev auto-switching
│   ├── 99-ryzenadj-rapl.rules         # RAPL permissions
│   └── ryzenadj-boot-check.sh         # Boot-time profile detection
├── widget/
│   ├── install-widget.sh
│   └── com.github.zren.commandoutput/ # Pre-configured widget
└── ryzen_smu/                         # Patched kernel module v0.1.7
```

### Installed Locations (RPM)
```
/usr/bin/ryzenadj                      # Main binary
/usr/bin/ryzenadj-boot-check.sh        # Boot script
/usr/lib64/libryzenadj.so              # Library
/usr/libexec/ryzenadj/show_stats.sh    # Widget script
/usr/src/ryzen_smu-0.1.7/              # DKMS source
/etc/tuned/profiles/ryzenadj-*/        # tuned profiles
/usr/lib/udev/rules.d/99-ryzenadj-*.rules  # udev rules
/usr/lib/systemd/system/ryzenadj-boot-check.service
/usr/share/ryzenadj/                   # Widget files
```

## Common Commands

### Testing
```bash
# Power limits
sudo ryzenadj -i | grep -E "STAPM|PPT"

# Current profile
tuned-adm active

# Widget output
/usr/libexec/ryzenadj/show_stats.sh

# Screen refresh rate
kscreen-doctor -o | grep eDP

# AC status
cat /sys/class/power_supply/ACAD/online  # 1=AC, 0=battery

# Boot service
systemctl status ryzenadj-boot-check.service
journalctl -u ryzenadj-boot-check.service
```

### Profile Switching
```bash
sudo tuned-adm profile ryzenadj-battery  # 10W/5W, 60Hz
sudo tuned-adm profile ryzenadj-ac       # 53W/35W, 120Hz
```

## Release Process

1. **Update version** in `rpm/ryzenadj-ryzen_smu-ai300-krackan-PP.spec`:
   - Change `Version:` line
   - Add changelog entry

2. **Commit and tag**:
   ```bash
   git add -A && git commit -m "Bump version to X.Y.Z"
   git tag -a vX.Y.Z -m "vX.Y.Z: Description"
   git push labonsky master --tags
   ```

3. **Build RPM**:
   ```bash
   git archive --format=tar.gz --prefix=ryzenadj_AI300-X.Y.Z/ \
     -o ~/rpmbuild/SOURCES/vX.Y.Z.tar.gz vX.Y.Z
   rpmbuild -bb rpm/ryzenadj-ryzen_smu-ai300-krackan-PP.spec
   ```

4. **Create GitHub release**:
   ```bash
   gh release create vX.Y.Z \
     ~/rpmbuild/RPMS/x86_64/ryzenadj-ryzen_smu-ai300-krackan-PP-X.Y.Z-1.fc43.x86_64.rpm \
     ~/rpmbuild/SOURCES/vX.Y.Z.tar.gz \
     --repo labonsky/ryzenadj_AI300 \
     --title "vX.Y.Z: Description" \
     --notes "Release notes here"
   ```

5. **Install and test**:
   ```bash
   sudo dnf install ~/rpmbuild/RPMS/x86_64/ryzenadj-*.rpm
   ```

## Known Quirks

### STAPM Limit is Dynamic
- Requested STAPM (e.g., 5W) may show as ~10-14W in ryzenadj output
- This is firmware-controlled based on thermal headroom
- PPT Fast/Slow limits are the ones directly controlled

### Profile Script Timing
- Scripts include `sleep 1` before ryzenadj to let base profile apply first
- Without this delay, base profile (powersave) can override ryzenadj settings

### RAPL Counter Overflow
- show_stats.sh handles counter wraparound at ~65.5 GJ
- Without overflow handling, CPU power shows negative values

### Screen Refresh Modes
- Mode 1: 2880x1920@120Hz (AC)
- Mode 2: 2880x1920@60Hz (battery)
- Uses kscreen-doctor with dynamic user detection via loginctl

### Config Files Not Replaced on Upgrade
- RPM uses `%config(noreplace)` for tuned profile scripts
- Manual fix needed if upgrading from old version with wrong paths:
  ```bash
  sudo cp tuned-profiles/ryzenadj-*/script.sh /etc/tuned/profiles/ryzenadj-*/
  ```

## Hardware Info

| Property | Value |
|----------|-------|
| Codename | Krackan Point |
| CPU Family | 0x1A (26) |
| CPU Model | 0x60 (96) |
| PM Table Version | 0x650005 |
| PM Table Size | 0xD80 (3456 bytes) |
| ryzen_smu codename | 27 (CODENAME_KRACKANPOINT) |

## Power Profiles

| Profile | STAPM | Fast | Slow | Screen | Use Case |
|---------|-------|------|------|--------|----------|
| ryzenadj-battery | 5W | 10W | 5W | 60Hz | Battery life |
| ryzenadj-balanced | 5W | 10W | 5W | 60Hz | Same as battery |
| ryzenadj-ac | 53W | 53W | 35W | 120Hz | Full performance |

## Sudo Access

Claude Code uses `SUDO_ASKPASS=~/.claude/hooks/sudo_askpass.sh sudo -A` for privileged commands.

## Git Remote

- Remote name: `labonsky`
- URL: https://github.com/labonsky/ryzenadj_AI300.git
- Default branch: `master`
- Current version: `v0.19.8.1`
