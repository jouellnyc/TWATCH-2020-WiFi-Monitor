"""watch_display.py - standalone TWATCH-2020 display init"""
from machine import Pin, SPI
import axp202c
import st7789
from st7789 import color565

dc        = 27
cs        = 5
sck       = 18
mosi      = 19
backlight = 15
rotation  = 90

class WatchDisplay:

    def __init__(self):
        self.axp = axp202c.PMU()
        self.axp.enablePower(axp202c.AXP202_LDO2)
        self.tft = st7789.ST7789(
            SPI(1, baudrate=32000000, sck=Pin(sck, Pin.OUT), mosi=Pin(mosi, Pin.OUT)),
            240, 240,
            cs=Pin(cs, Pin.OUT),
            dc=Pin(dc, Pin.OUT),
            backlight=Pin(backlight, Pin.OUT),
            rotation=rotation
        )
        self.tft.init()

    def battery_percent(self):
        try:
            volts = self.axp.getBattVoltage() / 1000.0
            pct   = int((volts - 3.5) / (4.2 - 3.5) * 100)
            return max(0, min(100, pct))
        except:
            return None

display = WatchDisplay()