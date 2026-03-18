# TWATCH-2020-WiFi-Monitor

A simple MicroPython app for the **LilyGO T-WATCH-2020** that displays:
- 📅 Date (manually set)
- 📡 Signal strength (dBm) of a target WiFi SSID
- 🔋 Battery percentage (calculated from voltage)

![TWATCH-2020 WiFi Monitor](screenshot.png)

---

## Hardware

- [LilyGO T-WATCH-2020](https://www.aliexpress.us/item/3256802898629918.html)
- USB-C cable

---

## Prerequisites

### MicroPython Firmware

Flash the TWATCH-2020 specific firmware from the [russhughes st7789_mpy repo](https://github.com/russhughes/st7789_mpy/tree/master/firmware/TWATCH-2020).

This firmware has the `st7789` display driver built in, which is required.

### Required Libraries on the device

The following must be present on the device filesystem:

- `axp202c.py` — AXP202 power management driver
- `fonts/lily_go_watch_vga1_bold_16x32.py` — font for the watch screen

Both are available from the [BB-ESP32-KIOSK repo](https://github.com/jouellnyc/BB-ESP32-KIOSK) — grab the `fonts/` and `lib/` folders from there.

### IDE

Use [Thonny](https://thonny.org/) to upload files and interact with the REPL.

---

## Installation

1. Clone or download this repo
2. Upload the following files to the **root** of the device using Thonny:
   - `main.py`
   - `watch_display.py`
   - `time_wifi_display.py`
3. Make sure `axp202c.py` and `fonts/lily_go_watch_vga1_bold_16x32.py` are also on the device

---

## Configuration

Edit the top of `time_wifi_display.py` before uploading:

```python
# --- Set date manually here ---
MONTH = 3
DAY   = 17

# --- Set your target SSID here ---
TARGET_SSID = "Jinxy-64"
```

- **MONTH / DAY** — set to today's date (the watch has no RTC battery so date resets on power off)
- **TARGET_SSID** — the exact name of the WiFi network you want to monitor

---

## How It Works

### `main.py`
Entry point. Imports `watch_display` to initialize the hardware, then imports `time_wifi_display` to run the app.

### `watch_display.py`
Handles all hardware initialization:
- Powers on the display via the **AXP202** power management chip
- Initializes the **ST7789** 240x240 display over SPI
- Exposes the `display` object with `display.tft` and `display.axp`

### `time_wifi_display.py`
The main app loop:
- Activates WiFi in STA mode
- Every **15 seconds**: scans for the target SSID and reads battery voltage
- Updates the display with signal strength (dBm) and battery %

---

## Display Layout

```
┌─────────────────────────┐
│ DATE: Mar 17            │
├─────────────────────────┤
│ Jinxy-64                │
│                         │
│ -35 dBm                 │
│                         │
├─────────────────────────┤
│ BATTERY: 100%           │
└─────────────────────────┘
```

### Signal Strength Colors
| dBm | Color | Quality |
|-----|-------|---------|
| > -60 | 🟢 Green | Good |
| -60 to -70 | 🟡 Yellow | Fair |
| < -70 | 🔴 Red | Weak |

### Battery Colors
| % | Color |
|---|-------|
| > 50% | 🟢 Green |
| 20–50% | 🟡 Yellow |
| < 20% | 🔴 Red |

---

## Notes

- The **AXP202** power chip must be initialized from a cold boot — soft resets via Thonny will not reinitialize the display. Always power cycle the watch to run the app.
- WiFi scanning takes ~2–3 seconds on the ESP32, so scanning more frequently than every 10 seconds will cause the display to pause briefly.
- The watch does not have an RTC battery, so the clock resets to `00:00:00` on each boot. Set `MONTH` and `DAY` manually each day.
- Battery % is calculated from voltage: `4.2V = 100%`, `3.5V = 0%`. Values are clamped to 0–100%.
- Press the **side button (Pin 36)** to exit the app gracefully back to the REPL.

---

## Based On

This project was built on top of the hardware init patterns from:
- [BB-ESP32-KIOSK](https://github.com/jouellnyc/BB-ESP32-KIOSK) by [@jouellnyc](https://github.com/jouellnyc)
- [st7789_mpy](https://github.com/russhughes/st7789_mpy) by [@russhughes](https://github.com/russhughes)
- NOTE: This was purely AI driven by Claude but used my guidance and knowledge of the above projects.
---

## License

MIT

