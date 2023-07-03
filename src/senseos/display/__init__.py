# SenseOS Display Subsystem - Display Management
#
# This module contains the display management implementation for SenseOS
# Allows SenseOS to manage the displays and output information to the user
# regardless of the device hosting the operating system
# This displays can be implemented using console output, a display controller, etc.
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware.display import SenseDeviceDisplay, SenseDeviceType


# ---------------------------------------------------------------------
#                        Display Management
# ---------------------------------------------------------------------

class SenseDisplaySubsystem:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __primary_display: SenseDeviceDisplay = None
    """Internal field that contains the primary display of the system"""

    __initialised = False
    """Internal field that indicates if the ACPI subsystem has been initialised"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def initialized(self) -> bool:
        """
        Returns whether the display subsystem has been initialized
        :return: Boolean indicating if the ACPI subsystem is initialized
        """
        return self.__initialised

    @property
    def primary_display(self) -> SenseDeviceDisplay:
        """
        Returns the primary display of the system
        :return: The primary display of the system
        """
        return self.__primary_display

    @primary_display.setter
    def primary_display(self, display: str):
        """
        Sets the primary display of the system
        :param value: The primary display of the system
        """
        self.__primary_display = self.__senseos.hardware.find(display)

    @property
    def displays(self) -> list[SenseDeviceDisplay]:
        """
        Returns the list of displays available on the system
        :return: The list of displays available on the system
        """
        return self.__senseos.hardware.find_type(SenseDeviceType.DISPLAY)

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def initialize(self):
        """
        Initializes the display subsystem
        """
        self.__primary_display = self.displays[(len(self.displays) - 1)]
        self.__initialised = True

    def deinitialize(self):
        """
        Deinitializes the display subsystem
        """
        self.__initialised = False

    def __init__(self, senseos):
        """
        Initializes the display subsystem
        :param senseos: The SenseOS instance that owns this subsystem
        """
        self.__senseos = senseos
