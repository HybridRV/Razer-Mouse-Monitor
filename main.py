import os
import time
import threading
import re
from pathlib import Path
from PIL import Image
import pystray

# ------------------------------
# CONFIG
# ------------------------------
LOG_FILE = Path.home() / "AppData/Local/Razer/Synapse3/Log/Razer Synapse 3.log"

ICON_PATHS = {
    "green": "green.png",
    "yellow": "yellow.png",
    "brown": "brown.png",
    "red": "red.png"
}

# ------------------------------
# GLOBAL STATE
# ------------------------------
battery_status = {
    "percent": "?",
    "state": "Unknown"
}

ICONS = {}

# ------------------------------
# PARSE BATTERY LINES
# ------------------------------
battery_regex = re.compile(r"level (\d+)\s+state (\d+)")

def parse_battery_line(line):
    match = battery_regex.search(line)
    if match:
        level = int(match.group(1))
        state_code = int(match.group(2))
        state = "Charging" if state_code else "Not Charging"
        return {"percent": level, "state": state}
    return None

# ------------------------------
# READ LATEST BATTERY
# ------------------------------
def get_latest_battery():
    if not LOG_FILE.exists():
        return None
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in reversed(f.readlines()):
            status = parse_battery_line(line)
            if status:
                return status
    return None

# ------------------------------
# ICON SELECTION
# ------------------------------
def get_icon_for_percent(percent):
    if percent >= 80:
        return ICONS["green"]
    elif percent >= 50:
        return ICONS["yellow"]
    elif percent >= 25:
        return ICONS["orange"]
    else:
        return ICONS["red"]

# ------------------------------
# TAIL LOG
# ------------------------------
def tail_battery_log(icon):
    if not LOG_FILE.exists():
        return
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            status = parse_battery_line(line)
            if status:
                battery_status.update(status)
                percent = battery_status['percent'] if isinstance(battery_status['percent'], int) else 0
                icon.icon = get_icon_for_percent(percent)
                icon.title = f"Battery: {battery_status['percent']}% ({battery_status['state']})"

# ------------------------------
# MAIN
# ------------------------------
def main():
    # Preload icons
    for key, path in ICON_PATHS.items():
        img = Image.open(path).convert("RGBA").resize((16, 16), Image.LANCZOS)
        ICONS[key] = img

    # Initial icon
    initial_icon = get_icon_for_percent(0)
    icon = pystray.Icon("BatteryMonitor", initial_icon, "Battery Monitor")

    # Initial battery read
    status = get_latest_battery()
    if status:
        battery_status.update(status)
        percent = battery_status['percent'] if isinstance(battery_status['percent'], int) else 0
        icon.icon = get_icon_for_percent(percent)
        icon.title = f"Battery: {battery_status['percent']}% ({battery_status['state']})"

    # Start log tailing in background
    thread = threading.Thread(target=tail_battery_log, args=(icon,), daemon=True)
    thread.start()

    # Run tray icon (blocks)
    icon.run()

if __name__ == "__main__":
    main()
