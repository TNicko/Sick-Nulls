import paho.mqtt.client as mqtt
from collections import deque
from decouple import config

MQTT_BROKER = config("MQTT_BROKER")
MQTT_TOPIC = config("MQTT_TOPIC")
MQTT_USER = config("MQTT_USER")
MQTT_PASS = config("MQTT_PASSWORD")


class MQTTSubscriber:
    def __init__(
        self,
        broker_address: str,
        port: int = 1883,
        username: str = None,
        password: str = None,
    ):
        # Set MQTT broker's hostname and port
        self.broker_address = broker_address
        self.port = port

        # Set username and password
        self.username = username
        self.password = password

        # Create an MQTT client
        self.client = mqtt.Client()

        # Set the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.data = deque(maxlen=10)

    # Define callback functions for MQTT events
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            # Subscribe to a topic when connected
            # self.client.subscribe(userdata)  # Replace with your desired topic
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, message):
        self.data.append(message.payload.decode())

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"Unexpected disconnection with code {rc}")

    def connect_and_subscribe_to_topic(self, topic: str):
        # Connect to the MQTT broker with username and password
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_address, self.port, 60)
        self.client.subscribe(topic)


def initialize_mqtt_subscriber() -> MQTTSubscriber:
    """
    Initialize and start the MQTT subscriber.
    """
    subscriber = MQTTSubscriber(
        MQTT_BROKER, username=MQTT_USER, password=MQTT_PASS
    )
    subscriber.connect_and_subscribe_to_topic(MQTT_TOPIC)
    print("MQTT subscriber connected.")
    return subscriber


if __name__ == "__main__":
    subscriber = initialize_mqtt_subscriber()

    try:
        subscriber.client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting due to keyboard interrupt...")
    finally:
        subscriber.client.disconnect()
