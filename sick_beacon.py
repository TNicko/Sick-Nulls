import requests

from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

headers = {
    "accept": "application/json",
    "Authorization": (
        "Bearer"
        " eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDczQjI0QUU0OUREOTUwNDJFQjg2RDZGMjdFOUYzIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE2OTgyMjcxNjcsImV4cCI6MTY5ODIyODk2NywiaXNzIjoiaHR0cHM6Ly8xMjcuMC4wLjEvdXNlci1tYW5hZ2VyIiwiYXVkIjoiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiLCJjbGllbnRfaWQiOiJhc3NldC1hbmFseXRpY3MiLCJzdWIiOiI2NThlYmZmMi1hM2VkLTQ0Y2MtODkyYi0zYTZjZTVjY2Q1NjYiLCJhdXRoX3RpbWUiOjE2OTgyMjQ4NTIsImlkcCI6ImxvY2FsIiwiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9yb2xlIjoidmlld2VyIiwianRpIjoiQjlBNkRGRTg4MDU4QTlCQzI2MzkwQkQ0NEI1NDg2Q0IiLCJzaWQiOiI0QjY3MjE0NEUyRjMyQkQ2RTBCNEZCQjMwMkQxMjA4MSIsImlhdCI6MTY5ODIyNzE2Nywic2NvcGUiOlsiaHR0cDovL2Fzc2V0LWFuYWx5dGljcy5pby9hcGkiXSwiYW1yIjpbInB3ZCJdfQ.ftd50r-bh33RydXJrxP8kw5PdZyhrffFL3OO-ldwTHGQorwlRcRZeQGGWZsfX-CFlJPPialIJfvzJdlk49v8yRd0WbBBbQWSc2x5nu6-spLR0pQNn11VJ1v-wKHRudo-dmtQRbs5pIw_OxRnD6zuq_FLRLGOKKdo3dQ2mYP9KhUWNJtp3HLjSqODGCuAom0mzAbp2Uepf_ckzAbzDp_naiuRN8W5-xvvCekd3jOqKHurygDQL8zjEMzB3iQjJQKa4tm4KVo596IkpD6s5HTrftKDYFudu4VYxbhBaN2Sjk-4dAHekFkAb3V3D2WPGlGlagr9nMi807zOGT8RgU3crg"
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

print(response.json()["positions"][0]["position"])
