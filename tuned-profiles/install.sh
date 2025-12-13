#!/bin/bash
# Install ryzenadj tuned profiles for Fedora
# Run with sudo

set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (sudo ./install.sh)"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing ryzenadj tuned profiles..."

# Copy profiles
cp -r "$SCRIPT_DIR/ryzenadj-battery" /etc/tuned/profiles/
cp -r "$SCRIPT_DIR/ryzenadj-balanced" /etc/tuned/profiles/
cp -r "$SCRIPT_DIR/ryzenadj-ac" /etc/tuned/profiles/

# Make scripts executable
chmod +x /etc/tuned/profiles/ryzenadj-battery/script.sh
chmod +x /etc/tuned/profiles/ryzenadj-balanced/script.sh
chmod +x /etc/tuned/profiles/ryzenadj-ac/script.sh

# Install udev rules for auto-switching and RAPL permissions
cp "$SCRIPT_DIR/99-ryzenadj-power.rules" /etc/udev/rules.d/
cp "$SCRIPT_DIR/99-ryzenadj-rapl.rules" /etc/udev/rules.d/

# Install ppd.conf for KDE power profiles integration
cp "$SCRIPT_DIR/ppd.conf" /etc/tuned/

# Install boot-time profile check
cp "$SCRIPT_DIR/ryzenadj-boot-check.sh" /usr/bin/
chmod +x /usr/bin/ryzenadj-boot-check.sh
cp "$SCRIPT_DIR/ryzenadj-boot-check.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable ryzenadj-boot-check.service

# Reload services
udevadm control --reload-rules
systemctl restart tuned
systemctl restart tuned-ppd 2>/dev/null || true

echo ""
echo "Installation complete!"
echo ""
echo "Available profiles:"
tuned-adm list | grep ryzenadj
echo ""
echo "Usage:"
echo "  sudo tuned-adm profile ryzenadj-battery  # Low power (5W)"
echo "  sudo tuned-adm profile ryzenadj-ac       # Full power (53W)"
echo ""
echo "Auto-switching enabled via udev rules."
echo "KDE Power Profiles GUI also works."
