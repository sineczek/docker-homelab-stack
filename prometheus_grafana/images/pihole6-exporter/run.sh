#!/bin/sh
set -e
: "${PH_HOST:?PH_HOST required}"
: "${PH_KEY:?PH_KEY required}"
: "${PH_PORT:=9666}"

exec python /opt/src/metrics_exporter/pihole6_metrics_exporter.py \
  -H "${PH_HOST}" \
  -k "${PH_KEY}" \
  -p "${PH_PORT}"