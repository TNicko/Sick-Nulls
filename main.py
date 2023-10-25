import threading
from time import sleep
from mqtt_client import MQTTSubscriber
from decouple import config


def test():
    count = 0
    while True:
        print(count)
        count += 1
        sleep(1)


def main():
    subscriber = MQTTSubscriber(
        config("MQTT_BROKER"),
        username=config("MQTT_USER"),
        password=config("MQTT_PASSWORD"),
    )
    subscriber.connect_and_subscribe_to_topic(config("MQTT_TOPIC"))

    thread_1 = threading.Thread(
        target=subscriber.client.loop_forever, args=(1,)
    )
    thread_2 = threading.Thread(target=test)
    try:
        thread_1.start()
        thread_2.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print("Fatal error {e}")


if __name__ == "__main__":
    main()
