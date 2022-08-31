ARG BUILD_FROM=ghcr.io/hassio-addons/base:12.2.3
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base
# hadolint ignore=DL3003
RUN \
    apk add --no-cache --virtual .build-dependencies \
        build-base=0.5-r3 \
        git=2.36.2-r0 \
    \
    && apk add --no-cache \
        go=1.18.5-r0 \
        libqrencode=4.1.1-r0 \
        openresolv=3.12.0-r0 \
        wireguard-tools=1.0.20210914-r0 \
    \
    && git clone --branch "0.0.20220316" --depth=1 \
        "https://git.zx2c4.com/wireguard-go" /tmp/wireguard \
    \
    && cd /tmp/wireguard \
    && make \
    && make install \
    \
    && rm -f -r /tmp/* \
    && apk del --no-cache --purge \
        .build-dependencies \
        go

COPY root /

# Build api client
RUN \
    apk add --no-cache py3-pip && \
    cd /etc/services.d/api && \
    pip3 install -r requirements.txt && \
    cd -
