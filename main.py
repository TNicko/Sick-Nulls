import threading
from time import sleep
from mqtt_client import MQTTSubscriber
from decouple import config
import json
import math
import requests
from data_collector import initialize_coordinates_file
from typing import Tuple
from urllib3.exceptions import InsecureRequestWarning


def sick_beacon_coordinates() -> Tuple[float, float]:
    headers = {
        "accept": "application/json",
        "Authorization": config("ASSET_MANAGER_AUTH"),
    }

    params = {
        "assetIds": "3a86f33b-964e-49fd-a3c1-bac393cc062a",
        "include": "positions",
    }

    response = requests.get(
        "https://172.16.0.20/asset-manager/api/v2/assets/data",
        params=params,
        headers=headers,
        verify=False,
    )
    coordinates = response.json()["positions"][0]["position"]
    return (coordinates["x"], coordinates["y"])


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

    try:
        thread_1.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Fatal error {e}")

    append_coordinates = initialize_coordinates_file()
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    while True:
        if len(subscriber.data) > 0:
            string_data = subscriber.data.popleft()
            json_data = json.loads(string_data)
            agv_position = json_data["agvPosition"]
            x = agv_position["x"]
            y = agv_position["y"]
            theta_rad = agv_position["theta"]
            theta_deg = math.degrees(theta_rad)
            xy1 = (x, y)
            xy2 = sick_beacon_coordinates()

            append_coordinates(*xy1, *xy2)
        sleep(1)


if __name__ == "__main__":
    main()
