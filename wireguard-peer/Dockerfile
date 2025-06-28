ARG BUILD_FROM=ghcr.io/hassio-addons/base:18.0.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base
# hadolint ignore=DL3003
RUN \
    apk add --no-cache --virtual .build-dependencies \
        build-base=0.5-r3 \
        git=2.49.0-r0 \
    \
    && apk add --no-cache \
        go=1.24.4-r0 \
        iptables=1.8.11-r1 \
        libqrencode-tools=4.1.1-r3 \
        openresolv=3.14.1-r0 \
        wireguard-tools=1.0.20250521-r0 \
    \
    && ln -sf /sbin/xtables-nft-multi /sbin/ip6tables \
    && ln -sf /sbin/xtables-nft-multi /sbin/iptables \
    && git clone --branch "master" --depth=1 \
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
