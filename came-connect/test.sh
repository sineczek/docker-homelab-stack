#!/bin/bash

ACCESS_TOKEN="$ACCESS_TOKEN"
DEVICE_ID="$DEVICE_ID"
LOG_FILE="came_cloud_bruteforce.log"

> $LOG_FILE

declare -a methods=("POST" "PUT" "PATCH")
declare -a endpoints=(
"/api/devices/$DEVICE_ID/commands"
"/api/devices/$DEVICE_ID/control"
"/api/devices/$DEVICE_ID/actions"
"/api/commands"
)
declare -a payloads=(
'{"commandId":5,"outputId":1}'
'{"commandId":5,"target":1}'
'{"commandId":5,"outputId":1,"siteId":201975,"deviceId":308545}'
'{"commandId":5,"target":1,"siteId":201975,"deviceId":308545,"actionType":"move"}'
)

for method in "${methods[@]}"; do
  for endpoint in "${endpoints[@]}"; do
    for payload in "${payloads[@]}"; do
      echo "Testing $method $endpoint with $payload" >> $LOG_FILE
      curl -s -X $method "https://app.cameconnect.net$endpoint" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$payload" >> $LOG_FILE
      echo -e "\n---" >> $LOG_FILE
    done
  done
done

echo "Test zakończony. Wyniki w $LOG_FILE"