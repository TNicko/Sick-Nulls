import pickle
import numpy as np
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
from sklearn.linear_model import LinearRegression


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
    print(response.status_code)
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
        "Authorization": config("AGV_API_AUTH"),
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
        "authorization": config("AGV_API_AUTH"),
    }

    # Payload
    payload = {
        "llsX": coords[0],
        "llsY": coords[1],
        "llsTheta": theta,  # radians
        "deviationRadius": 0.7,
        "map": "Hackathon_20231025.vmap",
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
        config("MQTT_BROKER"),
        username=config("MQTT_USER"),
        password=config("MQTT_PASSWORD"),
    )
    subscriber.connect_and_subscribe_to_topic(config("MQTT_TOPIC"))

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
        print(f"AGV coords: ", agv_position)
        theta_deg = math.degrees(theta_rad)
        agv_coords = (x, y)

        theta_rad = 0.0
        url = "http://172.16.0.242:32500/api/driveRotate"
        headers = {
            "accept": "application/json",
            "authorization": "Basic cmFzcGk6c2VjcmV0UGFzc3dvcmQ=",
            "Content-Type": "application/json",
        }

        angle_radians = 0.2 * math.pi
        data = {
            "rotationDirection": "clockwise",
            "angleRadians": angle_radians,
            "speedRadianPerSecond": 0.02,
        }

        theta_rad = angle_radians
        for i in range(10):
            set_position(transformed_beacon_coords[0], theta_rad)
            sleep(5)
            print(f"Beacon Coordinates: {transformed_beacon_coords}")
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                print("Request was successful!")
                # print("Response:", response.json())
            else:
                print(
                    f"Request failed with status code {response.status_code}:"
                )
                print(response.text)
            matching_rate = get_matching_rate()
            print(f"Theta: {theta_rad} Matching rate: {matching_rate}")
            if matching_rate >= 90:
                break

            theta_rad = angle_radians + 0.2 * math.pi
            print(theta_rad)
            sleep(5)

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
