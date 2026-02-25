
FROM prom/blackbox-exporter:latest AS upstream

FROM curlimages/curl:8.10.1
USER 65534
COPY --from=upstream /bin/blackbox_exporter /usr/local/bin/blackbox_exporter
EXPOSE 9115
ENTRYPOINT ["/usr/local/bin/blackbox_exporter"]
