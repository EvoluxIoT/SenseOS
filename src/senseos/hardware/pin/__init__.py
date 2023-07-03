# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware import SenseDevice, SenseDeviceType

# Platform-specific Libraries (circuitpython)

DIGITALIO_AVAILABLE = False
"""Indicates if the digitalio module is available, for digital input/output"""

try:
    import digitalio
except ImportError:
    pass
else:
    DIGITALIO_AVAILABLE = True

MICROCONTROLLER_AVAILABLE = False
"""Indicates if the microcontroller module is available, for microcontroller-specific functions"""

try:
    import microcontroller
except ImportError:
    pass
else:
    MICROCONTROLLER_AVAILABLE = True

BOARD_AVAILABLE = False
"""Indicates if the board module is available, for board-specific functions"""

try:
    import board
except ImportError:
    pass
else:
    BOARD_AVAILABLE = True

# ---------------------------------------------------------------------
#                           Base Pin
# ---------------------------------------------------------------------

class SenseDevicePin(SenseDevice):
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __type = SenseDeviceType.PIN
    """Internal field that represents the type of the device implemented"""

    __pin: microcontroller.Pin = None
    """Internal field that represents the pin object"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def pin(self) -> microcontroller.Pin:
        """
        Returns the pin object
        :return: The pin object
        """
        return self.__pin

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------