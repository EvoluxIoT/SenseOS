# SenseOS Hardware Subsystem - Push Button
#
# This module provides access to a high level abstraction
# for a push button, allowing the operating system to detect
# and read the state and perform actions based on it in common
# push buttons
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware.button import SenseDeviceButton

# Platform-specific Libraries (circuitpython)

DIGITALIO_AVAILABLE = False
"""Indicates if the digitalio module is available, used for button control"""

try:
    import digitalio
except ImportError:
    pass
else:
    DIGITALIO_AVAILABLE = True

MICROCONTROLLER_AVAILABLE = False
"""Indicates if the microcontroller module is available, used for pin identification control"""
try:
    from microcontroller import Pin
except ImportError:
    pass
else:
    MICROCONTROLLER_AVAILABLE = True


# ---------------------------------------------------------------------
#                           Push Button
# ---------------------------------------------------------------------

class SensePushButton(SenseDeviceButton):
    """
    Represents a push button, which can be pressed and released.
    Allows the user and the operating system to perform actions
    based on it's state
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __io: digitalio.DigitalInOut = None
    """Internal field that represents the pin used to read the button state"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def pressed(self) -> bool:
        """
        Is this button pressed
        :return: True if the button is pressed, False otherwise
        """
        r = not self.__io.value

        if self.__sw_available:
            r = self.__sw_pressed

        return r

    def __init__(self, name: str, pin: Pin):
        super().__init__(name)
        self.__pin = pin
        self.__io = digitalio.DigitalInOut(self.__pin)
        self.__io.switch_to_input(digitalio.Pull.UP)

# ------------------------------------------------------------------

