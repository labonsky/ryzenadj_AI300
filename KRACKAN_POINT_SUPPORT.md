# AMD Ryzen AI 300 (Krackan Point) Support

This fork of [FlyGoat/RyzenAdj](https://github.com/FlyGoat/RyzenAdj) includes full support for **Krackan Point** (AMD Ryzen AI 300 series) processors.

## Hardware Specifications

| Property | Value |
|----------|-------|
| Codename | Krackan Point |
| Product | AMD Ryzen AI 5 340 / AI 7 350 |
| Architecture | Zen 5 + Zen 5c (hybrid) |
| CPU Family | 0x1A |
| CPU Model | 0x60 (96) |
| PM Table Version | 0x650005 |
| PM Table Size | 0xD80 (3456 bytes) |
| Base TDP | 28W |
| Configurable TDP | 15-54W |

## Component Status

| Component | Status | Notes |
|-----------|--------|-------|
| **RyzenAdj** | ✓ Working | PM table size fix applied |
| **ryzen_smu** | ✓ Patched | Full Krackan Point support |
| **tuned profiles** | ✓ Working | Auto-switching via udev |
| **KDE integration** | ✓ Working | Power profiles + widgets |
| **Boot detection** | ✓ Working | Systemd service applies correct profile |
| **Screen refresh** | ✓ Working | 120Hz on AC, 60Hz on battery |

## Changes from Upstream

### RyzenAdj (lib/api.c)

```c
case 0x650005: ry->table_size = 0xD80; break;  // Krackan Point
```

### ryzen_smu (ryzen_smu/)

Patched v0.1.7 with Krackan Point support:
- `smu.h`: Added `CODENAME_KRACKANPOINT` enum
- `smu.c`: CPU detection, mailbox config, PM table version/size
- `lib/libsmu.h`, `lib/libsmu.c`: Userspace library patches

See `ryzen_smu/KRACKAN_POINT.md` for patch details.

## Installation

### RPM Package (Fedora - Recommended)

Download from [GitHub Releases](https://github.com/labonsky/ryzenadj_AI300/releases):

```bash
# Install RPM
sudo dnf install ryzenadj-ryzen_smu-ai300-krackan-PP-0.19.9.2-1.fc43.x86_64.rpm

# Install KDE widget
/usr/share/ryzenadj/install-widget.sh
# Then: Add Widgets → "Command Output" → drag to panel
# Widget is pre-configured, no manual setup needed

# Verify
sudo ryzenadj -i
tuned-adm list | grep ryzenadj
```

The RPM includes everything: ryzenadj binary, ryzen_smu DKMS module, tuned profiles, auto-switching, and KDE widget.

### Build from Source

```bash
# Clone
git clone https://github.com/labonsky/ryzenadj_AI300.git
cd ryzenadj_AI300

# Build RyzenAdj
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo cp ryzenadj /usr/bin/
cd ..

# Install ryzen_smu kernel module
cd ryzen_smu && sudo ./install.sh && cd ..

# Install tuned profiles (Fedora)
cd tuned-profiles && sudo ./install.sh && cd ..

# Verify
sudo ryzenadj -i
tuned-adm list | grep ryzenadj
```

## Power Profiles

### tuned Integration (Fedora)

| Profile | Inherits | STAPM | Fast | Slow | Screen |
|---------|----------|-------|------|------|--------|
| `ryzenadj-battery` | powersave | 3W | 5W | 3W | 60Hz |
| `ryzenadj-balanced` | powersave | 3W | 5W | 3W | 60Hz |
| `ryzenadj-ac` | throughput-performance | 53W | 53W | 35W | 120Hz |

### KDE Power Profiles Mapping

| KDE GUI | tuned Profile |
|---------|---------------|
| Power Saver | ryzenadj-battery |
| Balanced | ryzenadj-balanced |
| Performance | ryzenadj-ac |

### Manual Switching

```bash
sudo tuned-adm profile ryzenadj-battery  # Low power
sudo tuned-adm profile ryzenadj-ac       # Full power
tuned-adm active                          # Check current
```

### Auto-Switching

Fully automatic power management:

| Event | Profile | Power Limits | Screen |
|-------|---------|--------------|--------|
| **Plug in AC** | ryzenadj-ac | 53W / 35W | 120Hz |
| **Unplug** | ryzenadj-battery | 5W / 3W | 60Hz |
| **Boot on AC** | ryzenadj-ac | 53W / 35W | 120Hz |
| **Boot on battery** | ryzenadj-battery | 5W / 3W | 60Hz |

How it works:
- **udev rules:** Detect AC plug/unplug events and switch profiles
- **Boot service:** Systemd oneshot service checks AC state at boot
- **Profile scripts:** Apply ryzenadj power limits + kscreen-doctor refresh rate

## File Structure

```
ryzenadj/
├── lib/api.c              # PM table size fix
├── ryzen_smu/             # Patched kernel module
├── tuned-profiles/        # Fedora tuned integration
│   ├── install.sh
│   ├── ppd.conf           # KDE power profiles mapping
│   ├── 99-ryzenadj-power.rules    # AC/battery auto-switching
│   ├── 99-ryzenadj-rapl.rules     # RAPL permissions for widget
│   ├── ryzenadj-boot-check.sh     # Boot-time profile check
│   ├── ryzenadj-boot-check.service
│   ├── ryzenadj-battery/
│   ├── ryzenadj-balanced/
│   └── ryzenadj-ac/
├── rpm/                   # RPM packaging
│   └── ryzenadj-ryzen_smu-ai300-krackan-PP.spec
├── widget/                # KDE Command Output widget
│   ├── install-widget.sh
│   └── com.github.zren.commandoutput/
├── show_stats.sh          # Combined stats (Laptop | CPU | Temp)
├── archive/               # Archived old scripts
└── WIDGET_SETUP.md        # Widget documentation
```

## Troubleshooting

### Check Detection

```bash
# CPU info
cat /proc/cpuinfo | grep -E "family|model"
# Should show: Family 26 (0x1A), Model 96 (0x60)

# ryzen_smu
cat /sys/kernel/ryzen_smu_drv/codename
# Should show: 27 (CODENAME_KRACKANPOINT)

# PM table version
sudo od -A x -t x1z /sys/kernel/ryzen_smu_drv/pm_table_version
# Should show: 05 00 65 00 (0x650005)
```

### Common Issues

| Issue | Solution |
|-------|----------|
| "Unsupported" | Check CPU family/model matches |
| Module won't load | Check dmesg, verify Secure Boot MOK |
| PM table fails | Verify codename 27 detected |

## License

- RyzenAdj: LGPL-3.0
- ryzen_smu: GPL-2.0
