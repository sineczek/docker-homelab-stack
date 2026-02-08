#!/usr/bin/env bash
set -euo pipefail
TS=$(date +%Y%m%d_%H%M%S)
OUT="/opt/docker_volumes/_backups/monitoring_backup_${TS}.tar.gz"
tar -czf "$OUT" \
  -C /opt/docker_volumes/prometheus_grafana \
  prometheus/prometheus.yml \
  prometheus/rules \
  grafana/provisioning \
  alertmanager/alertmanager.yml \
  alertmanager/templates \
  exporters
echo "Backup -> $OUT"