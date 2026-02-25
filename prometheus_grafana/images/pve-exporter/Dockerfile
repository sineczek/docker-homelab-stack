# syntax=docker/dockerfile:1

FROM curlimages/curl:8.10.1 AS curlsrc

FROM prompve/prometheus-pve-exporter:latest

COPY --from=curlsrc /usr/bin/curl /usr/local/bin/curl

EXPOSE 9221

