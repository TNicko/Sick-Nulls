import requests
import json
from decouple import config
import time

password = config("ERIKSON_PASSWORD")
username = config("ERIKSON_USER")


def get_data(ip):
    # Get cookie and token
    cookies = {
        "CGISID": "NULL",
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101"
            " Firefox/110.0"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "http://" + ip + "/login.html",
        "Content-Type": "json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://" + ip,
        "Connection": "keep-alive",
    }

    params = {
        "_": "set_web_user_login_0.010597065160396713",
    }

    data = (
        '{"action":"set_web_user_login","args":{"user":"'
        + username
        + '","password":"'
        + password
        + '"}}'
    )

    response = requests.post(
        "http://" + ip + "/cgi-bin/login.cgi",
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )

    aaa = response.headers["Set-Cookie"]

    cookies = {"CGISID": aaa.split(";")[0].split("=")[1]}

    # Get data
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101"
            " Firefox/110.0"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "http://" + ip + "/index.html",
        "Content-Type": "json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://" + ip,
        "Connection": "keep-alive",
    }

    params = {
        "_": "get_wwan_radio_info3_0.8110112846379409",
    }

    data = (
        '{"action":"get_wwan_radio_info3","token":"'
        + response.json()["set_web_user_login"]["cgitoken"]
        + '"}'
    )

    while True:
        response = requests.post(
            "http://" + ip + "/cgi-bin/gui.cgi",
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        )

        resp = response.json()["get_wwan_radio_info3"]
        rsrp = (
            resp["nr_srv_cell_rsrp_0"],
            resp["nr_srv_cell_rsrp_1"],
            resp["nr_srv_cell_rsrp_2"],
            resp["nr_srv_cell_rsrp_3"],
        )
        rsrq = resp["nr_srv_cell_rsrq"]
        snr = resp["nr_snr"]
        yield rsrp, rsrq, snr


for rsrp, rsrq, snr in get_data("192.168.1.1"):
    print(f"RSRP: {rsrp}, RSRQ: {rsrq}, SNR: {snr}")
