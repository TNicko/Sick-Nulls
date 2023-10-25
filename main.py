import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
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
            " eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDczQjI0QUU0OUREOTUwNDJFQjg2RDZGMjdFOUYzIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2OTgyNjAyOTQsImV4cCI6MTY5ODI2MjA5NCwiaXNzIjoiaHR0cHM6Ly8xMjcuMC4wLjEvdXNlci1tYW5hZ2VyIiwiYXVkIjoiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiLCJjbGllbnRfaWQiOiJhc3NldC1hbmFseXRpY3MiLCJzdWIiOiI2NThlYmZmMi1hM2VkLTQ0Y2MtODkyYi0zYTZjZTVjY2Q1NjYiLCJhdXRoX3RpbWUiOjE2OTgyMjU3ODgsImlkcCI6ImxvY2FsIiwiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9yb2xlIjoidmlld2VyIiwianRpIjoiOTYwNDVGMUM3MzQ5N0MwQUNCRjdCNkFCNDI3NkJCNDciLCJzaWQiOiJGMzc5OUU5QzAyQzRERDI3RTkxNDBFQ0M4NEExMkVDRCIsImlhdCI6MTY5ODI2MDI5NCwic2NvcGUiOlsiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiXSwiYW1yIjpbInB3ZCJdfQ.urTSGG25IIH9jO3A-d3lFw7eO29ycEOVY_1uU450qlhG0XJXleIGoN3MzrQJ0FIlBwN1IkLTjZvxs103mQH6GYAXr9qE9Jfe9iC9meQUm2HoccK9XwulbRgyVy2_SSTZ-y2wD7mdfwAljMl6_mb03V7epXx_g0e06vhsoEG9cIo3u3YlLDP0REnM2X0-SNQV5xrvIb6_KiEC9hmvBblsWGRaCns0-Id52Vr7-bmkDJw8NBZ4NsWenpg0cuBnkOWsKJOoI3l9d_424bjCoNhj5KXobjKy6wFhVn-lymnY5nmlSmXg9395OaQCBWiK5ujQ7zmgPDqAW0f0CCZ0qyHPeQ"
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


def transform_coord(beacon_coord):
    with open("model/model.sav", "rb") as file:
        model = pickle.load(file)

    predicted_coord = model.predict(np.array(beacon_coord).reshape(1, -1))
    return predicted_coord


def get_matching_rate():
    url = "http://172.16.0.242:32500/api/localization/matchingRate"

    headers = {
        "Authorization": "Basic cmFzcGk6c2VjcmV0UGFzc3dvcmQ=",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    return response.json()


def set_position(coords, theta):
    # URL and endpoint
    url = "http://172.16.0.242:32500/api/setPosition"

    # Headers
    headers = {
        "accept": "application/json",
        "authorization": "Basic cmFzcGk6c2VjcmV0UGFzc3dvcmQ=",
    }

    # Payload
    payload = {
        "llsX": coords[0],
        "llsY": coords[1],
        "llsTheta": theta,  # radians
        "deviationRadius": 0.3,
        "map": "SickHackathon_20231023.vmap",
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))


def main():
    beacon_coords = sick_beacon_coordinates()
    print("Running transform...")
    print("Beacon coords: ", beacon_coords)
    transformed_beacon_coords = transform_coord(beacon_coords)
    print("Transform coords: ", transformed_beacon_coords)
    theta_rad = 0
    set_position(beacon_coords, theta_rad)

    subscriber = MQTTSubscriber(
        "128.140.111.159", username="rabbitmq", password="rabbitmq"
    )
    subscriber.connect_and_subscribe_to_topic("uagv/2/safelog/AGVS303:S/state")
    print("connected")
    thread_1 = threading.Thread(
        target=subscriber.client.loop_forever, args=(1,)
    )
    try:
        thread_1.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Fatal error {e}")

    print("LOOPY")

    # append_coordinates = initialize_coordinates_file()
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    # while True:
    sleep(3)
    if len(subscriber.data) > 0:
        string_data = subscriber.data.popleft()
        print(string_data)
        json_data = json.loads(string_data)
        agv_position = json_data["agvPosition"]
        x = agv_position["x"]
        y = agv_position["y"]
        theta_rad = agv_position["theta"]
        print(f"Initial theta: {theta_rad}")
        print(f"AGV coords: ", agv_position)
        theta_deg = math.degrees(theta_rad)
        agv_coords = (x, y)

        for i in range(4):
            set_position(beacon_coords, theta_rad)
            matching_rate = get_matching_rate()
            print(f"Theta: {theta_rad} Matching rate: {matching_rate}")
            if matching_rate >= 90:
                break

            theta_rad += 0.5 * math.pi
            if theta_rad > 2 * math.pi:
                theta_rad -= 2 * math.pi

            sleep(3)


if __name__ == "__main__":
    main()
