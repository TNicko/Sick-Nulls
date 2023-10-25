import threading
from time import sleep
from mqtt_client import MQTTSubscriber
import json
import math
import requests
from data_collector import initialize_coordinates_file
from typing import Tuple
from urllib3.exceptions import InsecureRequestWarning

def sick_beacon_coordinates() -> Tuple[float, float]:
    headers = {
        "accept": "application/json",
        "Authorization": (
            "Bearer"
            " eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDczQjI0QUU0OUREOTUwNDJFQjg2RDZGMjdFOUYzIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2OTgyNDg3MTcsImV4cCI6MTY5ODI1MDUxNywiaXNzIjoiaHR0cHM6Ly8xMjcuMC4wLjEvdXNlci1tYW5hZ2VyIiwiYXVkIjoiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiLCJjbGllbnRfaWQiOiJhc3NldC1hbmFseXRpY3MiLCJzdWIiOiI2NThlYmZmMi1hM2VkLTQ0Y2MtODkyYi0zYTZjZTVjY2Q1NjYiLCJhdXRoX3RpbWUiOjE2OTgyMjA3ODQsImlkcCI6ImxvY2FsIiwiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9yb2xlIjoidmlld2VyIiwianRpIjoiNEVEOUMzNEY1ODU2M0ZGRjlEMEJBMDI0NDg1OEU0MTMiLCJzaWQiOiIxMURBODUyQzNENzkyNUMyNDAwQjlFMDQ2MzhERTFCOSIsImlhdCI6MTY5ODI0ODcxNywic2NvcGUiOlsiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiXSwiYW1yIjpbInB3ZCJdfQ.pwAM-JWflZLsisXf_6p-805p7OcNv5GSqyN5bWRZphzpakoeut92O62VAv-Cf808ZEDJ5fOcvZX7ZwbB2ZDcfo-UtSV0rMmXjHfNFujfrObszFurshJyCKvEHVUdyi1UasBwukzj7Gk52Znmmowfq11r3iVDO_kdKtLyS5rKJERxfFAS-2q6S73HQiGXx3BmHJSUXKiE66ovU-PP9u_RNA0uqWil6u3bmh1ohf_65jkZNL1aN2Oomt1sd9GHUdp_wp6H3TtLusWFtYjmg02Ri6gjZW2DigvlFmbqgsWuQVw0uHisqhuUrgG2ZishA9PgOStkd1N4yLKNvTVqn3Jygw"
        ),
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
    subscriber = MQTTSubscriber("128.140.111.159", username="rabbitmq", password="rabbitmq")
    subscriber.connect_and_subscribe_to_topic("uagv/2/safelog/AGVS303:S/state")

    thread_1 = threading.Thread(target=subscriber.client.loop_forever, args=(1,))

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
            xy1 = (x,y)
            xy2 = sick_beacon_coordinates()
            
            append_coordinates(*xy1, *xy2)
        sleep(1)

if __name__ == "__main__":
    main()

    