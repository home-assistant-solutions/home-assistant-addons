ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.12
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add make gcc g++ python3 linux-headers git nodejs npm nginx py3-pip
RUN pip3 install pyyaml
RUN mkdir /run/nginx
RUN git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
WORKDIR /opt/zigbee2mqtt
RUN npm ci --production

COPY root /

COPY frontend /frontend
RUN \
  cd /frontend && \
  npm install && \
  npm run build && \
  cd - && rm -rf /frontend

