# SenseOS Hardware Subsystem - Keypad Abstractions
#
# This module provides access to a high level abstraction
# for buttons, allowing the operating system to detect
# and read the state of various types of keypads and matrixes
# of buttons
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware import SenseDevice, SenseDeviceType

# Platform-specific Libraries (circuitpython)

DIGITALIO_AVAILABLE = False
"""Indicates if the digitalio module is available, used for keypad control"""

try:
    import digitalio
except ImportError:
    pass
else:
    DIGITALIO_AVAILABLE = True

# ---------------------------------------------------------------------
#                           Base Keypad
# ---------------------------------------------------------------------


class SenseDeviceKeypad(SenseDevice):
    """
    A generic keypad device, handles matrixes of buttons and
    provides a high level abstraction for the operating system
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __type = SenseDeviceType.KEYPAD
    """Internal field that represents the type of the device implemented"""

    __old_matrix_state: list = None
    """Internal field that stores the last state of the matrix"""

    __new_matrix_state: list = None
    """Internal field that stores the current state of the matrix"""

    __rows: int = 0
    """Internal field that represents the number of rows in the matrix"""

    __cols: int = 0
    """Internal field that represents the number of columns in the matrix"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def rows(self) -> int:
        """
        Returns the number of rows in the matrix
        :return: The number of rows in the matrix
        """
        return self.__rows

    @property
    def columns(self) -> int:
        """
        Returns the number of columns in the matrix
        :return: The number of columns in the matrix
        """
        return self.__cols

    @property
    def changed(self) -> bool:
        """
        Indicates if the state of the keys has been updated
        :return: True if the state of the keys has been updated, False otherwise
        """
        return self.__old_matrix_state != self.__new_matrix_state

    @property
    def pressed(self) -> list[tuple[int, int]]:
        """
        Returns a list of tuples containing the coordinates of the keys that are pressed
        :return: A list of tuples containing the coordinates of the keys that are pressed
        """

        k = []

        for new_key in self.__new_matrix_state:
            if new_key not in self.__old_matrix_state:
                k.append(new_key)

        return k

    @property
    def released(self) -> list[tuple[int, int]]:
        """
        Returns a list of tuples containing the coordinates of the keys that are released
        :return: A list of tuples containing the coordinates of the keys that are released
        """
        k = []

        for old_key in self.__old_matrix_state:
            if old_key not in self.__new_matrix_state:
                k.append(old_key)

        return k


    # ---------------------------------------------------------------
    #                           Methods
    # ---------------------------------------------------------------

    def read(self):
        """
        Reads the state of the keypad and updates its state
        """


    # ---------------------------------------------------------------
    #                          Constructor
    # ---------------------------------------------------------------

    def __init__(self, name, columns: int, rows: int):
        super().__init__(name, self.__type)
        self.__rows = rows
        self.__cols = columns
        self.__old_matrix_state = []
        self.__new_matrix_state = []