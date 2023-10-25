import requests
import base64

url = "http://172.16.0.242:32500/api/localization/matchingRate"

headers = {
    "Authorization": "Basic cmFzcGk6c2VjcmV0UGFzc3dvcmQ=",
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)

print(response.json())
