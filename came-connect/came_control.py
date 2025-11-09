import os
import requests
import json


# Dane konfiguracyjne

CLIENT_ID = os.getenv("CAME_CONNECT_CLIENT_ID")
CLIENT_SECRET = os.getenv("CAME_CONNECT_CLIENT_SECRET")
USERNAME = os.getenv("CAME_CONNECT_USERNAME")
PASSWORD = os.getenv("CAME_CONNECT_PASSWORD")

REDIRECT_URI = "https://app.cameconnect.net/role"
QBE_IP = "192.168.55.134"  # lokalny mostek
DEVICE_ID = 308545  # np. z API devices
COMMAND_OPEN = 5  # otwórz
COMMAND_CLOSE = 2  # zamknij


def get_auth_code():
    url = "https://app.cameconnect.net/api/oauth/auth-code"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "username": USERNAME,
        "password": PASSWORD,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile"
    }
    response = requests.post(url, auth=(CLIENT_ID, CLIENT_SECRET), headers=headers, data=data)
    print("DEBUG:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()["code"]


def get_access_token(auth_code):
    url = "https://app.cameconnect.net/api/oauth/token"
    response = requests.post(url,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI
        }
    )
    response.raise_for_status()
    token_data = response.json()
    with open("token.json", "w") as f:
        json.dump(token_data, f)
    return token_data["access_token"]

def send_command(token, command_id):
    url = f"http://{QBE_IP}:8000/devices/{DEVICE_ID}/command/{command_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(response.status_code, response.text)

if __name__ == "__main__":
    print("Pobieram auth_code...")
    auth_code = get_auth_code()
    print("Auth code:", auth_code)

    print("Wymieniam na access_token...")
    token = get_access_token(auth_code)
    print("Access token:", token)

    # Test: otwarcie rolety
    print("Wysyłam komendę OTWÓRZ...")
    send_command(token, COMMAND_OPEN)