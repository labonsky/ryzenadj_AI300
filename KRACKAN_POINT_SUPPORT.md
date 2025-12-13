# AMD Ryzen AI 300 (Krackan Point) Support

This fork of [FlyGoat/RyzenAdj](https://github.com/FlyGoat/RyzenAdj) includes full support for **Krackan Point** (AMD Ryzen AI 300 series) processors.

## Overview

| Component | Status | Notes |
|-----------|--------|-------|
| **RyzenAdj** | Working | PM table size fix applied |
| **ryzen_smu** | Patched | Full Krackan Point support added |
| **Power Automation** | Working | Systemd service + KDE widgets |

## Hardware Specifications

| Property | Value |
|----------|-------|
| Codename | Krackan Point |
| Product | AMD Ryzen AI 300 Series |
| Architecture | Zen 5 |
| CPU Family | 0x1A |
| CPU Model | 0x60 (96) |
| PM Table Version | 0x650005 |
| PM Table Size | 0xD80 (3456 bytes) |

## Changes from Upstream

### RyzenAdj (lib/api.c)

Single line addition for PM table size:

```c
case 0x650005: ry->table_size = 0xD80; break;  // Krackan Point
```

Without this fix, Krackan Point falls to default size (0x1000), which works but is larger than necessary.

### ryzen_smu (ryzen_smu/)

Fresh clone of [amkillam/ryzen_smu](https://github.com/amkillam/ryzen_smu) v0.1.7 with Krackan Point patches:

- **smu.h**: Added `CODENAME_KRACKANPOINT` enum
- **smu.c**: 9 additions for CPU detection, mailbox config, PM table
- **lib/libsmu.h**: Added enum
- **lib/libsmu.c**: Added codename string

See `ryzen_smu/KRACKAN_POINT.md` for details.

## Installation

### 1. Build RyzenAdj

```bash
cd /home/labonsky/Projects/ryzenadj
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
sudo cp ryzenadj /usr/local/bin/
```

### 2. Install ryzen_smu (Optional)

RyzenAdj works with `/dev/mem` by default. For the safer ryzen_smu driver:

```bash
cd /home/labonsky/Projects/ryzenadj/ryzen_smu
sudo ./install.sh
```

### 3. Verify

```bash
sudo ryzenadj -i
```

## Power Automation

See `WIDGET_SETUP.md` for the systemd service and KDE widget configuration.

### Quick Start

```bash
# Start the power management service
sudo systemctl start ryzenadj-feeder.service
sudo systemctl enable ryzenadj-feeder.service

# Check status
sudo systemctl status ryzenadj-feeder.service
```

### Power Profiles

| Mode | STAPM | Fast | Slow | Refresh |
|------|-------|------|------|---------|
| Battery | 5W | 7W | 5W | 60Hz |
| AC | 51W | 51W | 33W | 120Hz |

## File Structure

```
ryzenadj/
├── lib/api.c              # +1 line PM table fix
├── ryzen_smu/             # Patched kernel module
│   ├── install.sh         # Installation script
│   ├── KRACKAN_POINT.md   # Patch documentation
│   ├── smu.c              # Patched
│   ├── smu.h              # Patched
│   └── lib/               # Userspace library (patched)
├── power_feeder.py        # Power management automation
├── power_widget.py        # KDE widget (unused)
├── show_watts.sh          # Widget helper
├── show_laptop_watts.sh   # Widget helper
├── WIDGET_SETUP.md        # Widget documentation
└── KRACKAN_POINT_SUPPORT.md  # This file
```

## Upstream Contributions

Consider submitting these patches upstream:

1. **RyzenAdj**: PM table size for 0x650005
   - Target: https://github.com/FlyGoat/RyzenAdj

2. **ryzen_smu**: Krackan Point support
   - Target: https://github.com/amkillam/ryzen_smu

## Troubleshooting

### RyzenAdj shows "Unsupported"

Krackan Point should be detected automatically. If not:
```bash
cat /proc/cpuinfo | grep -E "family|model"
```
Should show Family 26 (0x1A), Model 96 (0x60).

### ryzen_smu module doesn't load

```bash
dmesg | grep -i ryzen_smu
```

Check for CPUID detection or SMU initialization errors.

### PM table read fails

The PM table size (0xD80) was estimated. If you see corruption or errors, try adjusting:
- Larger: 0xE00
- Smaller: 0xD54

## License

- RyzenAdj: LGPL-3.0
- ryzen_smu: GPL-2.0
