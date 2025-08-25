import os, sys, time, threading, re, ctypes
from pathlib import Path
from PIL import Image
import pystray
from win32com.client import Dispatch

# ------------------------------
# CONFIG
# ------------------------------
LOG_FILE = Path.home() / "AppData/Local/Razer/Synapse3/Log/Razer Synapse 3.log"
SCRIPT_DIR = Path(__file__).parent
ICON_FOLDER = SCRIPT_DIR / "battery_icons_colored"
ICON_BASE_SIZE = 32
DEVICE_NAME = "Mouse"

STARTUP_FOLDER = Path(os.getenv("APPDATA")) / "Microsoft/Windows/Start Menu/Programs/Startup"
SHORTCUT_PATH = STARTUP_FOLDER / "Mouse Battery Monitor.lnk"

battery_status = {"percent": "?", "state": "Unknown"}
ICONS = {}

# ------------------------------
# DPI scaling
# ------------------------------
def get_system_scale():
    try:
        ctypes.windll.user32.SetProcessDPIAware()
        dc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)
        ctypes.windll.user32.ReleaseDC(0, dc)
        return dpi / 96.0
    except:
        return 1.0
ICON_SIZE = int(ICON_BASE_SIZE * get_system_scale())

# ------------------------------
# Parse battery lines
# ------------------------------
battery_regex = re.compile(r"level (\d+)\s+state (\d+)")
def parse_line(line):
    m = battery_regex.search(line)
    if m:
        return {"percent": int(m.group(1)), "state": "Charging" if int(m.group(2)) else "Not Charging"}
    return None

def get_latest():
    if not LOG_FILE.exists(): return None
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for l in reversed(f.readlines()):
            s = parse_line(l)
            if s: return s
    return None

# ------------------------------
# Load icons
# ------------------------------
def load_icons():
    for f in os.listdir(ICON_FOLDER):
        if f.endswith(".png"):
            img = Image.open(ICON_FOLDER / f).convert("RGBA").resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
            ICONS[f.replace(".png", "").lower()] = img

# ------------------------------
# Icon selection
# ------------------------------
def get_icon(p, s):
    prefix = "battery-charging" if s.lower() == "charging" else "battery"
    rounded = max(10, min(100, int(round(p / 10) * 10)))
    return ICONS.get(f"{prefix}-{rounded}-icon", ICONS.get("battery-100-icon"))

# ------------------------------
# Tail battery log
# ------------------------------
def tail_log(icon):
    if not LOG_FILE.exists(): return
    with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            s = parse_line(line)
            if s:
                battery_status.update(s)
                p = battery_status['percent'] if isinstance(battery_status['percent'], int) else 0
                st = battery_status['state']
                icon.icon = get_icon(p, st)
                icon.title = f"{DEVICE_NAME} Battery: {p}% ({st})"

# ------------------------------
# Run on Startup functions
# ------------------------------
def enable_startup():
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(str(SHORTCUT_PATH))
    shortcut.Targetpath = sys.executable
    shortcut.Arguments = '"' + str(Path(__file__).resolve()) + '"'  # fixed type error
    shortcut.WorkingDirectory = str(Path(__file__).parent.resolve())
    shortcut.IconLocation = str(Path(__file__).parent / "battery_icons_colored/battery-100-icon.png")
    shortcut.save()

def disable_startup():
    if SHORTCUT_PATH.exists():
        SHORTCUT_PATH.unlink()

def is_startup_enabled():
    return SHORTCUT_PATH.exists()

def toggle_startup(icon, item):
    if is_startup_enabled():
        disable_startup()
    else:
        enable_startup()
    icon.update_menu()

# ------------------------------
# Menu actions
# ------------------------------
def quit_app(icon, item):
    icon.stop()

def restart_app(icon, item):
    icon.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)

# ------------------------------
# Main
# ------------------------------
def main():
    load_icons()
    initial_icon = get_icon(0, "Not Charging")

    menu = pystray.Menu(
        pystray.MenuItem(lambda item: "✓ Run on Startup" if is_startup_enabled() else "Run on Startup", toggle_startup),
        pystray.MenuItem("Restart", restart_app),
        pystray.MenuItem("Quit", quit_app)
    )

    icon = pystray.Icon("BatteryMonitor", initial_icon, "Mouse Battery Monitor", menu)

    status = get_latest()
    if status:
        battery_status.update(status)
        p = battery_status['percent'] if isinstance(battery_status['percent'], int) else 0
        st = battery_status['state']
        icon.icon = get_icon(p, st)
        icon.title = f"{DEVICE_NAME} Battery: {p}% ({st})"

    threading.Thread(target=tail_log, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    main()
