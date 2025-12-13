#!/bin/bash
# Install RyzenAdj Power Monitor widget for KDE Plasma

set -e

WIDGET_NAME="com.github.zren.commandoutput"
WIDGET_DIR="$HOME/.local/share/plasma/plasmoids/$WIDGET_NAME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for widget source in multiple locations
if [ -d "$SCRIPT_DIR/widget/$WIDGET_NAME" ]; then
    WIDGET_SRC="$SCRIPT_DIR/widget/$WIDGET_NAME"
elif [ -d "$SCRIPT_DIR/$WIDGET_NAME" ]; then
    WIDGET_SRC="$SCRIPT_DIR/$WIDGET_NAME"
elif [ -d "/usr/share/ryzenadj/widget/$WIDGET_NAME" ]; then
    WIDGET_SRC="/usr/share/ryzenadj/widget/$WIDGET_NAME"
else
    echo "Error: Widget source not found"
    exit 1
fi

echo "Installing RyzenAdj Power Monitor widget..."

# Create plasmoids directory if needed
mkdir -p "$HOME/.local/share/plasma/plasmoids"

# Remove old version if exists
if [ -d "$WIDGET_DIR" ]; then
    echo "Removing old widget version..."
    rm -rf "$WIDGET_DIR"
fi

# Install widget
cp -r "$WIDGET_SRC" "$WIDGET_DIR"

echo ""
echo "Widget installed successfully!"
echo ""
echo "To add the widget to your panel:"
echo "1. Right-click on your KDE panel"
echo "2. Select 'Add Widgets...'"
echo "3. Search for 'Command Output'"
echo "4. Drag it to your panel"
echo ""
echo "The widget is pre-configured to show: Laptop | CPU | Temp"
echo "Example output: 7.2 W | 3.5 W | 37°C"
echo ""
echo "To restart Plasma shell (optional):"
echo "  kquitapp6 plasmashell && kstart6 plasmashell"
