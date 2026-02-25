# syntax=docker/dockerfile:1

FROM prom/alertmanager:v0.27.0 AS upstream

FROM curlimages/curl:8.10.1

USER root
RUN mkdir -p /var/lib/alertmanager && chown -R 65534:65534 /var/lib/alertmanager

COPY --from=upstream /bin/alertmanager /usr/local/bin/alertmanager

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER 65534
EXPOSE 9093

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]