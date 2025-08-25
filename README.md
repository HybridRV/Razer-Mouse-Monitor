# Razer Mouse Monitor

A lightweight Python tray application that monitors your Razer mouse battery in real-time and displays it using custom colored icons.

## Features

- Real-time battery monitoring from Razer Synapse logs
- Tray icon changes color based on battery level
- Charging vs. normal battery state icons
- DPI-aware icon scaling for crisp display
- Minimal setup, fully portable

## Requirements

- Python 3.8+


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MDMason92/Razer-Mouse-Monitor.git
   cd Razer-Mouse-Monitor
   ```
2. Install dependencies:

- [Pillow](https://pillow.readthedocs.io/) (`pip install Pillow`)
- [pystray](https://pypi.org/project/pystray/) (`pip install pystray`)


3. Ensure the `battery_icons_colored` folder is in the same directory as the script.

## Usage

1. Run the battery monitor script:
`python battery_monitor.pyw`

2. The tray icon will appear and update based on your mouse battery level.

3. Hover over the tray icon to see:
   - Device name (e.g., Mouse)  
   - Battery percentage  
   - Charging state

4. Right-click the tray icon to access the menu:
   - Run on Startup – toggle automatic launch at Windows login  
   - Restart – restart the tray app  
   - Quit – close the tray app completely

5. The Run on Startup toggle creates or removes a shortcut in the Windows Startup folder automatically, so no manual setup is required.

---

## Icon Customization

- Icons are located in `battery_icons_colored/`.
- You can replace them with your own PNGs, keeping the same filenames for proper functionality.

## License

[MIT License](LICENSE)
