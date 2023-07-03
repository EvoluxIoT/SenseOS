# SenseOS
#
# The universally connected and independent IoT operating system for embedded devices
# This is the main SenseOS package, containing the core of the operating system
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.acpi import SenseACPISubsystem
from senseos.display import SenseDisplaySubsystem
from senseos.hardware import SenseHardwareSubsystem
from senseos.memory import SenseMemorySubsystem
from senseos.synapselink import SenseSynapseLinkSubsystem

# ---------------------------------------------------------------------
#                           SenseOS
# ---------------------------------------------------------------------

__name__ = "SenseOS"
__version__ = "0.0.1"
__channel__ = "alpha"


class SenseOS:
    """
    The universally connected and independent IoT operating system for embedded devices
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __acpi: SenseACPISubsystem = None
    """Internal field that represents the ACPI subsystem of the operating system"""

    __hardware: SenseHardwareSubsystem = None
    """Internal field that represents the hardware subsystem of the operating system"""

    __memory: SenseMemorySubsystem = None
    """Internal field that represents the memory subsystem of the operating system"""

    __display: SenseDisplaySubsystem = None
    """Internal field that represents the display subsystem of the operating system"""

    __synapselink: SenseSynapseLinkSubsystem = None
    """Internal field that represents the SynapseLink subsystem of the operating system"""

    # ---------------------------------------------------------------
    #                           Properties
    # ---------------------------------------------------------------

    @property
    def acpi(self):
        """ACPI subsystem of the operating system"""
        return self.__acpi

    @property
    def hardware(self):
        """Hardware subsystem of the operating system"""
        return self.__hardware

    @property
    def memory(self):
        """Memory subsystem of the operating system"""
        return self.__memory

    @property
    def display(self):
        """Display subsystem of the operating system"""
        return self.__display

    @property
    def synapselink(self):
        """SynapseLink subsystem of the operating system"""
        return self.__synapselink

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def initialize(self):
        """
        Initializes the SenseOS operating system
        """
        self.__acpi.initialize()
        self.__memory.initialize()
        self.__hardware.initialize()
        self.__display.initialize()
        self.__synapselink.initialize()

    def deinitialize(self):
        """
        Deinitializes the SenseOS operating system
        """
        self.__synapselink.deinitialize()
        self.__display.deinitialize()
        self.__hardware.deinitialize()
        self.__memory.deinitialize()
        self.__acpi.deinitialize()

    def __del__(self):
        del self.__synapselink
        del self.__display
        del self.__hardware
        del self.__memory
        del self.__acpi

    # ---------------------------------------------------------------
    #                           Constructor
    # ---------------------------------------------------------------

    def __init__(self):
        self.__acpi = SenseACPISubsystem()
        self.__memory = SenseMemorySubsystem()
        self.__hardware = SenseHardwareSubsystem(self)
        self.__display = SenseDisplaySubsystem(self)
        self.__synapselink = SenseSynapseLinkSubsystem(self)
