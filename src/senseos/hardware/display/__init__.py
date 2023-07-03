# SenseOS Hardware Subsystem - Display Abstractions
#
# This module provides access to a high level abstraction
# for various models of displays, allowing the operating
# system to show information to the user through it
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware import SenseDevice, SenseDeviceType
from senseos.display.screen import SenseDisplayioScreen

# Platform-specific Libraries (circuitpython)

GARBAGE_COLLECTOR_AVAILABLE = False
"""Indicates if the gc module is available, used for garbage collection"""

try:
    import gc
except ImportError:
    pass
else:
    GARBAGE_COLLECTOR_AVAILABLE = True

DISPLAYIO_AVAILABLE = False
"""Indicates if the displayio module is available, used for display control"""

try:
    import displayio
except ImportError:
    pass
else:
    DISPLAYIO_AVAILABLE = True


# ---------------------------------------------------------------------
#                           Base Display
# ---------------------------------------------------------------------

class SenseDeviceDisplay(SenseDevice):
    """
    Represents a generic display device, used for by the operating system
    to display information to the user
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __type = SenseDeviceType.DISPLAY
    """Internal field that represents the type of the device implemented"""

    __width: int = None
    """Internal field that represents the width of the display in pixels"""

    __height: int = None
    """Internal field that represents the height of the display in pixels"""

    __brightness_level: float = None
    """Internal field that represents current brightness level of the display"""

    # ---------------------------------------------------------------
    #                           Properties
    # ---------------------------------------------------------------

    @property
    def width(self) -> int:
        """Width of the display in pixels"""
        return self.__width

    @property
    def height(self) -> int:
        """Height of the display in pixels"""
        return self.__height

    @property
    def brightness_level(self) -> float:
        """Current brightness level of the display"""
        return self.__brightness_level

    @brightness_level.setter
    def brightness_level(self, value):
        """Sets the brightness level of the display"""
        self.set_brightness(value)

    @property
    def screen(self):
        """Current screen being displayed"""
        return None

    @screen.setter
    def screen(self, value):
        """Sets the screen to be displayed"""
        self.set_screen(value)

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def set_brightness(self, value: float = 1.0):
        """
        Set the brightness level of the display
        :param value: Value between 0 and 1
        """
        pass

    def clear(self, refresh: bool = True):
        """Clears the display"""
        pass

    def set_screen(self, screen, refresh: bool = True):
        """
        Sets the screen to be displayed

        :param refresh: Should the display be refreshed after setting the screen
        :param screen: Screen to be displayed
        """
        pass

    def refresh(self) -> bool:
        """Refreshes the display"""
        pass

    # ---------------------------------------------------------------------
    #                           Constructor
    # ---------------------------------------------------------------------

    def __init__(self, name: str, width: int, height: int):
        super().__init__(name, SenseDeviceType.DISPLAY)
        self.__width = width
        self.__height = height


# -------------------------------------------------------------------------
#                   Display Implementation for DisplayIO
# -------------------------------------------------------------------------
class SenseDisplayioDisplay(SenseDeviceDisplay):
    """
    Used when a device implementing displayio is available
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __display: displayio.Display = None
    """Internal field that represents the displayio display"""

    __screen: SenseDisplayioScreen = None
    """Internal field that represents the current screen"""

    # ---------------------------------------------------------------
    #                           Properties
    # ---------------------------------------------------------------

    @property
    def screen(self) -> SenseDisplayioScreen:
        """Displayio display"""
        return self.__screen

    @screen.setter
    def screen(self, value: SenseDisplayioScreen):
        """Sets the screen to be displayed"""
        self.set_screen(value)

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def set_screen(self, screen: SenseDisplayioScreen, refresh: bool = True):
        """
        Sets the screen to be displayed

        :param refresh: Should the display be refreshed after setting the screen
        :param screen: Screen to be displayed
        """
        if DISPLAYIO_AVAILABLE:
            if self.__display.root_group is not None:
                self.clear(False)

        self.__screen = screen
        self.__display.root_group = self.__screen

        if refresh:
            self.refresh()

    def clear(self, refresh: bool = True):
        """
        Clears the display
        """
        self.__display.root_group = None
        self.__screen = None
        if GARBAGE_COLLECTOR_AVAILABLE:
            gc.collect()

        if refresh:
            self.refresh()

    def refresh(self) -> bool:
        """
        Refreshes the display
        """
        return self.__display.refresh()


# -------------------------------------------------------------------------
#                   Unavailable Display Implementation
# -------------------------------------------------------------------------
class SenseDummyDisplay(SenseDeviceDisplay):
    """
    Used when no display is available, provides a dummy implementation
    that does nothing allowing the operating system to run without a display
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __brightness_level = 0.0
    """Internal field that represents current brightness level of the display"""

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def set_brightness(self, value: float = 1.0):
        """
        Set the brightness level of the display
        :param value: Value between 0 and 1
        """
        pass

    def clear(self, refresh: bool = True):
        """Clears the display"""
        pass

    def set_screen(self, screen, refresh: bool = True):
        """
        Sets the screen to be displayed

        :param refresh: Should the display be refreshed after setting the screen
        :param screen: Screen to be displayed
        """
        pass

    def refresh(self) -> bool:
        """Refreshes the display"""
        pass

    # ---------------------------------------------------------------------
    #                           Constructor
    # ---------------------------------------------------------------------

    def __init__(self):
        super().__init__("internal-dummy", 0, 0)
