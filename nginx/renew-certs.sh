#!/usr/bin/env bash
set -euo pipefail

cd /opt/docker_volumes/nginx

# lock, żeby nie odpaliło się równolegle
exec 9>/var/lock/certbot-renew.lock
flock -n 9 || exit 0

# Odnowienie certów (DNS Cloudflare)
docker compose run --rm certbot renew \
  --dns-cloudflare \
  --dns-cloudflare-credentials /cloudflare.ini \
  --dns-cloudflare-propagation-seconds 60 \
  --non-interactive \
  --quiet

# Reload nginx, żeby podniósł nowe certy z plików
docker exec nginx nginx -t
docker exec nginx nginx -s reload
