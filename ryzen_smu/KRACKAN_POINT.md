# Krackan Point Support Patches

This directory contains [amkillam/ryzen_smu](https://github.com/amkillam/ryzen_smu) v0.1.7 with patches for **Krackan Point** (AMD Ryzen AI 300 series) support.

## Hardware Info

| Property | Value |
|----------|-------|
| Codename | Krackan Point |
| Product | AMD Ryzen AI 300 Series |
| Architecture | Zen 5 |
| CPU Family | 0x1A |
| CPU Model | 0x60 (96) |

## SMU Configuration

Based on Strix Point/Strix Halo (same Zen 5 generation):

| Setting | Value |
|---------|-------|
| RSMU CMD | 0x3B10A20 |
| RSMU RSP | 0x3B10A80 |
| RSMU ARG | 0x3B10A88 |
| MP1 IF Version | 13 |
| MP1 CMD | 0x3b10928 |
| MP1 RSP | 0x3b10978 |
| MP1 ARG | 0x3b10998 |
| HSMP | Not supported (skip) |
| DRAM Base Fn | 0x66 |
| Transfer Fn | 0x65 (arg0=3) |
| PM Version Fn | 0x06 |
| PM Table Version | 0x650005 |
| PM Table Size | 0xD80 (3456 bytes) |

## Patches Applied

**Total: 12 insertions across 4 files**

### smu.h
- Line 94: Added `CODENAME_KRACKANPOINT` to enum

### smu.c
1. Line 363-365: CPU model 0x60 detection
2. Line 426: RSMU mailbox configuration
3. Line 476: HSMP skip (goto MP1_DETECT)
4. Line 542: MP1 mailbox configuration
5. Line 616: Codename string "Krackan Point"
6. Line 692: DRAM base address (fn=0x66)
7. Line 810: Transfer table (arg0=3, fn=0x65)
8. Line 906: PM table version (fn=0x06)
9. Line 1168-1176: PM table size (0x650005 → 0xD80)

### lib/libsmu.h
- Line 104: Added `CODENAME_KRACKANPOINT` to enum

### lib/libsmu.c
- Line 481-482: Codename string "Krackan Point"

## Installation

```bash
sudo ./install.sh
```

## Verification

```bash
# Module loaded
lsmod | grep ryzen_smu

# Sysfs created
ls /sys/kernel/ryzen_smu_drv/

# Codename detected (should show 28 for KRACKANPOINT)
cat /sys/kernel/ryzen_smu_drv/codename

# Kernel messages
dmesg | grep -i "ryzen_smu\|krackan"
```

## Contributing Back

If these patches work for you, consider submitting a PR to upstream:
https://github.com/amkillam/ryzen_smu
