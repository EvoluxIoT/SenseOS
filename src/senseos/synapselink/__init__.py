# SenseOS SynapseLink Connector
#
# SynapseLink is a custom protocol that allows remote management and access to
# your synapse device, allowing you to program it remotely and manage it
#
# Miguel Lopes <miguellopes2004.ml@hotmail.com

# ---------------------------------------------------------------------
#                      Libraries and References
# ---------------------------------------------------------------------

# SenseOS Libraries

# Network Libraries
from adafruit_minimqtt.adafruit_minimqtt import MQTT
from ssl import create_default_context
from socketpool import SocketPool
from wifi import radio

import gc

# Board Libraries
import microcontroller

# ---------------------------------------------------------------------
#                           Constants
# ---------------------------------------------------------------------

COMMAND_MAXVERSION = 0x00
COMMAND_HEARTBEAT = 0x01
COMMAND_ACKNOWLEDGE = 0x02
COMMAND_REBOOT = 0x03
COMMAND_DIGITALREAD = 0x04
COMMAND_DIGITALWRITE = 0x05
COMMAND_ANALOGREAD = 0x06
COMMAND_ANALOGWRITE = 0x07
COMMAND_PWMREAD = 0x08
COMMAND_PWMWRITE = 0x09
COMMAND_DISPLAYWRITE = 0x0A


# ---------------------------------------------------------------------
#                           SynapseLink
# ---------------------------------------------------------------------

class SynapseLink:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __max_version: int = 1
    """Internal field that contains the maximum version of the protocol supported by this client"""

    # ---------------------------------------------------------------
    #                         Properties
    # ---------------------------------------------------------------

    @property
    def mqtt_connected(self) -> bool:
        """
        Returns if the client is connected to the broker
        :return: True if the client is connected to the broker, False otherwise
        """
        return False

    @property
    def network_connected(self) -> bool:
        """
        Returns if the client is connected to the network
        :return: True if the client is connected to the network, False otherwise
        """
        return radio.connected

    @property
    def connected(self):
        return self.mqtt_connected and self.network_connected

    @property
    def max_version(self) -> int:
        """
        Returns the maximum version of the protocol supported by this client
        :return: The maximum version of the protocol supported by this client
        """
        return self.__max_version

    # ---------------------------------------------------------------
    #                         Methods
    # ---------------------------------------------------------------

    def __before_evoke(self, name: str, parameters: list, event: int):
        """
        Executes before the event is evoked
        :param name: The name of the event to evoke
        :param parameters: The parameters of the event
        :param event: The event to evoke
        """


    def __after_evoke(self, name: str, parameters: list, event: int):
        """
        Executes after the event is evoked
        :param name: The name of the event to evoke
        :param parameters: The parameters of the event
        :param event: The event to evoke
        """

    def __evoke(self, name: str, parameters: list, event: int):
        """
        Evoke an event on the SenseOS operating system
        :param name: The name of the event to evoke
        :param parameters: The parameters of the event
        :param event: The event to evoke
        """
        self.__before_evoke(name, parameters, event)

        if name == "maxversion":
            self.maxversion(event)

        if name == "heartbeat":
            self.heartbeat(event)
        if name == "reboot":
            self.reboot(event)
        if name == "digitalread":
            self.digitalread(parameters[0], event)
        if name == "digitalwrite":
            self.digitalwrite(parameters[0], parameters[1], event)
        if name == "displaywrite":
            self.displaywrite(parameters[0], event)




        self.__after_evoke(name, parameters, event)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def maxversion(self, event: int):
        """
        Maximum version of the protocol supported by this client
        """

    def heartbeat(self, event: int):
        """
        Sends a heartbeat to the server
        """

    def reboot(self, event: int):
        """
        Reboots the device
        """
        self.__senseos.acpi.reboot()

    def digitalread(self, pin: int, event: int):
        """
        Reads a digital pin
        """

    def digitalwrite(self, pin: int, state: bool, event: int):
        """
        Writes a digital pin
        """

    def analogread(self, pin: int, event: int):
        """
        Reads an analog pin
        """

    def analogwrite(self, pin: int, state: int, event: int):
        """
        Writes an analog pin
        """

    def pwmread(self, pin: int, event: int):
        """
        Reads a PWM pin
        """

    def pwmwrite(self, pin: int, state: int, event: int):
        """
        Writes a PWM pin
        """

    def displaywrite(self, text: str, event: int):
        """
        Writes a message to the display
        """


    def __init__(self, senseos):
        self.__senseos = senseos

# ---------------------------------------------------------------------
#                           SynapseLink
# ---------------------------------------------------------------------

class MQTTSynapseLink(SynapseLink):

    __mqtt: MQTT = None
    """Internal field that contains the MQTT client"""

    __pool: SocketPool = None
    """Internal field that contains the socket pool"""

    __mqtt_initialized: bool = False
    
    __counter = 0

    topic: str = f"synapsepod-crystal"

    @property
    def mqtt(self) -> MQTT:
        """
        Returns the MQTT client
        :return: The MQTT client
        """
        return self.__mqtt

    @property
    def mqtt_connected(self) -> bool:
        """
        Returns if the client is connected to the broker
        :return: True if the client is connected to the broker, False otherwise
        """
        return self.__mqtt is not None and self.__mqtt.is_connected()

    def __on_mqtt_connect(self, client: MQTT, userdata, flags, rc):
        """
        Executes when the MQTT client connects
        :param client: The MQTT client
        :param userdata: The user data
        :param flags: The flags
        :param rc: The return code
        """
        print("Connected to MQTT Broker! as {}".format(client.client_id))
        client.subscribe(topic=self.topic)

    def __on_mqtt_disconnect(self, client: MQTT, userdata, rc):
        """
        Executes when the MQTT client disconnects
        :param client: The MQTT client
        :param userdata: The user data
        :param rc: The return code
        """
        print("Disconnected from MQTT Broker!")

    def __on_mqtt_message(self, client: MQTT, topic: str, message: str):
        """
        Executes when the MQTT client receives a message
        :param client: The MQTT client
        :param topic: The topic of the message
        :param message: The message
        """
        if message.startswith("!"):
            return
        else:
            message = message.split(":,:")
            self.__evoke(message[0], message[1:], 0)
    def connect(self, force: bool = False):
        if not self.__mqtt_initialized or force:
            del self.__mqtt
            self.__mqtt_init()
        try:
            self.__mqtt.connect()
        except Exception as e:
            return False
        return True

    def disconnect(self):
        if self.mqtt_connected:
            self.__mqtt.disconnect()

    def __mqtt_init(self, broker: str = "evoluxiot.pt", port: int = 1883, username: str = "evoluxiot", password: str = "evoluxiot"):
        self.__pool = SocketPool(radio)

        gc.collect()
        self.__mqtt = MQTT(
            socket_pool=self.__pool,
            broker=broker,
            port=port,
            username=username,
            password=password,
            ssl_context=create_default_context(),
            client_id=f"synapsepod-crystal",
            is_ssl=False,
            keep_alive=15,
        )

        self.__mqtt.on_connect = self.__on_mqtt_connect
        self.__mqtt.on_disconnect = self.__on_mqtt_disconnect
        self.__mqtt.on_message = self.__on_mqtt_message

        self.__mqtt_initialized = True

    def __del__(self):
        self.__mqtt.disconnect()

        del self.__mqtt
        del self.__pool
        del self.__mqtt_init



    def __init__(self, senseos):
        super().__init__(senseos)
        self.__mqtt_init()

    # ---------------------------------------------------------------
    #                         Commands
    # ---------------------------------------------------------------

    def __before_evoke(self, name: str, parameters: list, event: int):
        self.__counter += 1
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_ACKNOWLEDGE}:,:{name}:,:{parameters}:,:{self.__counter}")

    def __after_evoke(self, name: str, parameters: list, event: int):
        pass

    def maxversion(self, event: int):
        """
        Maximum version of the protocol supported by this client
        """
        
        self.__counter += 1
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_MAXVERSION}:,:{self.max_version}:,:{self.__counter}")

    def heartbeat(self, event: int):
        """
        Sends a heartbeat to the server
        """
        self.__counter += 1
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_HEARTBEAT}:,:{self.__counter}")

    def reboot(self, event: int):
        """
        Reboots the device
        """
        self.__counter += 1
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_REBOOT}:,:{self.__counter}")
        self.__senseos.acpi.reboot()

    def digitalread(self, pin: int, event: int):
        """
        Reads a digital pin
        """
        self.__counter += 1
        state = False
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_DIGITALREAD}:,:{pin}:,:{int(state)}:,:{self.__counter}")

    def digitalwrite(self, pin: int, state: bool, event: int):
        """
        Writes a digital pin
        """
        self.__counter += 1
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_DIGITALWRITE}:,:{pin}:,:{state}:,:{self.__counter}")

    def displaywrite(self, text: str, event: int):
        """
        Writes a digital pin
        """

        self.__counter += 1
        self.__senseos.display.primary_display.screen.display(text)
        self.__mqtt.publish(topic=self.topic, msg=f"!{COMMAND_DISPLAYWRITE}:,:{text}:,:{self.__counter}")

class SenseSynapseLinkSubsystem:
    # ---------------------------------------------------------------
    #                         Internal Fields
    # ---------------------------------------------------------------

    __senseos = None
    """Internal field that contains access to the SenseOS operating system"""

    __initialised = False
    """Internal field that indicates if the memory subsystem has been initialised"""

    __synapselink: MQTTSynapseLink = None
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
        if not self.__synapselink.mqtt_connected and self.__synapselink.network_connected:
            return self.__synapselink.connect()

        return self.__synapselink.connected

    def disconnect(self):
        if self.__synapselink.connected:
            self.__synapselink.disconnect()

        return not self.__synapselink.mqtt_connected

    def poll(self):
        if self.__synapselink.connected:
            try:
                self.__synapselink.mqtt.loop(timeout=1)
            except:
                return False
            else:
                return True
        return False

    def initialize(self):

        self.__synapselink = MQTTSynapseLink(self.__senseos)
        self.__initialised = True

    def deinitialize(self):
        try:
            self.__synapselink.disconnect()
        except:
            pass

        del self.__synapselink
        self.__initialised = False

    def __init__(self, senseos):
        self.__senseos = senseos