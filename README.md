# RyzenAdj - Krackan Point (AMD Ryzen AI 300) Fork

Adjust power management settings for Ryzen Mobile Processors.

**This fork adds full support for AMD Ryzen AI 300 series (Krackan Point) processors.**

Based on: [FlyGoat/RyzenAdj](https://github.com/FlyGoat/RyzenAdj) v0.18.0

## Krackan Point Support

| Property | Value |
|----------|-------|
| Codename | Krackan Point |
| Product | AMD Ryzen AI 300 Series |
| Architecture | Zen 5 |
| CPU Family | 0x1A |
| CPU Model | 0x60 (96) |
| PM Table Version | 0x650005 |
| PM Table Size | 0xD80 (3456 bytes) |

### Changes from Upstream

- **RyzenAdj**: Added PM table size for version 0x650005
- **ryzen_smu**: Included patched v0.1.7 with full Krackan Point support
- **Power Automation**: Systemd service for automatic power management

For GUI options see [Universal x86 Tuning Utility](https://github.com/JamesCJ60/Universal-x86-Tuning-Utility) or [ryzen-controller](https://gitlab.com/ryzen-controller-team/ryzen-controller/).

## Usage
The command line interface is identical on both Windows and Unix-Like OS.

You should run it with Administrator on Windows or root on Linux.

You can write a shell script or bat to do it automatically.

```
$./ryzenadj -h
Usage: ryzenadj [options]

 Ryzen Power Management adjust tool.

    -h, --help                            show this help message and exit

Options
    -i, --info                            Show information and most important power metrics after adjustment
    --dump-table                          Show whole power metric table before and after adjustment

Settings
    -a, --stapm-limit=<u32>               Sustained Power Limit         - STAPM LIMIT (mW)
    -b, --fast-limit=<u32>                Actual Power Limit            - PPT LIMIT FAST (mW)
    -c, --slow-limit=<u32>                Average Power Limit           - PPT LIMIT SLOW (mW)
    -d, --slow-time=<u32>                 Slow PPT Constant Time (s)
    -e, --stapm-time=<u32>                STAPM constant time (s)
    -f, --tctl-temp=<u32>                 Tctl Temperature Limit (degree C)
    -g, --vrm-current=<u32>               VRM Current Limit             - TDC LIMIT VDD (mA)
    -j, --vrmsoc-current=<u32>            VRM SoC Current Limit         - TDC LIMIT SoC (mA)
    -k, --vrmmax-current=<u32>            VRM Maximum Current Limit     - EDC LIMIT VDD (mA)
    -l, --vrmsocmax-current=<u32>         VRM SoC Maximum Current Limit - EDC LIMIT SoC (mA)
    -m, --psi0-current=<u32>              PSI0 VDD Current Limit (mA)
    -n, --psi0soc-current=<u32>           PSI0 SoC Current Limit (mA)
    -o, --max-socclk-frequency=<u32>      Maximum SoC Clock Frequency (MHz)
    -p, --min-socclk-frequency=<u32>      Minimum SoC Clock Frequency (MHz)
    -q, --max-fclk-frequency=<u32>        Maximum Transmission (CPU-GPU) Frequency (MHz)
    -r, --min-fclk-frequency=<u32>        Minimum Transmission (CPU-GPU) Frequency (MHz)
    -s, --max-vcn=<u32>                   Maximum Video Core Next (VCE - Video Coding Engine) (MHz)
    -t, --min-vcn=<u32>                   Minimum Video Core Next (VCE - Video Coding Engine) (MHz)
    -u, --max-lclk=<u32>                  Maximum Data Launch Clock (MHz)
    -v, --min-lclk=<u32>                  Minimum Data Launch Clock (MHz)
    -w, --max-gfxclk=<u32>                Maximum GFX Clock (MHz)
    -x, --min-gfxclk=<u32>                Minimum GFX Clock (MHz)
    -y, --prochot-deassertion-ramp=<u32>  Ramp Time After Prochot is Deasserted: limit power based on value, higher values does apply tighter limits after prochot is over
    --apu-skin-temp=<u32>                 APU Skin Temperature Limit    - STT LIMIT APU (degree C)
    --dgpu-skin-temp=<u32>                dGPU Skin Temperature Limit   - STT LIMIT dGPU (degree C)
    --apu-slow-limit=<u32>                APU PPT Slow Power limit for A+A dGPU platform - PPT LIMIT APU (mW)
    --skin-temp-limit=<u32>               Skin Temperature Power Limit (mW)
    --power-saving                        Hidden options to improve power efficiency (is set when AC unplugged): behavior depends on CPU generation, Device and Manufacture
    --max-performance                     Hidden options to improve performance (is set when AC plugged in): behavior depends on CPU generation, Device and Manufacture
```

### Demo
If I'm going to set all the Power Limit to 45W, and Tctl to 90 °C,
then the command line should be:

    ./ryzenadj --stapm-limit=45000 --fast-limit=45000 --slow-limit=45000 --tctl-temp=90

### Documentation
- [Supported Models](https://github.com/FlyGoat/RyzenAdj/wiki/Supported-Models)
- [Renoir Tuning Guide](https://github.com/FlyGoat/RyzenAdj/wiki/Renoir-Tuning-Guide)
- [Options](https://github.com/FlyGoat/RyzenAdj/wiki/Options)
- [FAQ](https://github.com/FlyGoat/RyzenAdj/wiki/FAQ)

## Quick Start (Krackan Point / Ryzen AI 300)

### Prerequisites

**Fedora:**
```bash
sudo dnf install cmake gcc-c++ pciutils-devel dkms kernel-devel kernel-headers
```

**Ubuntu/Debian:**
```bash
sudo apt install build-essential cmake libpci-dev dkms linux-headers-$(uname -r)
```

**Arch:**
```bash
sudo pacman -S base-devel pciutils cmake dkms linux-headers
```

### Installation

```bash
# Clone this repository
git clone https://github.com/labonsky/ryzenadj_AI300.git
cd ryzenadj_AI300

# Build RyzenAdj
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo cp ryzenadj /usr/local/bin/
cd ..

# Install ryzen_smu kernel module (recommended for Krackan Point)
cd ryzen_smu
sudo ./install.sh
cd ..

# Test
sudo ryzenadj -i
```

### Verify Installation

```bash
# Check RyzenAdj
sudo ryzenadj -i

# Check ryzen_smu module
lsmod | grep ryzen_smu
cat /sys/kernel/ryzen_smu_drv/codename

# Should show power metrics and detect "Krackan Point"
```

### Secure Boot

If using Secure Boot, enroll the DKMS signing key:

```bash
sudo mokutil --import /var/lib/dkms/mok.pub
# Reboot and enroll in MOK manager
```

---

## Power Automation (Fedora/tuned Integration)

This fork includes tuned profiles that integrate with Fedora's power management, automatically adjusting power limits based on AC/battery status.

### Power Profiles

| Profile | Inherits | STAPM | Fast | Slow | Screen |
|---------|----------|-------|------|------|--------|
| `ryzenadj-battery` | powersave | 5W | 10W | 5W | 60Hz |
| `ryzenadj-ac` | balanced | 53W | 53W | 35W | 120Hz |

### Power Limit Explanation

| Limit | Description |
|-------|-------------|
| **PPT FAST** | Maximum burst power (milliseconds) - instant responsiveness |
| **PPT SLOW** | Average power over seconds - short-term workloads |
| **STAPM** | Sustained thermal power (minutes) - long-term heat management |

### Setup (Fedora with tuned)

```bash
# Create profile directories
sudo mkdir -p /etc/tuned/profiles/ryzenadj-battery
sudo mkdir -p /etc/tuned/profiles/ryzenadj-ac

# Battery profile (inherits Fedora's powersave settings)
sudo tee /etc/tuned/profiles/ryzenadj-battery/tuned.conf << 'EOF'
[main]
summary=Battery power saving with ryzenadj (5W sustain, 10W burst)
include=powersave

[script]
script=${i:PROFILE_DIR}/script.sh
EOF

sudo tee /etc/tuned/profiles/ryzenadj-battery/script.sh << 'EOF'
#!/bin/bash
case "$1" in
    start)
        /usr/local/bin/ryzenadj --stapm-limit=5000 --fast-limit=10000 --slow-limit=5000 2>/dev/null
        # Adjust username and display settings as needed
        sudo -u $USER XDG_RUNTIME_DIR=/run/user/$(id -u $USER) WAYLAND_DISPLAY=wayland-0 kscreen-doctor output.eDP-1.mode.2 2>/dev/null
        ;;
esac
exit 0
EOF
sudo chmod +x /etc/tuned/profiles/ryzenadj-battery/script.sh

# AC profile (inherits Fedora's balanced settings)
sudo tee /etc/tuned/profiles/ryzenadj-ac/tuned.conf << 'EOF'
[main]
summary=AC full power with ryzenadj (53W defaults)
include=balanced

[cpu]
boost=1

[script]
script=${i:PROFILE_DIR}/script.sh
EOF

sudo tee /etc/tuned/profiles/ryzenadj-ac/script.sh << 'EOF'
#!/bin/bash
case "$1" in
    start)
        /usr/local/bin/ryzenadj --stapm-limit=53000 --fast-limit=53000 --slow-limit=35000 2>/dev/null
        # Adjust username and display settings as needed
        sudo -u $USER XDG_RUNTIME_DIR=/run/user/$(id -u $USER) WAYLAND_DISPLAY=wayland-0 kscreen-doctor output.eDP-1.mode.1 2>/dev/null
        ;;
esac
exit 0
EOF
sudo chmod +x /etc/tuned/profiles/ryzenadj-ac/script.sh

# Verify profiles are available
tuned-adm list | grep ryzenadj
```

### Auto-Switching (udev)

Create udev rules to automatically switch profiles on plug/unplug:

```bash
sudo tee /etc/udev/rules.d/99-ryzenadj-power.rules << 'EOF'
# Switch to battery profile when unplugged
ACTION=="change", SUBSYSTEM=="power_supply", ATTR{type}=="Mains", ATTR{online}=="0", RUN+="/usr/sbin/tuned-adm profile ryzenadj-battery"

# Switch to AC profile when plugged in
ACTION=="change", SUBSYSTEM=="power_supply", ATTR{type}=="Mains", ATTR{online}=="1", RUN+="/usr/sbin/tuned-adm profile ryzenadj-ac"
EOF

sudo udevadm control --reload-rules
```

### Manual Profile Switching

```bash
# Switch to battery mode
sudo tuned-adm profile ryzenadj-battery

# Switch to AC mode
sudo tuned-adm profile ryzenadj-ac

# Check current profile
tuned-adm active

# Verify power limits
sudo ryzenadj -i
```

### Fedora Powersave Features (Inherited)

The `ryzenadj-battery` profile inherits these additional power savings from Fedora's powersave profile:

| Setting | Effect |
|---------|--------|
| `governor=powersave` | CPU frequency scaling |
| `boost=0` | Disables turbo boost |
| `platform_profile=low-power` | ACPI power mode |
| `panel_power_savings=3` | Display power saving |
| `vm.laptop_mode=5` | Aggressive disk caching |
| `radeon_powersave=dpm-battery` | GPU power saving |
| `alpm=med_power_with_dipm` | SATA link power management |

### Legacy: Standalone Power Feeder (Alternative)

For non-Fedora systems or if you prefer a standalone service, see `power_feeder.py` in this repository.

---

## Standard Installation

### Linux

RyzenAdj needs elevated access to the SMU. Two methods are supported:

1. **ryzen_smu kernel module** (recommended) - Included in this repo with Krackan Point support
2. **/dev/mem** (fallback) - Requires `iomem=relaxed` kernel parameter

RyzenAdj will try ryzen_smu first, then fallback to /dev/mem.

#### Build from Source

```bash
git clone https://github.com/labonsky/ryzenadj_AI300.git
cd ryzenadj_AI300
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
sudo cp ryzenadj /usr/local/bin/
```

#### Install ryzen_smu (Krackan Point Patched)

The included `ryzen_smu/` directory contains [amkillam/ryzen_smu](https://github.com/amkillam/ryzen_smu) v0.1.7 with Krackan Point patches.

```bash
cd ryzen_smu
sudo ./install.sh
```

Or manually:

```bash
cd ryzen_smu
sudo dkms add .
sudo dkms build ryzen_smu/0.1.7
sudo dkms install ryzen_smu/0.1.7
sudo modprobe ryzen_smu
```

#### Upstream ryzen_smu (Other Processors)

For non-Krackan Point processors, you can use upstream:

```bash
git clone https://github.com/amkillam/ryzen_smu
cd ryzen_smu && sudo make dkms-install
```

### Windows

It can be built by Visual Studio + MSVC automaticaly, or Clang + Nmake in command line.
However, as for now, MingW-gcc can't be used to compile for some reason.

Required dll is included in ./win32 of source tree. Please put the dll
library and sys driver in the same folder with ryzenadj.exe.

We don't recommend you to build by yourself on Windows since the environment configuarion
is very complicated. If you would like to use ryzenadj functions in your program, see libryzenadj.
