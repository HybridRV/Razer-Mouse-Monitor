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
   git clone https://github.com/your-username/repo-name.git
   cd repo-name
   ```
2. Install dependencies:

- [Pillow](https://pillow.readthedocs.io/) (`pip install Pillow`)
- [pystray](https://pypi.org/project/pystray/) (`pip install pystray`)


3. Ensure the `battery_icons_colored` folder is in the same directory as the script.

## Usage

Run the battery monitor script:

```bash
python battery_monitor.py
```
- The tray icon will update based on your mouse battery level.
- Hover over the icon to see the battery percentage and state.

## Icon Customization

- Icons are located in `battery_icons_colored/`.
- You can replace them with your own PNGs, keeping the same filenames for proper functionality.

## License

[MIT License](LICENSE)
