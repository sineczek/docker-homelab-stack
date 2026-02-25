
FROM ribbybibby/ssl-exporter:latest AS upstream

FROM curlimages/curl:8.10.1
USER 65534
COPY --from=upstream /ssl_exporter /usr/local/bin/ssl_exporter
EXPOSE 9219
ENTRYPOINT ["/usr/local/bin/ssl_exporter"]
