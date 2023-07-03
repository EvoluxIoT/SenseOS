# SenseOS Display Screen
#
# This module contains the display screen implementation for SenseOS
# Allows SenseOS to draw elements to the screen and output information to the user
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# Platform-specific Libraries (circuitpython)

DISPLAYIO_AVAILABLE = False
"""Indicates if the displayio module is available, used for display management on circuitpython"""

try:
    import displayio
except ImportError:
    pass
else:
    DISPLAYIO_AVAILABLE = True


# ---------------------------------------------------------------------
#                          Display Screen
# ---------------------------------------------------------------------

class SenseDisplayScreen:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __initialized: bool = False
    """Internal field that indicates if the screen has been initialized"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def initialized(self) -> bool:
        """
        Indicates if the screen has been initialized
        :return: True if the screen has been initialized, False otherwise
        """
        return self.__initialized

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def initialize(self):
        """
        Initializes the current display screen, preparing the layout and the elements to be drawn
        """

    def tick(self, *args, **kwargs):
        """
        Performs a tick on the screen, updating the state of the screen
        """


# ---------------------------------------------------------------------
#                     Display Screen for DisplayIO
# ---------------------------------------------------------------------

class SenseDisplayioScreen(SenseDisplayScreen, displayio.Group):

    # ---------------------------------------------------------------
    #                         Constructor
    # ---------------------------------------------------------------

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize()

