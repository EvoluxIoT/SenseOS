# SenseOS Memory Subsystem - Memory Management
#
# This module contains the memory management implementation for SenseOS
# This allows the implementation of memory management features
# regardless of the device hosting the operating system
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# Platform-specific Libraries (circuitpython)

GARBAGE_COLLECTOR_AVAILABLE = False
"""Indicates if the gc module is available, used for memory management on circuitpython"""

try:
    import gc
except ImportError:
    pass
else:
    GARBAGE_COLLECTOR_AVAILABLE = True
    gc.enable()


# ---------------------------------------------------------------------
#                          Memory Management
# ---------------------------------------------------------------------

class SenseMemorySubsystem:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __initialised = False
    """Internal field that indicates if the memory subsystem has been initialised"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def free(self) -> int:
        """
        Returns the amount of free memory in bytes
        :return: The amount of free memory in bytes, or -1 if the current platform does not support this feature
        """
        if GARBAGE_COLLECTOR_AVAILABLE:
            return gc.mem_free()
        else:
            return -1

    @property
    def used(self) -> int:
        """
        Returns the amount of used memory in bytes
        :return: The amount of used memory in bytes, or -1 if the current platform does not support this feature
        """
        if GARBAGE_COLLECTOR_AVAILABLE:
            return gc.mem_alloc()
        else:
            return -1

    @property
    def total(self) -> int:
        """
        Returns the total amount of memory in bytes
        :return: The total amount of memory in bytes, or -1 if the current platform does not support this feature
        """
        if GARBAGE_COLLECTOR_AVAILABLE:
            return self.free + self.used
        else:
            return -1

    @property
    def auto_reclaim(self) -> bool:
        """
        Indicates if the memory subsystem has enabled a feature which automatically reclaims memory at runtime when
        needed
        :return: Boolean indicating if the feature is enabled, else False
        """

        if GARBAGE_COLLECTOR_AVAILABLE:
            return gc.isenabled()
        else:
            return False

    @auto_reclaim.setter
    def auto_reclaim(self, value: bool):
        """
        Enables or disables the automatic memory reclamation feature
        :param value: Boolean indicating if the feature should be enabled or disabled
        """
        if GARBAGE_COLLECTOR_AVAILABLE:
            if value:
                gc.enable()
            else:
                gc.disable()

    @property
    def initialized(self) -> bool:
        """
        Indicates if the memory subsystem is initialized
        :return: Boolean indicating if the memory subsystem is initialized
        """
        return self.__initialised

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def initialize(self):
        """
        Initializes the memory subsystem
        """
        self.auto_reclaim = True
        self.__initialised = True

    def deinitialize(self):
        """
        Deinitializes the memory subsystem
        """
        self.auto_reclaim = False
        self.__initialised = False

    def reclaim(self) -> bool:
        """
        Tries to reclaim memory by deleting unused objects
        :return: True if reclaimed memory, False otherwise
        """
        if GARBAGE_COLLECTOR_AVAILABLE:
            return gc.collect() > 0
        else:
            return False
