# SenseOS Hardware Subsystem - Display ILI9341
#
# This module provides access to a high level abstraction
# for ILI9341 displays, allowing the operating system to
# render information to the user through it
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# -------------------------------------------------------------------
#                    Libraries and references
# -------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware.display import SenseDisplayioDisplay

# External Libraries
from adafruit_ili9341 import ILI9341

# Platform-specific Libraries (circuitpython)

PWNIO_AVAILABLE = False
"""Indicates if the pwmio module is available, used for backlight control"""

try:
    from pwmio import PWMOut
except ImportError:
    pass
else:
    PWNIO_AVAILABLE = True

DISPLAYIO_AVAILABLE = False
"""Indicates if the displayio module is available, used for display control"""

try:
    import displayio
except ImportError:
    pass
else:
    DISPLAYIO_AVAILABLE = True

BUSIO_AVAILABLE = False
"""Indicates if the busio module is available, used for SPI communication"""
try:
    from busio import SPI
except ImportError:
    pass
else:
    BUSIO_AVAILABLE = True

GARBAGE_COLLECTOR_AVAILABLE = False
"""Indicates if the gc module is available, used for garbage collection"""

try:
    import gc
except ImportError:
    pass
else:
    GARBAGE_COLLECTOR_AVAILABLE = True

MICROCONTROLLER_AVAILABLE = False
"""Indicates if the microcontroller module is available, used for pin identification control"""
try:
    from microcontroller import Pin
except ImportError:
    pass
else:
    MICROCONTROLLER_AVAILABLE = True


# -------------------------------------------------------------------
#                           ILI9341 Display
# -------------------------------------------------------------------

class SenseILI9341Display(SenseDisplayioDisplay):
    """
    Represents a ILI9341 display device, used for by the operating system
    to display information to the user by providing a high level abstraction
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __cs_pin: Pin = None
    """Internal field that represents the chip select pin of the display"""

    __dc_pin: Pin = None
    """Internal field that represents the data/command pin of the display"""

    __reset_pin: Pin = None
    """Internal field that represents the reset pin of the display"""

    __backlight_pin: Pin = None
    """Internal field that represents the backlight pin of the display"""

    __clock_pin: Pin = None
    """Internal field that represents the clock pin of the display"""

    __mosi_pin: Pin = None
    """Internal field that represents the MOSI pin of the display"""

    __miso_pin: Pin = None
    """Internal field that represents the MISO pin of the display"""

    __spi: SPI = None
    """Internal field that represents the SPI bus of the display"""

    __backlight: PWMOut = None
    """Internal field that represents the PWM output of the backlight pin"""

    __display_bus: displayio.FourWire = None
    """Internal field that represents the displayio driver bus"""

    __display: ILI9341 = None
    """Internal field that represents the displayio driver controller"""

    # ---------------------------------------------------------------
    #                           Constructor
    # ---------------------------------------------------------------

    def __init__(self, name: str, cs_pin: Pin, dc_pin: Pin, rst_pin: Pin, clk_pin: Pin, mosi_pin: Pin,
                 miso_pin: Pin = None, bl_pin: Pin = None, width: int = 320, height: int = 240,
                 brightness_level: float = 1):
        # Device Initialization
        super().__init__(name, width, height)

        # Pin Initialization
        self.__cs_pin = cs_pin
        self.__dc_pin = dc_pin
        self.__reset_pin = rst_pin
        if PWNIO_AVAILABLE:
            self.__backlight_pin = bl_pin
            self.__backlight = PWMOut(self.__backlight_pin)
            self.set_brightness(brightness_level)
        self.__clk_pin = clk_pin
        self.__mosi_pin = mosi_pin
        self.__miso_pin = miso_pin

        # Display Initialization
        self.__spi = SPI(clock=self.__clk_pin, MOSI=self.__mosi_pin, MISO=self.__miso_pin)
        self.__display_bus = displayio.FourWire(self.__spi, command=self.__dc_pin, chip_select=self.__cs_pin,
                                                reset=self.__reset_pin)
        self.__display = ILI9341(self.__display_bus, width=width, height=height)

    def set_brightness(self, value: float = 1.0):
        """
        Sets the brightness of the display to the specified level

        :param value: Brightness level (0-1)
        """
        if PWNIO_AVAILABLE and self.__backlight is not None:
            level = int((2 ** 16 - 1) * value)
            self.__backlight.duty_cycle = level
            self.__brightness_level = level

