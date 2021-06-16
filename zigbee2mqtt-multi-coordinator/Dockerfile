ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.12
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add make gcc g++ python3 linux-headers git nodejs npm nginx py3-pip
RUN mkdir /run/nginx
RUN git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
WORKDIR /opt/zigbee2mqtt
RUN npm ci --production

COPY root /

RUN \ 
  cd /etc/services.d/api && \
  pip3 install -r requirements.txt && \
  cd -

COPY frontend /frontend
RUN \
  cd /frontend && \
  npm install && \
  npm run build && \
  cd - && rm -rf /frontend

RUN git clone https://github.com/nurikk/z2m-frontend.git /frontend
RUN \
  cd /frontend && \
  npm install && \
  npm run build && \
  mv ./dist /var/www/frontend/zigbee2mqtt-frontend && \
  cd - && rm -rf /frontend

