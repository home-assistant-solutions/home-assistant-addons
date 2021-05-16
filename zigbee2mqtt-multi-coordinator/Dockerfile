ARG BUILD_FROM=ghcr.io/hassio-addons/base/amd64:9.1.7
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add --no-cache --virtual .buildtools make gcc g++ python3 linux-headers git nodejs npm
RUN git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
WORKDIR /opt/zigbee2mqtt
RUN npm ci --production

COPY root /