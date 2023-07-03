# SenseOS Hardware Subsystem - 4x4 Matrix Button Module
#
# This module provides access to a high level abstraction
# for a 4x4 matrix of buttons, allowing the operating system to detect
# and read the state and perform actions based on it in common
# 4x4 matrix of buttons
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>
import microcontroller

# ---------------------------------------------------------------------
#                     Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.hardware.keypad import SenseDeviceKeypad

# Platform-specific Libraries (circuitpython)

DIGITALIO_AVAILABLE = False
"""Indicates if the digitalio module is available, used for keypad control"""

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
#                           4x4 Matrix Button
# ---------------------------------------------------------------------

class Sense4x4MatrixButtonKeypad(SenseDeviceKeypad):
    """
    Represents a 4x4 matrix of buttons, which can be pressed and released.
    Allows the user and the operating system to perform actions based on its state
    """

    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __row_pins: list[microcontroller.Pin] = []
    """Internal field that represents the pins used to read the button state"""

    __col_pins: list[microcontroller.Pin] = []
    """Internal field that represents the pins used to read the button state"""

    __io_rows: list[digitalio.DigitalInOut] = []
    """Internal field that represents the pins used to read the button state"""

    __io_cols: list[digitalio.DigitalInOut] = []
    """Internal field that represents the pins used to read the button state"""

    __old_matrix_state = []
    """Internal field that represents the previous state of the matrix"""

    __new_matrix_state = []
    """Internal field that represents the current state of the matrix"""

    # ---------------------------------------------------------------
    #                       Methods
    # ---------------------------------------------------------------

    def read(self):
        """
        Reads the state of the matrix and updates the internal state
        """
        self.__old_matrix_state = self.__new_matrix_state.copy()

        self.__new_matrix_state = []

        for col in range(self.columns):

            self.__io_cols[col].value = False

            for row in range(self.rows):

                if not self.__io_rows[row].value:
                    self.__new_matrix_state.append((row,col))

            self.__io_cols[col].value = True


    @property
    def pressed_key_1(self) -> bool:
        """
        Indicates if the key 1 is pressed
        :return: True if the key 1 is pressed, False otherwise
        """
        return (3, 3) in self.pressed

    @property
    def pressed_key_2(self) -> bool:
        """
        Indicates if the key 2 is pressed
        :return: True if the key 2 is pressed, False otherwise
        """
        return (2, 3) in self.pressed

    @property
    def pressed_key_3(self) -> bool:
        """
        Indicates if the key 3 is pressed
        :return: True if the key 3 is pressed, False otherwise
        """
        return (1, 3) in self.pressed

    @property
    def pressed_key_4(self) -> bool:
        """
        Indicates if the key 4 is pressed
        :return: True if the key 4 is pressed, False otherwise
        """
        return (0, 3) in self.pressed

    @property
    def pressed_key_5(self) -> bool:
        """
        Indicates if the key 5 is pressed
        :return: True if the key 5 is pressed, False otherwise
        """
        return (3, 2) in self.pressed

    @property
    def pressed_key_6(self) -> bool:
        """
        Indicates if the key 6 is pressed
        :return: True if the key 6 is pressed, False otherwise
        """
        return (2, 2) in self.pressed

    @property
    def pressed_key_7(self) -> bool:
        """
        Indicates if the key 7 is pressed
        :return: True if the key 7 is pressed, False otherwise
        """
        return (1, 2) in self.pressed

    @property
    def pressed_key_8(self) -> bool:
        """
        Indicates if the key 8 is pressed
        :return: True if the key 8 is pressed, False otherwise
        """
        return (0, 2) in self.pressed

    @property
    def pressed_key_9(self) -> bool:
        """
        Indicates if the key 9 is pressed
        :return: True if the key 9 is pressed, False otherwise
        """
        return (3, 1) in self.pressed

    @property
    def pressed_key_10(self) -> bool:
        """
        Indicates if the key 10 is pressed
        :return: True if the key 10 is pressed, False otherwise
        """
        return (2, 1) in self.pressed

    @property
    def pressed_key_11(self) -> bool:
        """
        Indicates if the key 11 is pressed
        :return: True if the key 11 is pressed, False otherwise
        """
        return (1, 1) in self.pressed

    @property
    def pressed_key_12(self) -> bool:
        """
        Indicates if the key 12 is pressed
        :return: True if the key 12 is pressed, False otherwise
        """
        return (0, 1) in self.pressed

    @property
    def pressed_key_13(self) -> bool:
        """
        Indicates if the key 13 is pressed
        :return: True if the key 13 is pressed, False otherwise
        """
        return (3, 0) in self.pressed

    @property
    def pressed_key_14(self) -> bool:
        """
        Indicates if the key 14 is pressed
        :return: True if the key 14 is pressed, False otherwise
        """
        return (2, 0) in self.pressed

    @property
    def pressed_key_15(self) -> bool:
        """
        Indicates if the key 15 is pressed
        :return: True if the key 15 is pressed, False otherwise
        """
        return (1, 0) in self.pressed

    @property
    def pressed_key_16(self) -> bool:
        """
        Indicates if the key 16 is pressed
        :return: True if the key 16 is pressed, False otherwise
        """
        return (0, 0) in self.pressed

    @property
    def released_key_1(self) -> bool:
        """
        Indicates if the key 1 is released
        :return: True if the key 1 is released, False otherwise
        """
        return (3, 3) in self.released

    @property
    def released_key_2(self) -> bool:
        """
        Indicates if the key 2 is released
        :return: True if the key 2 is released, False otherwise
        """
        return (2, 3) in self.released

    @property
    def released_key_3(self) -> bool:
        """
        Indicates if the key 3 is released
        :return: True if the key 3 is released, False otherwise
        """
        return (1, 3) in self.released

    @property
    def released_key_4(self) -> bool:
        """
        Indicates if the key 4 is released
        :return: True if the key 4 is released, False otherwise
        """
        return (0, 3) in self.released

    @property
    def released_key_5(self) -> bool:
        """
        Indicates if the key 5 is released
        :return: True if the key 5 is released, False otherwise
        """
        return (3, 2) in self.released

    @property
    def released_key_6(self) -> bool:
        """
        Indicates if the key 6 is released
        :return: True if the key 6 is released, False otherwise
        """
        return (2, 2) in self.released

    @property
    def released_key_7(self) -> bool:
        """
        Indicates if the key 7 is released
        :return: True if the key 7 is released, False otherwise
        """
        return (1, 2) in self.released

    @property
    def released_key_8(self) -> bool:
        """
        Indicates if the key 8 is released
        :return: True if the key 8 is released, False otherwise
        """
        return (0, 2) in self.released

    @property
    def released_key_9(self) -> bool:
        """
        Indicates if the key 9 is released
        :return: True if the key 9 is released, False otherwise
        """
        return (3, 1) in self.released

    @property
    def released_key_10(self) -> bool:
        """
        Indicates if the key 10 is released
        :return: True if the key 10 is released, False otherwise
        """
        return (2, 1) in self.released

    @property
    def released_key_11(self) -> bool:
        """
        Indicates if the key 11 is released
        :return: True if the key 11 is released, False otherwise
        """
        return (1, 1) in self.released

    @property
    def released_key_12(self) -> bool:
        """
        Indicates if the key 12 is released
        :return: True if the key 12 is released, False otherwise
        """
        return (0, 1) in self.released

    @property
    def released_key_13(self) -> bool:
        """
        Indicates if the key 13 is released
        :return: True if the key 13 is released, False otherwise
        """
        return (3, 0) in self.released

    @property
    def released_key_14(self) -> bool:
        """
        Indicates if the key 14 is released
        :return: True if the key 14 is released, False otherwise
        """
        return (2, 0) in self.released

    @property
    def released_key_15(self) -> bool:
        """
        Indicates if the key 15 is released
        :return: True if the key 15 is released, False otherwise
        """
        return (1, 0) in self.released

    @property
    def released_key_16(self) -> bool:
        """
        Indicates if the key 16 is released
        :return: True if the key 16 is released, False otherwise
        """
        return (0, 0) in self.released


    def __init__(self, name: str, rows: list[microcontroller.Pin], cols: list[microcontroller.Pin]):
        """
        Creates a new instance of the 4x4 Matrix Button Keypad
        :param name: The name of the device
        :param rows: The pins used to read the button state
        :param cols: The pins used to read the button state
        """
        super().__init__(name, len(cols), len(rows))

        # Set up column pins as outputs and initialize to high
        self.__io_cols = [digitalio.DigitalInOut(pin) for pin in cols]
        for col_pin in self.__io_cols:
            col_pin.direction = digitalio.Direction.OUTPUT
            col_pin.value = True

        # Set up row pins as inputs with pull-up resistors enabled
        self.__io_rows = [digitalio.DigitalInOut(pin) for pin in rows]
        for row_pin in self.__io_rows:
            row_pin.direction = digitalio.Direction.INPUT
            row_pin.pull = digitalio.Pull.UP



