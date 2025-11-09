
import requests
import logging
import string
import random
from requests.auth import HTTPBasicAuth
import hashlib
import base64
import json
import web
import os

logging.basicConfig(level=logging.INFO)

# --- helper functions ---
def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_code_challenge(code_verifier):
    encoded_bytes = base64.b64encode(hashlib.sha256(code_verifier.encode()).digest())
    encoded_str = str(encoded_bytes, "utf-8").replace("=", "").replace("+", "-" ).replace("/", "_")
    return encoded_str

def fetch_auth_code(code_verifier):
    client_id = os.environ['CAME_CONNECT_CLIENT_ID']
    client_secret = os.environ['CAME_CONNECT_CLIENT_SECRET']
    username = os.environ['CAME_CONNECT_USERNAME']
    password = os.environ['CAME_CONNECT_PASSWORD']
    nonce = random_string(100)
    state = random_string(100)
    code_challenge = generate_code_challenge(code_verifier)
    url = f"https://app.cameconnect.net/api/oauth/auth-code?client_id={client_id}&response_type=code&redirect_uri=https://www.cameconnect.net/role&state={state}&nonce={nonce}&code_challenge={code_challenge}&code_challenge_method=S256"
    data = {'grant_type': 'authorization_code', 'client_id': client_id, 'username': username, 'password': password}
    response = requests.post(url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    response.raise_for_status()
    return response.json()['code']

def fetch_bearer_token(client_id, client_secret, code, code_verifier):
    redirect_uri = 'https://www.cameconnect.net/role'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }
    url = "https://app.cameconnect.net/api/oauth/token"
    response = requests.post(url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    response.raise_for_status()
    json_data = response.json()
    return {'access_token': json_data['access_token'], 'expires_in': json_data['expires_in']}

def fetch_token():
    logging.info("Connecting to CAME Connect to fetch token...")
    code_verifier = random_string(100)
    try:
        code = fetch_auth_code(code_verifier)
        logging.info("Auth code fetched successfully.")
        bearer = fetch_bearer_token(
            os.environ['CAME_CONNECT_CLIENT_ID'],
            os.environ['CAME_CONNECT_CLIENT_SECRET'],
            code,
            code_verifier
        )
        logging.info("Bearer token retrieved successfully.")
        return bearer['access_token']
    except Exception as e:
        logging.error(f"Failed to fetch token from CAME Connect: {e}")
        raise

def fetch_sites(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get('https://app.cameconnect.net/api/sites', headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_devices(token):
    sites = fetch_sites(token)
    return sites.get('Data')[0].get('Devices')

def run_command_for_device(token, device_id, command_id):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://app.cameconnect.net/api/automations/{device_id}/commands/{command_id}"
    res = requests.post(url, headers=headers)
    return res.json()

# --- web.py endpoints ---
urls = (
    '/devices/(.*)/command/(.*)', 'DeviceCommand',
    '/devices', 'DevicesList',
    '/devices/(.*)/commands', 'DeviceCommands'
)

class DeviceCommand:
    def GET(self, device_id, command_id):
        logging.info(f"GET /devices/{device_id}/command/{command_id}")
        token = fetch_token()
        res = run_command_for_device(token, device_id, command_id)
        web.header('Content-Type', 'application/json')
        return json.dumps(res)

def POST(self, device_id, command_id):
    logging.info(f"Executing command {command_id} on device {device_id}")
    token = fetch_token()
    url = f"https://app.cameconnect.net/api/automations/{device_id}/commands/{command_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers, timeout=30)
    try:
        res = response.json()
    except ValueError:
        logging.error(f"Nie udało się sparsować JSON. Status: {response.status_code}, Treść: {response.text}")
        res = {
            "error": "Invalid JSON response",
            "status": response.status_code,
            "raw": response.text
        }

    web.header('Content-Type', 'application/json')
    return json.dumps(res)

class DevicesList:
    def GET(self):
        logging.info("GET /devices")
        token = fetch_token()
        devices = fetch_devices(token)
        web.header('Content-Type', 'application/json')
        return json.dumps(devices)

class DeviceCommand:
    def POST(self, device_id, command_id):
        logging.info(f"Executing command {command_id} on device {device_id}")
        token = fetch_token()
        url = f"https://app.cameconnect.net/api/automations/{device_id}/commands/{command_id}"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(url, headers=headers, timeout=30)
        try:
            res = response.json()
        except ValueError:
            logging.error(f"Nie udało się sparsować JSON. Status: {response.status_code}, Treść: {response.text}")
            res = {
                "error": "Invalid JSON response",
                "status": response.status_code,
                "raw": response.text
            }

        web.header('Content-Type', 'application/json')
        return json.dumps(res)

# --- run web.py ---
app = web.application(urls, globals())

if __name__ == "__main__":
    logging.info("Starting CAME Bridge on 0.0.0.0:8080")
    app.run()
