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
cp -r "$SCRIPT_DIR/ryzenadj-ac" /etc/tuned/profiles/

# Make scripts executable
chmod +x /etc/tuned/profiles/ryzenadj-battery/script.sh
chmod +x /etc/tuned/profiles/ryzenadj-ac/script.sh

# Install udev rules
cp "$SCRIPT_DIR/99-ryzenadj-power.rules" /etc/udev/rules.d/

# Reload
udevadm control --reload-rules
systemctl restart tuned

echo ""
echo "Installation complete!"
echo ""
echo "Available profiles:"
tuned-adm list | grep ryzenadj
echo ""
echo "To activate battery profile: sudo tuned-adm profile ryzenadj-battery"
echo "To activate AC profile:      sudo tuned-adm profile ryzenadj-ac"
echo ""
echo "Auto-switching is enabled via udev rules."
