import base64

import requests
from decouple import config


url = "http://172.16.0.242:32500/api/localization/matchingRate"

headers = {
    "Authorization": config("AGV_API_AUTH"),
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)

print(response.json())
