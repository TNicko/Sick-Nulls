from typing import Tuple
import requests


def get_beacon_coordinates() -> Tuple[float, float]:
    headers = {
        "accept": "application/json",
        "Authorization": (
            "Bearer"
            " eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDczQjI0QUU0OUREOTUwNDJFQjg2RDZGMjdFOUYzIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2OTgyNzM2NjgsImV4cCI6MTY5ODI3NTQ2OCwiaXNzIjoiaHR0cHM6Ly8xMjcuMC4wLjEvdXNlci1tYW5hZ2VyIiwiYXVkIjoiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiLCJjbGllbnRfaWQiOiJhc3NldC1hbmFseXRpY3MiLCJzdWIiOiI2NThlYmZmMi1hM2VkLTQ0Y2MtODkyYi0zYTZjZTVjY2Q1NjYiLCJhdXRoX3RpbWUiOjE2OTgyMjY1MTcsImlkcCI6ImxvY2FsIiwiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9yb2xlIjoidmlld2VyIiwianRpIjoiMTJEMEU0QTU2RDIzMkRGQzk3N0Q5NUNBQkQ1NzQzNTYiLCJzaWQiOiI4Rjg4Rjg5NkQwNzg2QkIyQzY3RTQyRDk3NEQwQTk5OSIsImlhdCI6MTY5ODI3MzY2OCwic2NvcGUiOlsiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiXSwiYW1yIjpbInB3ZCJdfQ.ecyeCCO1Y2SAoQeVy-V975_keJFXZPGOyLULqIITN9iaf3f9aFlwqI3iBuU7F95Bw-Sz5AAxDftshzbM-6ZEQhAsrnGyVQ3fKyejdjbLbuRYgNDJ4yQp3KFuhJ_NWgWFq79m0IRrw0PTZ_mb7Go38pMscHw6ekBod1CyAJxM9khNrFW-VX4BAhXm57nJifKweBkaZroebIxPdxsV5YQEU-IMqCCCbjn6UeZ0DmCANPRrUXx-3ZylSS3wxLk6dzKpCYnQS2o8W-WVIpHKeJkaMwEsco9kL-_5oSDyzMjXWdJsbTF-v6NzUoXLz4Q_Yzq2LZfA-gCqWUOmrLmjT9n9Ww"
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
    print(response.status_code)
    coordinates = response.json()["positions"][0]["position"]
    return (coordinates["x"], coordinates["y"])


def get_matching_rate():
    url = "http://172.16.0.242:32500/api/localization/matchingRate"

    headers = {
        "Authorization": "Basic cmFzcGk6c2VjcmV0UGFzc3dvcmQ=",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    return response.json()


def set_agv_position(coords, theta):
    url = "http://172.16.0.242:32500/api/setPosition"
    headers = {
        "accept": "application/json",
        "authorization": "Basic cmFzcGk6c2VjcmV0UGFzc3dvcmQ=",
    }
    payload = {
        "llsX": coords[0],
        "llsY": coords[1],
        "llsTheta": theta,  # radians
        "deviationRadius": 0.7,
        "map": "Hackathon_20231025.vmap",
    }
    requests.post(url, headers=headers, data=json.dumps(payload))
