#!/bin/bash

export $(grep -v '^#' .env | xargs)

echo "CLIENT_ID: $CAME_CONNECT_CLIENT_ID"

export AUTH_CODE=$(curl -s -X POST "https://app.cameconnect.net/api/oauth/auth-code" \
  -u "$CAME_CONNECT_CLIENT_ID:$CAME_CONNECT_CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "client_id=$CAME_CONNECT_CLIENT_ID" \
  -d "client_secret=$CAME_CONNECT_CLIENT_SECRET" \
  -d "username=$CAME_CONNECT_USERNAME" \
  -d "password=$CAME_CONNECT_PASSWORD" \
  -d "redirect_uri=https://beta.cameconnect.net/role" \
  -d "response_type=code" \
  -d "client_type=confidential" \
  -d "state=abcdefgh1234" | jq -r '.code')

echo "AUTH_CODE: $AUTH_CODE"

export AUTH_TOKEN=$(curl -s -X POST "https://app.cameconnect.net/api/oauth/token" \
  -u "$CAME_CONNECT_CLIENT_ID:$CAME_CONNECT_CLIENT_SECRET" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Accept: application/json" \
  -d "grant_type=authorization_code" \
  -d "code=$AUTH_CODE" \
  -d "redirect_uri=https://beta.cameconnect.net/role" | grep -oP '{.*}' | tail -n 1 | jq -r '.access_token')

echo "AUTH_TOKEN: $AUTH_TOKEN"