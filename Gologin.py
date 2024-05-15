import requests, time
import json

MAX_RETRIES = 3
# token = input("enetrtokemn")
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjQ0NGQ2ZWY5ZTk0NjcwNDBmYzQwNmYiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjQ0NGRhMjg2NjNjNjRlZjZmNWJiMmUifQ.2c7ZgQHgDAmzqIfg6c0WQIt_ZBbkyhsLtnqzwzY9tJM'


def CreateBrowser(retries=0):
    if retries >= MAX_RETRIES:
        raise Exception("Exceeded maximum retries")

    url = "https://api.gologin.com/browser"

    payload = json.dumps({
        "name": "string",
        "notes": "string",
        "browserType": "chrome",
        "os": "win",
        "startUrl": "string",
        "googleServicesEnabled": False,
        "lockEnabled": False,
        "debugMode": False,
        "navigator": {
            "userAgent": "string",
            "resolution": "string",
            "language": "string",
            "platform": "string",
            "doNotTrack": False,
            "hardwareConcurrency": 0,
            "deviceMemory": 1,
            "maxTouchPoints": 0
        },
        "geoProxyInfo": {},
        "storage": {
            "local": True,
            "extensions": True,
            "bookmarks": True,
            "history": True,
            "passwords": True,
            "session": True
        },
        "proxyEnabled": False,
        "proxy": {
            "mode": "none",
            "host": "",
            "port": 0,
            "username": "",
            "password": ""
        },
        "dns": "string",
        "plugins": {
            "enableVulnerable": True,
            "enableFlash": True
        },
        "timezone": {
            "enabled": True,
            "fillBasedOnIp": True,
            "timezone": "string"
        },
        "audioContext": {
            "mode": "off",
            "noise": 0
        },
        "canvas": {
            "mode": "off",
            "noise": 0
        },
        "fonts": {
            "families": [
                "string"
            ],
            "enableMasking": True,
            "enableDomRect": True
        },
        "mediaDevices": {
            "videoInputs": 0,
            "audioInputs": 0,
            "audioOutputs": 0,
            "enableMasking": False
        },
        "webRTC": {
            "mode": "alerted",
            "enabled": True,
            "customize": True,
            "localIpMasking": False,
            "fillBasedOnIp": True,
            "publicIp": "string",
            "localIps": [
                "string"
            ]
        },
        "webGL": {
            "mode": "noise",
            "getClientRectsNoise": 0,
            "noise": 0
        },
        "clientRects": {
            "mode": "noise",
            "noise": 0
        },
        "webGLMetadata": {
            "mode": "mask",
            "vendor": "string",
            "renderer": "string"
        },
        "webglParams": [],
        "profile": "string",
        "googleClientId": "string",
        "updateExtensions": True,
        "chromeExtensions": [
            "string"
        ]
    })
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        response_json = response.json()
        if response_json.get('id'):
            return response_json.get('id')
        else:
            return CreateBrowser(retries=retries + 1)

    except Exception as e:
        print(f"Error: {e}")
        return None


def start_browser(browser_id):
    retries = 0
    while retries < MAX_RETRIES:
        url = "http://localhost:36912/browser/start-profile"
        payload = json.dumps({
            "profileId": browser_id,
            "sync": True
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = response.json()

        if response_json.get('status') == 'success':
            return response_json.get('wsUrl')
        else:
            retries += 1
            time.sleep(1)

    return None


def stop_browser(browser_id):
    retries = 0
    while retries < MAX_RETRIES:
        url = "http://localhost:36912/browser/stop-profile"

        payload = json.dumps({
            "profileId": browser_id
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 204:
            return True
        else:
            retries += 1
            time.sleep(1)


def delete_browser(browser_id):
    retries = 0
    while retries < MAX_RETRIES:
        url = f"https://api.gologin.com/browser/{browser_id}"

        payload = {}
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)

        if response.status_code == 204:
            return True
        else:
            retries += 1
            time.sleep(1)
