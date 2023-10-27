import threading
from time import sleep
from mqtt_client import initialize_mqtt_subscriber
import json
import math
import requests
from api import (
    get_beacon_coordinates,
    set_agv_position,
    get_matching_rate,
    set_agv_rotation,
)
from transformation import load_model, predict_coordinates


def main():
    # Suppress only the single InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning
    )

    beacon_coords = get_beacon_coordinates()
    print("Beacon coords: ", beacon_coords)

    regression_model = load_model()
    transformed_beacon_coords = predict_coordinates(
        regression_model, beacon_coords
    )
    print("Transform coords: ", transformed_beacon_coords)

    theta_rad = 0
    set_agv_position(beacon_coords, theta_rad)

    subscriber = initialize_mqtt_subscriber()

    thread_1 = threading.Thread(
        target=subscriber.client.loop_forever, args=(1,)
    )
    try:
        thread_1.start()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Fatal error {e}")

    sleep(3)

    if subscriber.data:
        string_data = subscriber.data.popleft()
        print(string_data)
        json_data = json.loads(string_data)
        agv_position = json_data["agvPosition"]
        print(f"AGV coords: ", agv_position)

        theta_rad = 0.0
        angle_radians = 0.2 * math.pi
        theta_rad = 0.5 * math.pi
        rotation_data = {
            "rotationDirection": "clockwise",
            "angleRadians": angle_radians,
            "speedRadianPerSecond": 0.02,
        }

        for _ in range(10):
            set_agv_position(transformed_beacon_coords[0], theta_rad)
            sleep(5)
            print(f"Beacon Coordinates: {transformed_beacon_coords}")

            response = set_agv_rotation(rotation_data)
            if response.status_code == 200:
                print("Request was successful!")
            else:
                print(
                    f"Request failed with status code {response.status_code}:"
                )
                print(response.text)

            matching_rate = get_matching_rate()
            print(f"Theta: {theta_rad} Matching rate: {matching_rate}")
            if matching_rate >= 90:
                break
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
