ARG BUILD_FROM=ghcr.io/hassio-addons/base/amd64:11.0.0
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add make gcc g++ python3 linux-headers git nodejs npm nginx py3-pip
RUN pip3 install pyyaml
RUN mkdir -p /run/nginx
RUN mkdir -p /opt/zigbee2mqtt && wget -c https://github.com/Koenkk/zigbee2mqtt/archive/refs/tags/1.25.2.tar.gz -O - | tar -C /opt/zigbee2mqtt --strip 1 -xz
WORKDIR /opt/zigbee2mqtt
RUN npm ci

COPY root /

COPY frontend /frontend
RUN \
  cd /frontend && \
  npm install && \
  npm run build && \
  cd - && rm -rf /frontend

