from typing import Tuple, Dict, Any
from decouple import config
import requests

# Constants for the request headers and URLs
ASSET_MANAGER_AUTH = config("ASSET_MANAGER_AUTH")
AGV_API_AUTH = config("AGV_API_AUTH")
ASSET_MANAGER_URL = "https://172.16.0.20/asset-manager/api/v2/assets/data"
MATCHING_RATE_URL = "http://172.16.0.242:32500/api/localization/matchingRate"
SET_POSITION_URL = "http://172.16.0.242:32500/api/setPosition"
ROTATE_API_URL = "http://172.16.0.242:32500/api/driveRotate"


def get_beacon_coordinates() -> Tuple[float, float]:
    headers = {
        "accept": "application/json",
        "Authorization": ASSET_MANAGER_AUTH,
    }

    params = {
        "assetIds": "3a86f33b-964e-49fd-a3c1-bac393cc062a",
        "include": "positions",
    }

    response = requests.get(
        ASSET_MANAGER_URL,
        params=params,
        headers=headers,
        verify=False,  # This should be handled appropriately in production
    )

    response.raise_for_status()  # Ensure we notify on failed requests

    coordinates = response.json()["positions"][0]["position"]
    return coordinates["x"], coordinates["y"]


def get_matching_rate() -> float:
    headers = {
        "Authorization": AGV_API_AUTH,
        "Content-Type": "application/json",
    }

    response = requests.get(MATCHING_RATE_URL, headers=headers)
    response.raise_for_status()

    matching_rate = response.json()  # Add specific key if needed
    return matching_rate  # assuming the matching rate is a float


def set_agv_position(coords: Tuple[float, float], theta: float) -> None:
    headers = {
        "accept": "application/json",
        "authorization": AGV_API_AUTH,
    }

    payload = {
        "llsX": coords[0],
        "llsY": coords[1],
        "llsTheta": theta,  # radians
        "deviationRadius": 0.7,
        "map": "Hackathon_20231025.vmap",
    }

    response = requests.post(SET_POSITION_URL, headers=headers, json=payload)
    response.raise_for_status()  # This will raise an exception for HTTP errors


def set_agv_rotation(data: Dict[str, Any]) -> None:
    headers = {
        "accept": "application/json",
        "authorization": AGV_API_AUTH,
        "Content-Type": "application/json",
    }

    response = requests.post(
        ROTATE_API_URL, headers=headers, json=data, verify=False
    )
    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
