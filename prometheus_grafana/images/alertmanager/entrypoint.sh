#!/bin/sh
set -e

: "${AM_SMTP_HOST:?AM_SMTP_HOST is required}"
: "${AM_SMTP_FROM:?AM_SMTP_FROM is required}"
: "${AM_SMTP_TO:?AM_SMTP_TO is required}"
: "${AM_TG_BOT_TOKEN:?AM_TG_BOT_TOKEN is required}"
: "${AM_TG_CHAT_ID:?AM_TG_CHAT_ID is required}"

TEMPLATE="/etc/alertmanager/alertmanager.yml"
RENDERED="/var/lib/alertmanager/alertmanager.rendered.yml"

mkdir -p "$(dirname "$RENDERED")"

cp "$TEMPLATE" "$RENDERED"

for v in AM_SMTP_HOST AM_SMTP_FROM AM_SMTP_TO AM_TG_BOT_TOKEN AM_TG_CHAT_ID; do
  eval "val=\${$v:-}"
  esc_val=$(printf '%s' "$val" | sed -e 's/[\/&]/\\&/g')
  sed -i "s|\${$v}|$esc_val|g; s|\$$v|$esc_val|g" "$RENDERED"
done

exec /usr/local/bin/alertmanager \
  --config.file="$RENDERED" \
  --storage.path=/var/lib/alertmanager