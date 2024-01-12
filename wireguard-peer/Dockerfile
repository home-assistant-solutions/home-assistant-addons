ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.4
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base
# hadolint ignore=DL3003
RUN \
    apk add --no-cache --virtual .build-dependencies \
        build-base=0.5-r3 \
        git=2.43.0-r0 \
    \
    && apk add --no-cache \
        go=1.21.5-r0 \
        iptables=1.8.10-r3 \
        libqrencode-tools=4.1.1-r2 \
        openresolv=3.13.2-r0 \
        wireguard-tools=1.0.20210914-r3 \
    \
    && ln -sf /sbin/xtables-nft-multi /sbin/ip6tables \
    && ln -sf /sbin/xtables-nft-multi /sbin/iptables \
    && git clone --branch "0.0.20230223" --depth=1 \
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
