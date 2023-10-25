import requests
import json
from decouple import config

# URL and endpoint
url = "http://172.16.0.242:32500/api/setPosition"

# Headers
headers = {
    "accept": "application/json",
    "authorization": config("AGV_API_AUTH"),
}

# Payload
payload = {
    "llsX": 15.0,
    "llsY": 5.0,
    "llsTheta": 0.0,
    "deviationRadius": 0.3,
    "map": "SickHackathon_20231023.vmap",
}

# Make the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
