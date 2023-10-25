import threading
from time import sleep
from mqtt_client import MQTTSubscriber
import json
import math


def test():
    count = 0
    while True:
        print(count)
        count += 1
        sleep(1)
        

def main():
    subscriber = MQTTSubscriber("128.140.111.159", username="rabbitmq", password="rabbitmq")
    subscriber.connect_and_subscribe_to_topic("uagv/2/safelog/AGVS303:S/state")

    thread_1 = threading.Thread(target=subscriber.client.loop_forever, args=(1,))

    try:
        thread_1.start()
        # thread_2.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Fatal error {e}")

    while True:
        if len(subscriber.data) > 0:
            string_data = subscriber.data.popleft()
            json_data = json.loads(string_data)
            agv_position = json_data["agvPosition"]
            x = agv_position["x"]
            y = agv_position["y"]
            theta = agv_position["theta"]
            print(f"x: {x}      y: {y}     theta: {math.degrees(theta)}")
        sleep(1)

if __name__ == "__main__":
    main()

    