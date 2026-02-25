FROM python:3.12-alpine

RUN apk add --no-cache ca-certificates curl git \
 && git clone --depth 1 https://github.com/tarkilhk/pihole6_exporter_with_queries_time /opt/src

WORKDIR /opt/src/metrics_exporter
RUN pip install --no-cache-dir -r ../requirements.txt

COPY run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 9666
ENV PH_HOST=localhost PH_KEY="" PH_PORT=9666

ENTRYPOINT ["/run.sh"]