# Platform and Device Definitions - SynapsePod Crystal
#
# Defines the platform and device definitions for the SynapsePod Crystal
# This includes the attached devices and their respective pins
#
# SynapsePod Crystal is the first generation device of EvoluxIoT, ready
# for IoT remote programming and management, based on a Raspberry PI Pico W,
# paired with a ILI9341 320x240 tft display, a 4x4 button matrix keyboard
# and a cathode RGB led builtin. It allows you to connect and program more components
# according to the project ideas of the user turning it into a full fledged device
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware.display.ili9341 import SenseILI9341Display
from senseos.hardware.keypad.matrix_button_4x4 import Sense4x4MatrixButtonKeypad

# SenseOS Display Screens
from senseos.display.screen.bootscreen import SenseBootScreen
from senseos.display.screen.mainscreen import SenseMainScreen
from senseos.display.screen.wifisetupscreen import SenseWifiSetupScreen

# Platform Libraries
import board
import displayio
from wifi import radio
from time import sleep

displayio.release_displays()

# ---------------------------------------------------------------------
#                              Devices
# ---------------------------------------------------------------------

# Display
display = SenseILI9341Display(
    name="internal-builtin-display",
    cs_pin=board.GP5,
    dc_pin=board.GP4,
    rst_pin=board.GP3,
    bl_pin=board.GP2,
    clk_pin=board.GP6,
    mosi_pin=board.GP7,
    miso_pin=None,
    width=320,
    height=240,
    brightness_level=1
)

# Keypad
keypad = Sense4x4MatrixButtonKeypad(
    rows=[board.GP12, board.GP13, board.GP14, board.GP15],
    cols=[board.GP8, board.GP9, board.GP10, board.GP11],
    name="internal-builtin-keypad",
)

display.clear()

# ---------------------------------------------------------------------
#                             SenseOS
# ---------------------------------------------------------------------

# Use common firmware code to initialize operating system
from firmware import os

# Connect the display to SenseOS Operating System
os.hardware.connect(display.name, display)
os.hardware.connect(keypad.name, keypad)

os.display.primary_display = display.name

# Perform SenseOS boot
os.display.primary_display.screen = SenseBootScreen()
progress_status = 0
while progress_status <= 100:
    sleep(0.01)
    os.display.primary_display.screen.tick(progress_status)
    os.display.primary_display.refresh()

    progress_status += 1

os.display.primary_display.screen = None

while True:
    if not radio.connected:
        os.display.primary_display.screen = None
        os.display.primary_display.screen = SenseWifiSetupScreen()
        while not os.display.primary_display.screen.connected:
            os.display.primary_display.screen.tick(keypad)
            os.display.primary_display.refresh()

    os.display.primary_display.screen = None

    os.display.primary_display.screen = SenseMainScreen()
    os.display.primary_display.screen.senseos = os
    while radio.connected:
        os.display.primary_display.screen.tick(keypad)
        os.display.primary_display.refresh()

# ---------------------------------------------------------------------
#                             Exports
# ---------------------------------------------------------------------

__all__ = [
    "os"
]
