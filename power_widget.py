import sys
import time
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPainter, QPixmap, QColor, QFont
from PyQt6.QtCore import QTimer, Qt

# Path to temporary energy file
RAPL_PATH = "/tmp/ryzenadj_power.txt"

def get_energy_uj():
    try:
        with open(RAPL_PATH, 'r') as f:
            content = f.read().strip()
            if not content: return 0
            return int(content)
    except Exception:
        return 0

class PowerTray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.last_energy = get_energy_uj()
        self.last_time = time.time()
        self.first_run = True

        # Set up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_power)
        self.timer.start(1000)  # 1 second

        # Menu
        menu = QMenu()
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(menu)

        # Set initial placeholder icon
        self.update_icon(0) 
        self.setVisible(True)
        
        # Start timer
        self.timer.start(1000)

    def update_power(self):
        print("Timer ticked")
        current_energy = get_energy_uj()
        current_time = time.time()

        if self.first_run:
            self.first_run = False
            self.last_energy = current_energy
            self.last_time = current_time
            return

        diff_energy = current_energy - self.last_energy
        diff_time = current_time - self.last_time
        
        # Prevent division by zero
        if diff_time <= 0:
            return

        watts = (diff_energy / 1000000.0) / diff_time
        
        self.last_energy = current_energy
        self.last_time = current_time

        # Update Icon
        self.update_icon(watts)
        self.setToolTip(f"CPU Power: {watts:.2f} W")

    def update_icon(self, watts):
        # Create a pixmap to draw on
        size = 64
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw Background (Solid Dark Gray)
        painter.setBrush(QColor("#202020"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, size, size)

        # Text Config
        text = f"{int(watts)}W" if watts >= 10 else f"{watts:.1f}W"
        font = QFont("Sans Serif", 26, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Color based on usage
        painter.setPen(QColor("#FFFFFF")) # White

        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
        painter.end()

        self.setIcon(QIcon(pixmap))
        # self.setIcon(QIcon.fromTheme("applications-system"))

if __name__ == "__main__":
    try:
        print("Initializing QApplication...")
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        print("Creating Tray Icon...")
        tray = PowerTray()
        
        print("Widget started successfully. Entering event loop...")
        sys.exit(app.exec())
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()