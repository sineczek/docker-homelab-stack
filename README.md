# Self-Hosted Homelab Stack

This repository contains a collection of Docker-based services used in a self-hosted homelab environment. It is designed to be modular, secure, and extensible, with environment variables managed via `.env` files and examples provided via `.env.example`. The stack includes infrastructure, automation, monitoring, networking, and utility services. 

---

## 📦 Included Services

### acame-connect
Integration service for connecting external devices or APIs to the homelab.

### clamav
Antivirus service using ClamAV for scanning files and containers.

### dockge
A lightweight web UI for managing Docker Compose projects.

### homepage
A customizable dashboard for displaying service status, links, and widgets.

### nebula-sync
Peer-to-peer synchronization service using the Nebula overlay network.

### newrelic-infra
New Relic Infrastructure agent for monitoring system metrics and performance.

### nginx
Reverse proxy and static file server, often used with Traefik or standalone.

### nut
Network UPS Tools server for monitoring and managing UPS devices.

### nut-server
Dedicated NUT server container exposing UPS data to clients.

### webnut
Web interface for NUT, allowing UPS status visualization.

### nut_webgui
Alternative web GUI for NUT, supporting multiple UPS endpoints.

### pihole-EventHorizon
Pi-hole DNS filtering instance for the EventHorizon node.

### portainer
Web-based Docker container management UI.

### postfix-relay
SMTP relay service using Postfix, configured for secure mail forwarding.

### rclone
Command-line tool for syncing files to cloud storage providers.

### traefik
Reverse proxy and load balancer with automatic SSL via Let's Encrypt.

### wazuh
Security monitoring platform including Wazuh Manager, Indexer, and Dashboard.


## Scripts
### pre-commit hook
It’s a Git pre-commit hook that scans Docker Compose files for hardcoded sensitive values like passwords or API keys and prevents commits if any are found. It ensures that secrets are kept in environment variables or .env files, helping maintain secure configuration practices.

### env.example generator
Recursively scans the repository for .env files and generates corresponding .env.example files containing only the keys with empty values. It preserves comments and blank lines, making it easy to provide configuration examples without exposing sensitive data.
---

## 📁 Directory Structure
.
├── acame-connect/
├── clamav/
├── dockge/
├── homepage/
├── nebula-sync/
├── newrelic-infra/
├── nginx/
├── nut/
├── nut-server/
├── nut_webgui/
├── pihole-EventHorizon/
├── portainer/
├── postfix-relay/
├── rclone/
├── traefik/
├── wazuh/
└── webnut/

## 🔐 Security Notes

- All .env files are excluded via .gitignore.
- Example files (.env.example) are provided for safe configuration sharing.
- SSL certificates, keys, and secrets should be stored securely and never committed.