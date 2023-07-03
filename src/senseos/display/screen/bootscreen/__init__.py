# SenseOS Screen - Boot Screen
#
# This module contains the boot screen implementation for SenseOS
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.display.screen import SenseDisplayioScreen
from senseos.display.font import SenseFont
from senseos.display.elements import SenseGuiElementLabel, SenseGuiElementRect, SenseGuiElementHorizontalProgressBar, SenseGuiElementHorizontalFillDirection

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
#                           Boot Screen
# ---------------------------------------------------------------------

class SenseBootScreen(SenseDisplayioScreen):
    # ---------------------------------------------------------------
    #                        Elements
    # ---------------------------------------------------------------

    border: SenseGuiElementRect = None
    branding: SenseGuiElementLabel = None
    progress: SenseGuiElementHorizontalProgressBar = None

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------


    def initialize(self):
        """
        Initializes the current display screen, preparing the layout and the elements to be drawn
        """

        # Border of the screen
        self.border = SenseGuiElementRect(0, 0, 320, 240, outline=0x0000FF, stroke=1)

        # Branding of SenseOS
        self.branding = SenseGuiElementLabel(
            SenseFont, text="SenseOS", scale=4, color=0x0000FF, anchor_point=(0.5, 0.5),
            anchored_position=(160, 120)
        )

        # Progress bar representing the boot progress
        self.progress = SenseGuiElementHorizontalProgressBar(
            (20, 10), (280, 20), direction=SenseGuiElementHorizontalFillDirection.LEFT_TO_RIGHT,
            bar_color=0xFF3399, border_thickness=0
        )
        self.progress.y = 200

        # Add elements to the display
        self.append(self.branding)
        self.append(self.border)
        self.append(self.progress)

    def tick(self, *args, **kwargs):
        """
        Performs a tick on the screen, updating the state of the screen
        """

        status = args[0]
        self.progress.value = status

    def __del__(self):
        """
        De-initializes the screen, freeing up resources
        """

        self.remove(self.branding)
        self.remove(self.border)
        self.remove(self.progress)
        del self.branding
        del self.border
        del self.progress
