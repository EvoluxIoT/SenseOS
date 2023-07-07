# SenseOS Screen - Main Screen
#
# This module contains the main screen implementation for SenseOS
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com>

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries
from senseos.display.screen import SenseDisplayioScreen
from senseos.display.font import SenseFont
from senseos.display.elements import SenseGuiElementLabel, SenseGuiElementRect, SenseGuiElementHorizontalProgressBar, \
    SenseGuiElementHorizontalFillDirection, SenseGuiElementListSelect
from senseos.hardware.keypad.matrix_button_4x4 import Sense4x4MatrixButtonKeypad
import wifi
from time import sleep

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

class SenseWifiSetupScreen(SenseDisplayioScreen):
    # ---------------------------------------------------------------
    #                        Elements
    # ---------------------------------------------------------------

    border: SenseGuiElementRect = None
    branding: SenseGuiElementLabel = None
    progress: SenseGuiElementHorizontalProgressBar = None
    wifi_selector: SenseGuiElementListSelect = None

    __networks: dict[str, wifi.Network] = {}
    """All the networks found by the wifi module"""

    __scanning = False
    """Indicates if the wifi module is scanning for networks"""

    __connecting = False
    """Indicates if the wifi module is connecting to a network"""

    __s = False

    @property
    def selected_network(self) -> wifi.Network:
        return self.__networks[self.wifi_selector.selected_item]

    @property
    def connected(self):
        return wifi.radio.connected

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def scan_networks(self, save_in_selector= True):
        self.__scanning = True
        self.branding.text = "Scanning Networks..."
        for network in self.__networks.values():
            del network
        self.__networks.clear()
        for network in wifi.radio.start_scanning_networks():
            self.__networks[network.ssid] = network
        wifi.radio.stop_scanning_networks()
        if save_in_selector:
            self.wifi_selector.items = list(self.__networks.keys())
            self.wifi_selector.selected_index = 0

        self.branding.text = "Choose network:"
        self.__scanning = False



    def try_connect(self):
        self.__connecting = True
        self.branding.text = "Enabling Wifi radio..."
        wifi.radio.enabled = True

        if wifi.radio.connected:
            self.branding.text = "Connected"
            self.__connecting = False

        self.branding.text = "Checking network security..."
        authentication_required = wifi.AuthMode.OPEN not in self.selected_network.authmode
        
        if authentication_required:
            password = "evoluxiot"
        else:
            password = ""

        

        try:
            self.branding.text = "Connecting to {}...".format(self.selected_network.ssid)
            wifi.radio.connect(self.selected_network.ssid, password, bssid=self.selected_network.bssid)
        except Exception as e:
            self.branding.text = "Connection Failed"
        for retry in range(5):
            self.branding.text = f"Retrying {retry+1}/5..."
            if wifi.radio.connected:
                self.branding.text = "Connected"
                self.__connecting = False
                return True
            sleep(0.2)

        if wifi.radio.connected:
            self.branding.text = "Connected"
            self.__connecting = False
            return True
        else:
            self.branding.text = "Connection Failed"
            self.__connecting = False
            return False




    def initialize(self):
        """
        Initializes the current display screen, preparing the layout and the elements to be drawn
        """

        # Border of the screen
        self.border = SenseGuiElementRect(0, 0, 320, 240, outline=0x0000FF, stroke=1)

        # Branding of SenseOS
        self.branding = SenseGuiElementLabel(
            SenseFont, text="Select Network:", scale=2, color=0x0000FF, anchor_point=(0.5, 0.5),
            anchored_position=(160, 20)
        )

        if self.connected:
            self.branding.text = "Connected"



        self.scan_networks(False)

        self.wifi_selector = SenseGuiElementListSelect(
            scale=1,
            items=list(self.__networks.keys()),
        )

        self.wifi_selector.anchor_point = (0.5, 0.5)
        self.wifi_selector.anchored_position = (320 // 2, 240 // 2)

        # Add elements to the display
        self.append(self.branding)
        self.append(self.border)
        self.append(self.wifi_selector)

    def tick(self, *args, **kwargs):
        if self.connected or self.__scanning or self.__connecting:
            return

        keypad: Sense4x4MatrixButtonKeypad = args[0]
        keypad.read()

        if keypad.pressed_key_2:
            if self.wifi_selector.selected_index == 0:
                self.wifi_selector.selected_index = len(self.wifi_selector.items) - 1
            else:
                self.wifi_selector.selected_index -= 1

        elif keypad.pressed_key_5:
            self.scan_networks(True)

        elif keypad.pressed_key_6:
            if self.try_connect():
                return
            else:
                self.scan_networks()

        elif keypad.pressed_key_10:
            if self.wifi_selector.selected_index == len(self.wifi_selector.items) - 1:
                self.wifi_selector.selected_index = 0
            else:
                self.wifi_selector.selected_index += 1





    def __del__(self):
        """
        De-initializes the screen, freeing up resources
        """

        self.remove(self.branding)
        self.remove(self.border)
        del self.branding
        del self.border
