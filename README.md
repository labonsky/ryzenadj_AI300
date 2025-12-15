# RyzenAdj - Krackan Point (AMD Ryzen AI 300) Fork

Power management for AMD Ryzen AI 300 series (Krackan Point) processors.

**Current release: [v0.20.0](https://github.com/labonsky/ryzenadj_AI300/releases/tag/v0.20.0)** - RPM for Fedora (kernel 6.18+)

Based on [FlyGoat/RyzenAdj](https://github.com/FlyGoat/RyzenAdj) v0.18.0 | [Upstream Wiki](https://github.com/FlyGoat/RyzenAdj/wiki)

## Krackan Point Support

| Property | Value |
|----------|-------|
| Product | AMD Ryzen AI 5 340 / AI 7 350 |
| Architecture | Zen 5 + Zen 5c (hybrid) |
| CPU Family / Model | 0x1A / 0x60 |
| PM Table | 0x650005 / 0xD80 |

**This fork includes:**
- RyzenAdj with PM table fix for Krackan Point
- ryzen_smu v0.2.0 kernel module (DKMS)
- tuned profiles with auto-switching
- KDE widget for power monitoring

## Installation

### RPM Package (Fedora - Recommended)

```bash
# Install
sudo dnf install ryzenadj-ryzen_smu-ai300-krackan-PP-0.20.0-1.fc43.x86_64.rpm

# Verify
sudo ryzenadj -i
tuned-adm active

# Optional: KDE widget
/usr/share/ryzenadj/install-widget.sh
```

### Build from Source

```bash
# Prerequisites (Fedora)
sudo dnf install cmake gcc-c++ pciutils-devel dkms kernel-devel

# Build
git clone https://github.com/labonsky/ryzenadj_AI300.git
cd ryzenadj_AI300
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo cp ryzenadj /usr/bin/
cd ..

# Install kernel module
cd ryzen_smu && sudo ./install.sh && cd ..

# Install tuned profiles (Fedora)
cd tuned-profiles && sudo ./install.sh && cd ..
```

### Secure Boot

```bash
sudo mokutil --import /var/lib/dkms/mok.pub
# Reboot and enroll in MOK manager
```

## Power Profiles

| Profile | STAPM | Fast | Slow | Screen |
|---------|-------|------|------|--------|
| `ryzenadj-battery` | 3W | 5W | 3W | 60Hz |
| `ryzenadj-ac` | 53W | 53W | 35W | 120Hz |

Auto-switching via udev on AC plug/unplug. Manual control:

```bash
sudo tuned-adm profile ryzenadj-battery
sudo tuned-adm profile ryzenadj-ac
tuned-adm active
```

### AMD P-State EPP

On kernel 6.3+, `amd-pstate-epp` handles frequency scaling while ryzenadj controls power budget. The tuned profiles coordinate both automatically.

## Usage

```bash
# Show current power metrics
sudo ryzenadj -i

# Set power limits (milliwatts)
sudo ryzenadj --stapm-limit=45000 --fast-limit=45000 --slow-limit=45000

# All options
ryzenadj -h
```

## Documentation

- [KRACKAN_POINT_SUPPORT.md](KRACKAN_POINT_SUPPORT.md) - Detailed hardware/software info
- [WIDGET_SETUP.md](WIDGET_SETUP.md) - KDE power widget setup

## License

- RyzenAdj: LGPL-3.0
- ryzen_smu: GPL-2.0
