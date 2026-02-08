FROM ekofr/pihole-exporter:latest AS upstream

FROM alpine:3.19
RUN apk add --no-cache ca-certificates curl
COPY --from=upstream /root/pihole-exporter /usr/local/bin/pihole-exporter

EXPOSE 9617
ENTRYPOINT ["/usr/local/bin/pihole-exporter"]