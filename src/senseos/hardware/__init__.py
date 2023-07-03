# SenseOS Hardware Subsystem - Hardware Manager
#
# This module is for managing the hardware of the system, providing
# a simple and powerful way to interface with the hardware
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                           Device Types
# ---------------------------------------------------------------------

class SenseDeviceType:
    """
    Enumerates the different types of devices that can be connected to
    the SenseOS system
    """

    GENERIC = "Generic"
    """Unknown/generic device type"""

    BUTTON = "Button"
    """Button or any other digital input device type"""

    KEYPAD = "Keypad"
    """Keypad, matrix of button or any other digital input device type"""

    DISPLAY = "Display"
    """Monitor, LCD, TFT, ePaper or any other display device type"""

    PIN = "Pin"
    """Pin, GPIO, PWM or any other digital output device type"""


# -------------------------------------------------------------------
#                          Base Device
# -------------------------------------------------------------------

class SenseDevice:
    """
    Represents a SenseOS device, which abstracts the communication
    with the hardware

    Contains the base methods and properties that all devices should
    implement in order to be compatible with the operating system
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __type: SenseDeviceType = SenseDeviceType.GENERIC
    """Internal field that represents the type of the device implemented"""

    name: str = None
    """Unique name representing this device"""

    # ---------------------------------------------------------------
    #                           Properties
    # ---------------------------------------------------------------

    @property
    def type(self):
        """Type of the device implemented"""
        return self.__type

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type

    def __str__(self):
        return f"SenseOS {self.__type} Device ({self.name})"

    def __repr__(self):
        return str(self)

    # ---------------------------------------------------------------
    #                           Constructor
    # ---------------------------------------------------------------

    def __init__(self, name: str, device_type: SenseDeviceType = SenseDeviceType.GENERIC):
        self.name = name
        self.__type = device_type


# -------------------------------------------------------------------
#                         Hardware Manager
# -------------------------------------------------------------------

from senseos.hardware.display import SenseDummyDisplay


class SenseHardwareSubsystem:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __devices: dict[str, SenseDevice] = {}
    """Internal field that contains all the devices connected to the system"""

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __initialized: bool = False
    """Internal field that indicates if the hardware subsystem has been initialized"""

    # ---------------------------------------------------------------
    #                           Properties
    # ---------------------------------------------------------------

    @property
    def initialized(self) -> bool:
        """
        Returns whether the hardware subsystem has been initialized
        :return: Boolean indicating if the hardware subsystem is initialized
        """
        return self.__initialized

    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def initialize(self):
        """
        Initializes the hardware subsystem
        """

        # Init Dummy Display
        self.connect("internal-dummy-display", SenseDummyDisplay())

        self.__initialized = True

    def deinitialize(self):
        for device in self.__devices:
            self.disconnect(device)

        self.__senseos.memory.reclaim()

        self.__initialized = False

    def connect(self, name: str, device: SenseDevice) -> bool:
        """
        Connects the specified device to SenseOS operating system
        :param name: The unique name chosen to identify this device
        :param device: Instance of the device to be connected
        :return: Boolean indicating if the device was successfully connected
        """
        if self.exists(name):
            return False

        self.__devices[name] = device
        return True

    def disconnect(self, name: str, try_reclaim_memory: bool = False) -> bool:
        """
        Disconnects the specified device from SenseOS operating system
        :param name: The unique name chosen to identify this device
        :param try_reclaim_memory: Boolean indicating if the memory should be reclaimed after disconnecting
        :return: Boolean indicating if the device was successfully disconnected
        """
        if not self.exists(name):
            return False

        del self.__devices[name]

        if try_reclaim_memory:
            self.__senseos.memory.reclaim()

        return True

    def find(self, name: str) -> SenseDevice:
        """
        Gets the device with the specified name
        :param name: The unique name chosen to identify this device
        :return: The device with the specified name
        """
        return self.__devices[name]

    def find_type(self, device_type: SenseDeviceType) -> list[SenseDevice]:
        """
        Gets all the devices of the specified type
        :param device_type: The type of the devices to be returned
        :return: A list containing all the devices of the specified type
        """
        return [device for device in self.__devices.values() if device.type == device_type]

    def exists(self, name: str) -> bool:
        """
        Checks if a device with the specified name exists
        :param name: The unique name chosen to identify this device
        :return: Boolean indicating if a device with the specified name exists
        """
        return name in self.__devices

    def __len__(self):
        return len(self.__devices)

    def __str__(self):
        return f"SenseOS Hardware Manager ({len(self)} devices attached)"

    def __repr__(self):
        return str(self)

    # ---------------------------------------------------------------
    #                           Constructor
    # ---------------------------------------------------------------

    def __init__(self, senseos):
        self.__senseos = senseos
