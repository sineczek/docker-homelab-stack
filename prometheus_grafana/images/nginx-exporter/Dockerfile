FROM nginx/nginx-prometheus-exporter:1.5.1 AS upstream

FROM alpine:3.19
RUN apk add --no-cache ca-certificates curl
COPY --from=upstream /usr/bin/nginx-prometheus-exporter /usr/local/bin/nginx-prometheus-exporter

EXPOSE 9113
ENTRYPOINT ["/usr/local/bin/nginx-prometheus-exporter"]