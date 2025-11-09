import requests

# Konfiguracja
base_url = "http://192.168.4.118:9102"
device_id = 308545

# Zakres testowanych command_id dla OPEN, CLOSE, STOP
command_ids = {
    "OPEN": [5, 6, 7, 8, 9, 10],
    "CLOSE": [2, 3, 4, 11, 12, 13],
    "STOP": [129, 130, 131, 132, 133, 134]
}

# Wyniki testów
results = []

for action, ids in command_ids.items():
    for cmd_id in ids:
        url = f"{base_url}/devices/{device_id}/command/{cmd_id}"
        try:
            response = requests.post(url, timeout=5)
            results.append((action, cmd_id, response.status_code, response.text[:200]))
        except Exception as e:
            results.append((action, cmd_id, "ERROR", str(e)))

# Zapis wyników do pliku
with open("came_command_test_results.txt", "w") as f:
    for action, cmd_id, status, detail in results:
        line = f"{action} command_id {cmd_id}: {status} -> {detail}\n"
        f.write(line)