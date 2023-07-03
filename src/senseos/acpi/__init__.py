# SenseOS ACPI Subsystem - Advanced Configuration and Power Interface
#
# This module contains the ACPI implementation for SenseOS
# This allows the implementation of power management features
# regardless of the device hosting the operating system
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# External Libraries
from time import monotonic, monotonic_ns

# Platform-specific Libraries (circuitpython)

MICROCONTROLLER_AVAILABLE = False
"""Indicates if the microcontroller module is available, used for power management on circuitpython"""

try:
    import microcontroller
except ImportError:
    pass
else:
    MICROCONTROLLER_AVAILABLE = True


# ---------------------------------------------------------------------
#                          ACPI Methods
# ---------------------------------------------------------------------

class SenseACPISubsystem:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __initialised = False
    """Internal field that indicates if the ACPI subsystem has been initialised"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def uptime(self) -> float:
        """
        Returns the number of seconds since the system started
        :return: Floating-point number of seconds since the system started
        """
        return monotonic()

    @property
    def uptime_ns(self) -> int:
        """
        Returns the number of nanoseconds since the system started
        :return: Integer number of nanoseconds since the system started
        """
        return monotonic_ns()

    @property
    def initialized(self) -> bool:
        """
        Returns whether the ACPI subsystem has been initialized
        :return: Boolean indicating if the ACPI subsystem is initialized
        """
        return self.__initialised

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def initialize(self):
        """
        Initializes the SenseOS Operating System
        """
        self.__initialised = True

    def deinitialize(self):
        """
        Deinitializes SenseOS Operating System
        """
        self.__initialised = False

    def reboot(self):
        """
        Resets the SenseOS operating system, performing a software based reboot of the system
        """
        self.__senseos.deinitialize()

        if MICROCONTROLLER_AVAILABLE:
            microcontroller.reset()
        else:
            pass
