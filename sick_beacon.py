import requests
from decouple import config
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

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

print(response.json()["positions"][0]["position"])
