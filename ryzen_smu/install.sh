#!/bin/bash
# Install ryzen_smu kernel module with Krackan Point support
# Based on upstream v0.1.7 with minimal patches

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== ryzen_smu Installation Script ===${NC}"
echo "Version: 0.1.7 + Krackan Point support"
echo ""

# Check for root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: Please run as root (sudo)${NC}"
    exit 1
fi

# Check for required tools
for cmd in dkms modprobe; do
    if ! command -v $cmd &> /dev/null; then
        echo -e "${RED}Error: $cmd is required but not installed${NC}"
        exit 1
    fi
done

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="0.1.7"

echo -e "${YELLOW}[1/6] Removing old ryzen_smu installations...${NC}"
# Remove any existing DKMS modules
dkms status | grep ryzen_smu | while read -r line; do
    ver=$(echo "$line" | grep -oP 'ryzen_smu[,/]\s*\K[0-9.]+')
    if [ -n "$ver" ]; then
        echo "  Removing ryzen_smu version $ver"
        dkms remove ryzen_smu/$ver --all 2>/dev/null || true
    fi
done

# Unload module if loaded
if lsmod | grep -q ryzen_smu; then
    echo "  Unloading ryzen_smu module"
    modprobe -r ryzen_smu 2>/dev/null || true
fi

# Clean up old source directories
rm -rf /usr/src/ryzen_smu-* /usr/src/ryzen_smu

echo -e "${YELLOW}[2/6] Copying source to /usr/src/ryzen_smu-${VERSION}...${NC}"
mkdir -p /usr/src/ryzen_smu-${VERSION}
cp -r "$SCRIPT_DIR"/{smu.c,smu.h,drv.c,Makefile,dkms.conf,lib,LICENSE} /usr/src/ryzen_smu-${VERSION}/

# Fix version in dkms.conf
sed -i "s/@VERSION@/${VERSION}/g" /usr/src/ryzen_smu-${VERSION}/dkms.conf

echo -e "${YELLOW}[3/6] Adding module to DKMS...${NC}"
dkms add ryzen_smu/${VERSION}

echo -e "${YELLOW}[4/6] Building module...${NC}"
dkms build ryzen_smu/${VERSION}

echo -e "${YELLOW}[5/6] Installing module...${NC}"
dkms install ryzen_smu/${VERSION}

echo -e "${YELLOW}[6/6] Loading module...${NC}"
modprobe ryzen_smu

echo ""
echo -e "${GREEN}=== Installation Complete ===${NC}"
echo ""

# Verification
echo "Verification:"
if lsmod | grep -q ryzen_smu; then
    echo -e "  Module loaded: ${GREEN}YES${NC}"
else
    echo -e "  Module loaded: ${RED}NO${NC}"
fi

if [ -d /sys/kernel/ryzen_smu_drv ]; then
    echo -e "  Sysfs interface: ${GREEN}YES${NC}"

    if [ -f /sys/kernel/ryzen_smu_drv/codename ]; then
        CODENAME=$(cat /sys/kernel/ryzen_smu_drv/codename 2>/dev/null)
        echo "  Codename value: $CODENAME"
    fi
else
    echo -e "  Sysfs interface: ${RED}NO${NC}"
fi

echo ""
echo "Kernel messages (last 10 lines):"
dmesg | grep -i ryzen_smu | tail -10

echo ""
echo -e "${GREEN}Done!${NC}"
