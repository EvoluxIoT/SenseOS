# SenseOS SynapseLink Connector
#
# SynapseLink is a custom protocol that allows remote management and access to
# your synapse device, allowing you to program it remotely and manage it
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# Network Libraries
import adafruit_minimqtt.adafruit_minimqtt
import wifi
import socketpool

# I/O Libraries
import board
import digitalio
import analogio
import pwmio
import gc

# ---------------------------------------------------------------------
#                           Global Variables
# ---------------------------------------------------------------------

pins = [
    digitalio.DigitalInOut(board.GP16),
    digitalio.DigitalInOut(board.GP17),
    digitalio.DigitalInOut(board.GP18),
    digitalio.DigitalInOut(board.GP19),
    digitalio.DigitalInOut(board.GP0),
    digitalio.DigitalInOut(board.GP1),
    digitalio.DigitalInOut(board.GP20),
    digitalio.DigitalInOut(board.GP21),
    analogio.AnalogIn(board.A0),
    analogio.AnalogIn(board.A1),
]

COMMAND_HELLO = 0x00
"""Hello command sent by the Synapse Device to present itself as online to the other node"""
COMMAND_GOODBYE = 0x01
"""Goodbye command sent by the Synapse Device to present itself as offline to the other node"""
COMMAND_MAXVERSION = 0x02
"""Announces the maximum version of the protocol supported by the device"""
COMMAND_HEARTBEAT = 0x03
"""Checks if the device is still online and responding"""
COMMAND_ACKNOWLEDGE = 0x04
"""Synapse Device acknowledges the receipt of a command"""
COMMAND_REBOOT = 0x05
"""Reboots the Synapse Device"""
COMMAND_DIGITALREAD = 0x06
"""Reads the value of a digital pin"""
COMMAND_DIGITALWRITE = 0x07
"""Writes a value to a digital pin"""
COMMAND_ANALOGREAD = 0x08
"""Reads the value of an analog pin"""
COMMAND_DISPLAYREAD = 0x0A
"""Writes a message to the display"""
COMMAND_DISPLAYWRITE = 0x0B
"""Writes a message to the display"""

# ---------------------------------------------------------------------
#                          SynapseLink Connector
# ---------------------------------------------------------------------

class SynapseLink:
    __mqtt: adafruit_minimqtt.adafruit_minimqtt.MQTT = None
    """The MQTT Client"""

    __pool: socketpool.SocketPool = None
    """The Socket Pool"""

    __counter: int = 0
    """Used for event id counting"""

    __device_id: str = "synapsepod-crystal"
    """The device id"""

    __max_version: int = 1
    """The maximum version of the protocol supported by this client"""

    __connected: bool = False
    """The connection status"""

    __senseos = None
    """SenseOS"""

    input_subscription = []

    def __init__(self, senseos):
        self.__senseos = senseos
        self.initialize()

    @property
    def mqtt(self) -> adafruit_minimqtt.adafruit_minimqtt.MQTT:
        """
        Returns the MQTT client
        :return: The MQTT client
        """
        return self.__mqtt
    
    @property
    def topic(self) -> str:
        """
        Returns the MQTT topic
        :return: The MQTT topic
        """
        return self.__device_id
    
    
    @property
    def network_connected(self)->bool:
        """
        Returns the network connection status
        :return: True if connected, False otherwise
        """
        return wifi.radio.connected

    @property
    def connected(self) -> bool:
        return self.network_connected and self.__connected and self.mqtt_connected
    
    @property
    def mqtt_connected(self) -> bool:
        if self.__mqtt is None:
            return False
        return self.__mqtt.is_connected()
    
    def poll(self):

        if self.connected:
            try:
                self.__mqtt.loop(timeout=1)
            except adafruit_minimqtt.adafruit_minimqtt.MMQTTException as e:
                return False
            except OSError:
                self.initialize(force=True)
            except KeyboardInterrupt:
                self.__senseos.acpi.reboot()
                return False
            else:
                return True
        return False
    
    def __on_mqtt_connect(self, client: adafruit_minimqtt.adafruit_minimqtt.MQTT, userdata, flags, rc):
        """
        Executes when the MQTT client connects
        :param client: The MQTT client
        :param userdata: The user data
        :param flags: The flags
        :param rc: The return code
        """
        self.__connected = True
        client.subscribe(topic=self.__device_id)
        self.__mqtt.publish(self.__device_id,self.__build_command(COMMAND_HELLO))
        self.__counter += 1

    def __on_mqtt_message(self, client: adafruit_minimqtt.adafruit_minimqtt.MQTT, topic: str, message: str):
        """
        Executes when the MQTT client receives a message
        :param client: The MQTT client
        :param topic: The topic of the message
        :param message: The message
        """
        if message.startswith("!"):
            return
        else:
            c = self.__parse_command(message)
            self.__handle_commands(c[0], c[1], c[2])
    
    def __on_mqtt_disconnect(self, client: adafruit_minimqtt.adafruit_minimqtt.MQTT, userdata, rc):
        """
        Executes when the MQTT client disconnects
        :param client: The MQTT client
        :param userdata: The user data
        :param rc: The return code
        """
        self.__connected = False
    
    def initialize(self, force: bool = False):
        if (self.__mqtt != None or self.__pool) and not force:
            return
        
        self.__connected = False
        
        gc.collect()
        
        self.__pool = socketpool.SocketPool(wifi.radio)
        self.__mqtt = adafruit_minimqtt.adafruit_minimqtt.MQTT(
            socket_pool=self.__pool,
            broker="mqtt.evoluxiot.pt",
            username="evoluxiot",
            password="evoluxiot",
            client_id=self.__device_id,
            is_ssl=False,
            keep_alive=15,
        )

        self.__mqtt.on_connect = self.__on_mqtt_connect
        self.__mqtt.on_message = self.__on_mqtt_message
        self.__mqtt.on_disconnect = self.__on_mqtt_disconnect

        # Goodbye message
        self.__mqtt.will_set(self.__build_command(COMMAND_GOODBYE, event_id=-2))
    
    def connect(self, force: bool = False):
        self.initialize(force)
        if self.connected:
            return True
        
        if not self.network_connected:
            return False
        
        try:
            self.__mqtt.connect()
        except adafruit_minimqtt.adafruit_minimqtt.MMQTTException:
            return False
        else:
            self.__connected = True
            return True

    
    def disconnect(self):
        if not self.connected:
            return
        
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_GOODBYE))
        
        self.__mqtt.disconnect()


    
    def __del__(self):
        try:
            self.__mqtt.disconnect()
        except:
            pass

        del self.__mqtt
        del self.__pool


    # -----------------------------------------------------------------
    #                          Commands
    # -----------------------------------------------------------------

    def __parse_command(self, message: str) -> tuple[int, list[str], int]:

        # Don't parse sent messages
        if message[0] == "!":
            return (-1, [],-1)

        # Split message into command parts
        data = message.split(":,:")

        # Command must have at least 3 parts (command and event_id)
        if len(data) < 2:
            return (-1, [],-1)
        # Parameterless command
        elif len(data) == 2:
            return (int(data[0]), [], int(data[1]))
        # Command with parameters
        else:
            return (int(data[0]), data[1:-1], int(data[-1]))
    
    def __before_command(self, command: int, parameters: list = [], event_id = None):
        self.__counter += 2
        self.acknowledge(command, parameters, event_id)

    def __after_command(self, command: int, parameters: list = [], event_id = None):
        pass
        
    def __handle_commands(self, command: int, parameters: list = [], event_id = None):
        self.__before_command(command, parameters, event_id)
        
        if command == COMMAND_MAXVERSION:
            self.__counter += 1
            self.maxversion(event_id)
        elif command == COMMAND_HEARTBEAT:
            self.__counter += 1
            self.heartbeat(event_id)
        elif command == COMMAND_ACKNOWLEDGE:
            pass
        elif command == COMMAND_REBOOT:
            self.__counter += 1
            self.reboot(event_id)
        elif command == COMMAND_DIGITALREAD:
            self.__counter += 1
            self.digitalread(int(parameters[0]), event_id)
        elif command == COMMAND_DIGITALWRITE:
            self.__counter += 1
            self.digitalwrite(int(parameters[0]), int(parameters[1]), event_id)
        elif command == COMMAND_ANALOGREAD:
            self.__counter += 1
            self.analogread(int(parameters[0]), event_id)
        elif command == COMMAND_DISPLAYREAD:
            self.__counter += 1
            self.displayread(event_id)
        elif command == COMMAND_DISPLAYWRITE:
            self.__counter += 1
            self.displaywrite(parameters[0], event_id)


        self.__after_command(command, parameters, event_id)

    def __build_command(self, command: int, *args, event_id: int = None) -> str:
        if event_id is None:
            event_id = self.__counter

        result = "!{}".format(command)

        for arg in args:
            result += ":,:{}".format(arg)

        result += ":,:{}".format(self.__counter)

        self.__counter += 1

        return "{}".format(result)
    
    def maxversion(self, event_id: int = None):
        """
        Maximum version of the protocol supported by this client
        """
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_MAXVERSION, self.__max_version))

    def heartbeat(self, event_id: int = None):
        """
        Heartbeat command
        """
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_HEARTBEAT))

    def acknowledge(self, command: str, params: list[str], event_id: int = None):
        """
        Acknowledge command
        """
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_ACKNOWLEDGE,command,*params))
    
    def reboot(self, event_id: int = None):
        """
        Reboot command
        """
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_REBOOT))
        self.__senseos.acpi.reboot()
    
    def digitalread(self, pin: int, event_id: int = None):
        """
        Digital Read command
        """
        pins[pin].switch_to_input(pull=digitalio.Pull.UP)
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_DIGITALREAD, pin, int(pins[pin].value)))

    def digitalwrite(self, pin: int, value: int, event_id: int = None):
        """
        Digital Write command
        """
        pins[pin].switch_to_output()
        pins[pin].value = value
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_DIGITALWRITE, pin, int(value)))
    
    def analogread(self, pin: int, event_id: int = None):
        """
        Analog Read command
        """
        if (pin in [8, 9]):
            self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_ANALOGREAD, pin, pins[pin].value))
    
    def displayread(self, text: str, event_id: int = None):
        """
        Display Write command
        """
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_DISPLAYREAD, self.__senseos.display.primary_display.screen.remote_text.text ))
    
    def displaywrite(self, text: str, event_id: int = None):
        """
        Display Write command
        """
        self.__senseos.display.primary_display.screen.remote_text.text = text
        self.__mqtt.publish(self.__device_id, self.__build_command(COMMAND_DISPLAYWRITE, text))

class SenseSynapseLinkSubsystem:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __initialised = False
    """Internal field that indicates if the memory subsystem has been initialised"""

    __synapselink: SynapseLink = None
    """Internal field that contains the SynapseLink client"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------


    @property
    def initialized(self) -> bool:
        """
        Indicates if the memory subsystem is initialized
        :return: Boolean indicating if the memory subsystem is initialized
        """
        return self.__initialised

    @property
    def mqtt_connected(self) -> bool:
        """
        Indicates if the SynapseLink client is connected to MQTT broker
        :return: True if connected, False otherwise
        """
        return self.__synapselink.mqtt_connected

    @property
    def network_connected(self) -> bool:
        """
        Indicates if the SynapseLink client is connected to network
        :return: True if connected, False otherwise
        """
        return self.__synapselink.network_connected

    @property
    def connected(self) -> bool:
        """
        Indicates if the SynapseLink client is connected to network and mqtt broker
        :return: True if connected, False otherwise
        """
        return self.__synapselink.connected

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def connect(self):
        if wifi.radio.connected and not self.__synapselink.connected:
            return self.__synapselink.connect()

        return self.__synapselink.connected

    def disconnect(self):
        if self.__synapselink.connected:
            self.__synapselink.disconnect()

        return not self.__synapselink.mqtt_connected 

    def poll(self):
        return self.__synapselink.poll()

    def initialize(self):

        self.__synapselink = SynapseLink(self.__senseos)
        self.__initialised = True

    def deinitialize(self):
        
        self.disconnect()

        del self.__synapselink
        self.__initialised = False

    def __init__(self, senseos):
        self.__senseos = senseos


