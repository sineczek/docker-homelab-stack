FROM debian:trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nut \
    nut-snmp \
    snmp \
    curl wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj własne pliki konfiguracyjne
COPY conf/ /etc/nut/

CMD ["upsd", "-D"]
