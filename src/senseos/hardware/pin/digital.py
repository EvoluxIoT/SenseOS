# SenseOS Hardare Subsystem - Digital Pin
#
# This module provides access to a high level abstraction
# for digital pins, allowing the operating system to detect,
# read and write the state of various types of digital pins
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware.pin import SenseDevicePin
from senseos.hardware import SenseDeviceType

# Platform-specific Libraries (circuitpython)

DIGITALIO_AVAILABLE = False
"""Indicates if the digitalio module is available, used for digital input/output"""

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

class SenseDigitalPin(SenseDevicePin):
    # ---------------------------------------------------------------
    #                       Internal Fields
    # ---------------------------------------------------------------

    __digital: digitalio.DigitalInOut = None
    """Internal field that represents the digital pin object"""

    # ---------------------------------------------------------------
    #                        Properties
    # ---------------------------------------------------------------

    @property
    def is_input(self) -> bool:
        """
        Indicates if the pin is in input mode
        """
        return self.__digital.direction == digitalio.Direction.INPUT

    @property
    def is_output(self) -> bool:
        """
        Indicates if the pin is in output mode
        """
        return self.__digital.direction == digitalio.Direction.OUTPUT

    @property
    def value(self) -> bool:
        """
        Returns the current value of the pin
        """
        return self.__digital.value

    @value.setter
    def value(self, value: bool):
        """
        Sets the value of the pin
        """
        self.__digital.value = value

    @property
    def pull(self) -> digitalio.Pull:
        """
        Gets the current pull of the pin
        """
        return self.__digital.pull

    @pull.setter
    def pull(self, value: digitalio.Pull):
        """
        Sets the pull of the pin
        """
        self.__digital.pull = value

    @property
    def drive_mode(self) -> digitalio.DriveMode:
        """
        Gets the current drive mode of the pin
        """
        return self.__digital.drive_mode

    @drive_mode.setter
    def drive_mode(self, value: digitalio.DriveMode):
        """
        Sets the drive mode of the pin
        """
        self.__digital.drive_mode = value

    @property
    def direction(self) -> digitalio.Direction:
        """
        Gets the current direction of the pin
        """
        return self.__digital.direction

    @direction.setter
    def direction(self, value: digitalio.Direction):
        """
        Sets the direction of the pin
        """
        self.__digital.direction = value

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def set_input(self):
        """
        Sets the pin to input mode
        """
        self.__digital.direction = digitalio.Direction.INPUT

    def set_output(self):
        """
        Sets the pin to output mode
        """
        self.__digital.direction = digitalio.Direction.OUTPUT

    def toggle(self):
        """
        Toggles the value of the pin
        """
        self.__digital.value = not self.__digital.value

    def on(self):
        """
        Sets the value of the pin to True
        """
        self.__digital.value = True

    def off(self):
        """
        Sets the value of the pin to False
        """
        self.__digital.value = False


    # ---------------------------------------------------------------
    #                         Constructor
    # ---------------------------------------------------------------

    def __init__(self, pin: microcontroller.Pin, name: str = None):
        """
        Initializes a new instance of the SenseDigitalPin class
        """
        super().__init__(name, SenseDeviceType.PIN)
        self.__pin = pin
        self.__digital = digitalio.DigitalInOut(pin)