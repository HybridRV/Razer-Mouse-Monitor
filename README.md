# Razer Mouse Monitor

A lightweight Python tray application that monitors your Razer mouse battery in real-time and displays it using custom colored icons.

## Features

- Real-time battery monitoring from Razer Synapse logs
- Tray icon changes color based on battery level
- Charging vs. normal battery state icons
- DPI-aware icon scaling for crisp display
- Minimal setup, fully portable

---

## Installation

1. Download the latest release from the [Releases](https://github.com/MDMason92/Razer-Mouse-Monitor/releases) page.
2. Extract the zip file to any folder on your PC.
3. Make sure the `images/` folder is in the same directory as `battery_monitor.exe`.
4. Double-click `battery_monitor.exe` to run the program.
5. (Optional) To run on startup:
   - Right-click the tray icon → select **Run on Startup**, or
   - Place a shortcut to `battery_monitor.exe` in:
     ```
     %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
     ```

---

## Usage

Run the battery monitor script:
`python battery_monitor.pyw`

The tray icon will appear and update based on your mouse battery level.

Hover over the tray icon to see:
   - Device name (e.g., Mouse)  
   - Battery percentage  
   - Charging state

Right-click the tray icon to access the menu:
   - Run on Startup – toggle automatic launch at Windows login  
   - Restart – restart the tray app  
   - Quit – close the tray app completely

The Run on Startup toggle creates or removes a shortcut in the Windows Startup folder automatically, so no manual setup is required.

---

## Icon Customization

- Icons are located in `battery_icons_colored/`.
- You can replace them with your own PNGs, keeping the same filenames for proper functionality.


## Planned Features
- Low battery notifications (popup or sound alert)
- Configurable thresholds for icon colors
- Improved charging icons and animations
- Multi-device support (for multiple Razer peripherals)
- Battery history logging
- Battery drain estimate


---

## Notes

- This program has only been tested on the **Razer Basilisk V3 Pro** and **Razer Synapse 3**.  
- Other Razer devices may work, but functionality is **not guaranteed** until further testing is completed.  
- If you experience issues with other devices, please open an issue in the repository so it can be tracked.


## License

[MIT License](LICENSE)
