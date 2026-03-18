"""time_wifi_display.py"""
import time
import network
from machine import Pin
from watch_display import display
from st7789 import color565
import fonts.lily_go_watch_vga1_bold_16x32 as font

# --- Set date manually here ---
MONTH = 3
DAY   = 17

white    = color565(255, 255, 255)
drk_grn  = color565(50, 100, 30)
red      = color565(255, 0,   0)
yellow   = color565(255, 255, 0)
green    = color565(0, 255,   0)

tft         = display.tft
BTN_PIN     = 36
TARGET_SSID = "$SSID"
btn  = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

def rssi_color(rssi):
    if rssi is None:   return red
    elif rssi >= -60:  return green
    elif rssi >= -70:  return yellow
    else:              return red

def battery_color(pct):
    if pct is None:  return red
    elif pct >= 50:  return green
    elif pct >= 20:  return yellow
    else:            return red

def draw_static():
    tft.fill(drk_grn)
    tft.hline(  0,   0, 239, white)
    tft.hline(  0, 237, 239, white)
    tft.vline(  0,   0, 239, white)
    tft.vline(239,   0, 239, white)
    tft.hline(  0,  40, 239, white)
    tft.hline(  0, 195, 239, white)  # top of battery box
    tft.hline(  0, 235, 239, white)  # bottom of battery box
    tft.fill_rect(0, 195, 239, 42, drk_grn)
    date_str = "{} {}".format(MONTHS[MONTH-1], DAY)
    tft.text(font, "DATE:",     8,   8, white, drk_grn)
    tft.text(font, date_str,   100,   8, green, drk_grn)
    tft.text(font, TARGET_SSID, 8,  58, white, drk_grn)
    tft.text(font, "BATTERY:",  8, 205, white, drk_grn)

def draw_dynamic(target_str, target_color, batt_str, batt_color):
    tft.text(font, "{:<15}".format(target_str), 8,   115, target_color, drk_grn)
    tft.fill_rect(1, 196, 237, 39, drk_grn)
    tft.hline(  0, 195, 239, white)  # roof
    tft.vline(  0, 195,  42, white)  # left border
    tft.text(font, "BATTERY:",       8,   205, white,      drk_grn)
    tft.text(font, batt_str.strip(), 144, 205, batt_color, drk_grn)
    tft.hline(  0, 235, 239, white)  # bottom
    
draw_static()

tick         = 0
scan_every   = 1
target_str   = "No scan yet"
target_color = red
batt_str     = "..."
batt_color   = white

while True:
    try:
        if btn.value() == 0:
            tft.fill(drk_grn)
            tft.text(font, "Stopped.", 8, 100, white, drk_grn)
            break

        if tick % scan_every == 0:
            tft.text(font, "scanning...    ", 8, 115, yellow, drk_grn)

            # WiFi scan
            try:
                nets        = wlan.scan()
                target_rssi = None
                for net in nets:
                    if net[0].decode('utf-8') == TARGET_SSID:
                        target_rssi = net[3]
                        break
                target_str   = "{} dBm".format(target_rssi) if target_rssi is not None else "Not found"
                target_color = rssi_color(target_rssi)
            except Exception:
                target_str   = "scan err"
                target_color = red

            # Battery
            try:
                volts = display.axp.getBattVoltage() / 1000.0
                pct   = int((volts - 3.5) / (4.2 - 3.5) * 100)
                pct   = max(0, min(100, pct))
                batt_str   = "{}%".format(pct)
                batt_color = battery_color(pct)
            except Exception:
                batt_str   = "N/A"
                batt_color = red

            draw_dynamic(target_str, target_color, batt_str, batt_color)

        tick += 1

    except KeyboardInterrupt:
        tft.fill(drk_grn)
        tft.text(font, "Stopped.", 8, 100, white, drk_grn)
        break

    except Exception as e:
        tft.text(font, str(e)[:14], 8, 36, red, drk_grn)
        time.sleep(2)
        draw_static()

    time.sleep(15)
