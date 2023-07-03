# SenseOS Screen - Main Screen
#
# This module contains the main screen implementation for SenseOS
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>
import time

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.display.screen import SenseDisplayioScreen
from senseos.display.font import SenseFont
from senseos.display.elements import SenseGuiElementLabel, SenseGuiElementRect, SenseGuiElementHorizontalProgressBar, \
    SenseGuiElementHorizontalFillDirection, SenseGuiElementCircle
from senseos.synapselink import SenseSynapseLinkSubsystem
from time import monotonic
import wifi

# Platform-specific Libraries (circuitpython)

DISPLAYIO_AVAILABLE = False
"""Indicates if the displayio module is available, used for display management on circuitpython"""

try:
    import displayio
except ImportError:
    pass
else:
    DISPLAYIO_AVAILABLE = True


GREEN = 0x06EA743
RED = 0xE11A00
YELLOW = 0xFFD300

# ---------------------------------------------------------------------
#                           Boot Screen
# ---------------------------------------------------------------------

class SenseMainScreen(SenseDisplayioScreen):
    # ---------------------------------------------------------------
    #                        Elements
    # ---------------------------------------------------------------

    network_state: SenseGuiElementCircle = None
    border: SenseGuiElementRect = None
    branding: SenseGuiElementLabel = None
    progress: SenseGuiElementHorizontalProgressBar = None

    perform_reconnect = True

    @property
    def synapselink(self) -> SenseSynapseLinkSubsystem:
        return self.senseos.synapselink

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
            SenseFont, text="EvoluxIoT: Ready", scale=2, color=0x0000FF, anchor_point=(0.5, 0.5),
            anchored_position=(160, 40)
        )

        # Circle shape
        self.network_state = SenseGuiElementCircle(50, 95, 5, fill=RED, outline=RED, stroke=1)

        self.mqtt_state = SenseGuiElementCircle(50, 125, 5, fill=RED, outline=RED, stroke=1)



        #self.hostname = SenseGuiElementLabel(
        #    SenseFont, text=f"Hostname: PWRSynapse", scale=1, color=0xFFFFFF, x=30, y=75
        #)

        self.ip = SenseGuiElementLabel(
            SenseFont, text=f"WIFI Network", scale=1, color=0xFFFFFF, x=70, y=95
        )

        self.mqtt_ip = SenseGuiElementLabel(
            SenseFont, text=f"EvoluxIoT MQTT", scale=1, color=0xFFFFFF, x=70, y=125
        )

        self.uptime = SenseGuiElementLabel(
            SenseFont, text=f"Uptime: 0 seconds", scale=1, color=0xFFFFFF, anchor_point=(0.5, 0.5),
            anchored_position=(160, 155)
        )

        self.remote_text = SenseGuiElementLabel(
            SenseFont, text=f"", scale=1, color=0xFFFFFF, anchor_point=(0.5, 0.5),
            anchored_position=(160, 185)
        )

        # Add elements to the display
        self.append(self.branding)
        self.append(self.border)
        self.append(self.network_state)
        self.append(self.mqtt_state)
        self.append(self.ip)
        self.append(self.mqtt_ip)
        self.append(self.uptime)
        self.append(self.remote_text)

    def display(self, value):
        self.remote_text.text = f"{value}"
    def tick(self, *args, **kwargs):
        """
        Performs a tick on the screen, updating the state of the screen
        """
        self.network_state.fill = RED if not wifi.radio.connected else GREEN
        self.network_state.outline = RED if not wifi.radio.connected else GREEN
        self.mqtt_state.fill = RED if self.perform_reconnect or not wifi.radio.connected else GREEN
        self.mqtt_state.outline = RED if self.perform_reconnect or not wifi.radio.connected else GREEN
        self.uptime.text = f"Uptime: {int(monotonic())} seconds"

        if self.perform_reconnect or not self.synapselink.connected:
            self.mqtt_state.fill = YELLOW
            self.branding.text = f"EvoluxIoT: Connecting..."
            self.synapselink.deinitialize()
            
            self.synapselink.initialize()
            if self.synapselink.connect():
                self.perform_reconnect = False
                self.branding.text = f"EvoluxIoT: Ready"
            else:
                self.branding.text = f"EvoluxIoT: Offline"
                time.sleep(2)

        elif not self.synapselink.poll():
            self.mqtt_state.fill = RED
            self.mqtt_state.outline = RED
            self.network_state.fill = RED
            self.network_state.outline = RED
            self.branding.text = f"EvoluxIoT: Offline"
            self.perform_reconnect = True





    def __del__(self):
        """
        De-initializes the screen, freeing up resources
        """

        self.remove(self.branding)
        self.remove(self.border)
        del self.branding
        del self.border
