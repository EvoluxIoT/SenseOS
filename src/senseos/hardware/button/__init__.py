# SenseOS Hardware Subsystem - Button Abstractions
#
# This module provides access to a high level abstraction
# for buttons, allowing the operating system to detect
# and read the state of various types of buttons
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware import SenseDevice, SenseDeviceType

# Platform-specific Libraries (circuitpython)

DIGITALIO_AVAILABLE = False
"""Indicates if the digitalio module is available, used for button control"""

try:
    import digitalio
except ImportError:
    pass
else:
    DIGITALIO_AVAILABLE = True


# ---------------------------------------------------------------------
#                           Base Button
# ---------------------------------------------------------------------

class SenseDeviceButton(SenseDevice):
    """
    Represents a generic button device, used for by the operating system
    to detect and read the state and perform actions based on it
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __type = SenseDeviceType.BUTTON
    """Internal field that represents the type of the device implemented"""

    __sw_pressed: bool = False
    """Internal field for emulating a keypress through systemcalls"""

    __sw_available: bool = False
    """Internal field specifying if the next keypress is handled by software or hardware"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def pressed(self) -> bool:
        """
        Is this button pressed
        :return: True if the button is pressed, False otherwise
        """
        r = None

        if self.__sw_available:
            r = self.__sw_pressed

        return r

    @property
    def released(self) -> bool:
        """
        Is this button released?
        :return: True if the button is released, False otherwise
        """
        f = self.pressed
        if f is None:
            return f
        return not self.pressed

    @property
    def is_software(self):
        """
        Is the next read handled by software?
        :return: True if handled by software, else False
        """
        return self.__sw_available

    @property
    def is_hardware(self):
        return not self.__sw_available

    # ---------------------------------------------------------------
    #                         Public Methods
    # ---------------------------------------------------------------

    def press(self):
        """
        Presses the button through software
        """

        self.__sw_available = True
        self.__sw_pressed = True

    def release(self):
        """
        Releases the button through software
        """

        self.__sw_available = True
        self.__sw_pressed = False

    def __init__(self, name: str):
        super().__init__(name, self.__type)
